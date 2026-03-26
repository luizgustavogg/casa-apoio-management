from decimal import Decimal
from datetime import date, datetime
from threading import local

from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from people.models import Checkin, Checkout, HomeServices, ProfessionalServices
from people.models.audit_log import AuditLog


_SIGNAL_STATE = local()
TRACKED_MODELS = (Checkin, Checkout, HomeServices, ProfessionalServices)
IGNORED_CHANGE_FIELDS = {"updated_at"}


def _storage():
    if not hasattr(_SIGNAL_STATE, "before_snapshots"):
        _SIGNAL_STATE.before_snapshots = {}
    return _SIGNAL_STATE.before_snapshots


def _snapshot_key(model_label, object_id):
    return f"{model_label}:{object_id}"


def _normalize_value(value):
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return value


def _serialize_instance(instance):
    data = {}
    for field in instance._meta.fields:
        raw_value = field.value_from_object(instance)
        field_name = field.name
        if field.is_relation and hasattr(field, "attname") and field.attname:
            # Store FK values by *_id while preserving the model field name.
            raw_value = getattr(instance, field.attname)
        data[field_name] = _normalize_value(raw_value)
    return data


def _safe_create_log(
    *, action, instance, before_data=None, after_data=None, changed_fields=None
):
    try:
        AuditLog.objects.create(
            action=action,
            entity=instance._meta.model_name,
            object_id=instance.pk,
            changed_fields=changed_fields or [],
            before_data=before_data,
            after_data=after_data,
        )
    except Exception:
        # Never block operational flows due to audit persistence issues.
        return


def _compute_changed_fields(before_data, after_data):
    if not before_data or not after_data:
        return []
    changed = []
    all_keys = set(before_data.keys()) | set(after_data.keys())
    for key in sorted(all_keys):
        if key in IGNORED_CHANGE_FIELDS:
            continue
        if before_data.get(key) != after_data.get(key):
            changed.append(key)
    return changed


@receiver(pre_save)
def capture_before_state(sender, instance, **kwargs):
    if sender not in TRACKED_MODELS or not instance.pk:
        return

    try:
        previous = sender.objects.filter(pk=instance.pk).first()
        if not previous:
            return
        model_label = sender._meta.label_lower
        _storage()[_snapshot_key(model_label, instance.pk)] = _serialize_instance(
            previous
        )
    except Exception:
        return


@receiver(post_save)
def create_or_update_audit_log(sender, instance, created, **kwargs):
    if sender not in TRACKED_MODELS:
        return

    after_data = _serialize_instance(instance)

    if created:
        _safe_create_log(
            action=AuditLog.ACTION_CREATE,
            instance=instance,
            before_data=None,
            after_data=after_data,
            changed_fields=sorted(after_data.keys()),
        )
        return

    model_label = sender._meta.label_lower
    before_data = _storage().pop(_snapshot_key(model_label, instance.pk), None)
    changed_fields = _compute_changed_fields(before_data, after_data)

    if changed_fields:
        _safe_create_log(
            action=AuditLog.ACTION_UPDATE,
            instance=instance,
            before_data=before_data,
            after_data=after_data,
            changed_fields=changed_fields,
        )


@receiver(post_delete)
def create_delete_audit_log(sender, instance, **kwargs):
    if sender not in TRACKED_MODELS:
        return

    before_data = _serialize_instance(instance)
    _safe_create_log(
        action=AuditLog.ACTION_DELETE,
        instance=instance,
        before_data=before_data,
        after_data=None,
        changed_fields=sorted(before_data.keys()),
    )
