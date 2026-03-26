### Create virtual environment

- > python -m venv myvenv

### Activate virtual environment

- > . myvenv/Scripts/activate

### Install requirements

- > pip install -r requirements.txt

### Enter project folder

- > cd danielle

### Run migrations

- > python manage.py makemigrations
- > python manage.py migrate

### Create superuser

- > python manage.py createsuperuser

### Run seeds

- Populate the database to show realistic dashboard metrics.
- Recommended for dashboard demos (varied data):

- > python manage.py seed_dashboard_data --reset --people 90 --days 60

- If you prefer fixed JSON fixtures, use:

- > python manage.py loaddata people/seed/people.json
- > python manage.py loaddata people/seed/checkins.json
- > python manage.py loaddata people/seed/home-services.json
- > python manage.py loaddata people/seed/professional-services.json

### Test and coverage

- > python -m pytest
- > python -m coverage run -m pytest
- > python -m coverage html
- > python -m pytest --cov=people --cov=utils --cov-report=term-missing

### Run the application

- > python manage.py runserver

### Local database default (SQLite)

- SQLite is now the default for local runs. No extra env var is required.

- > python manage.py migrate
- > python manage.py runserver

### Routes

- Users
  - `POST /users/` -> Create new user (username,password,email)
  - `POST /login/` -> Create token (username,password)
- People
  - `GET /api/v1/people/` -> List 12 card people.
  - `POST /api/v1/people/` -> Create new person.
  - `GET /api/v1/people/<int:id>/` -> Get person by ID.
  - `PUT /api/v1/people/<int:id>/` -> Replace all mandatory fields. plus fields in request.
  - `PATCH /api/v1/people/<int:id>/` -> Replace only fields sent in request.
  - `DELETE /api/v1/people/<int:id>/` -> Delete person by ID.

### API docs (drf-spectacular)

- OpenAPI schema (JSON): `GET /api/schema/`
- Swagger UI: `GET /api/docs/swagger/`
- ReDoc: `GET /api/docs/redoc/`

### Dashboard (MVT - no authentication)

- Public access: `GET /dashboard`
- Real-time indicators:
  - Total registered people
  - Active/total check-ins
  - Gender distribution
  - Check-in types
  - Treatment types (chemotherapy, radiotherapy, surgery, exams, appointments)
  - Home services usage
  - Social vacancies

## Steps done

### Models

- Create people app
- Add People app in settings
- Create the following models:
  - Base
  - Person
  - Checkin
  - Checkout
  - HomeServices
  - ProfessionalServices
- Add verbose name to models
- Add help text to models
- Add blank and null, if necessary
- Add `__str__` to models
- Add validators (CPF, CEP, EMAIL, ...)
- Add formatted_field methods to after deserialization

### Admin

- Register model to admin
- Customize section fields
- Customize list display
- Customize list filter
- Customize search fields
- Customize inline fields
- Customize collapse section fields

### Settings

- Add Authentication
- Add Permission
- Add Time Zone
- Add Language
- Add Cors
- Add Pagination

## Validations

- For each field in models, create custom validations, if necessary
- Create unit test for all validations above

### Serializers

- Exclude fields if necessary
- Include fields if necessary
- Format fields when needed

### Views

- Add class methods (choose right)
- Add view custom rules
- Add filters
- Add search
- Add ordering
- Add pagination
- Add authentications, authorization, permissions
