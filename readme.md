### Create virtual enviroment

- > python -m venv myvenv

### Activate virtual enviroment

- > . myvenv/Scripts/activate

### Install requirements

- > pip install -r requirements.txt

### In production, include enviroment variables

- > set DATABASE_URL=postgres://o.......

- > set SECRET_KEY=e6=m0rind-)pn+aw......

### Enter project folder

- > cd danielle

### Makemigrations and migrate

- > python manage.py makemigrations
- > python manage.py migrate

### Create superuser

- > python manage.py createsuperuser

### Run seeds

- Popular o banco e necessario para o dashboard exibir dados realistas.
- Recomendado para demo do dashboard (dados variados):

- > python manage.py seed_dashboard_data --reset --people 90 --days 60

- Se preferir a carga fixa em JSON, use:

- > python manage.py loaddata people/seed/people.json
- > python manage.py loaddata people/seed/checkins.json
- > python manage.py loaddata people/seed/home-services.json
- > python manage.py loaddata people/seed/professional-services.json

### Test and coverage

- > python -m pytest
- > python -m coverage run -m pytest
- > python -m coverage html

### Run the application

- > python manage.py runserver

### Local database default (SQLite)

- SQLite is now the default for local runs. No extra env var is required.

- > python manage.py migrate
- > python manage.py runserver

### Use MySQL (optional)

- PowerShell:
  - > $env:USE_MYSQL="1"
  - > $env:MYSQL_DATABASE="casa_apoio_management"
  - > $env:MYSQL_USER="root"
  - > $env:MYSQL_PASSWORD="your_password"
  - > $env:MYSQL_HOST="127.0.0.1"
  - > $env:MYSQL_PORT="3306"
  - > python manage.py migrate
  - > python manage.py runserver

- CMD:
  - > set USE_MYSQL=1
  - > set MYSQL_DATABASE=casa_apoio_management
  - > set MYSQL_USER=root
  - > set MYSQL_PASSWORD=your_password
  - > set MYSQL_HOST=127.0.0.1
  - > set MYSQL_PORT=3306
  - > python manage.py migrate
  - > python manage.py runserver

### Rotas

- Users
  - `POST /users/` -> Create new user (username,password,email)
  - `POST /login/` -> Create token (username,password)
- People
  - `GET /api/v1/people/` -> List 12 card people.
  - `POST /api/v1/people/` -> Create new person.
  - `GET /api/v1/people/<int:id>/` -> List person by id.
  - `PUT /api/v1/people/<int:id>/` -> Replace all mandatory fields. plus fields in request.
  - `Patch /api/v1/people/<int:id>/` -> Replace only fields in request.
  - `Delete /api/v1/people/<int:id>/` -> Delete person by ID

### API docs (drf-spectacular)

- OpenAPI schema (JSON): `GET /api/schema/`
- Swagger UI: `GET /api/docs/swagger/`
- ReDoc: `GET /api/docs/redoc/`

### Dashboard (MVT - sem autenticação)

- Acesso público: `GET /dashboard`
- Indicadores em tempo real:
  - Total de pessoas cadastradas
  - Check-ins ativos/totais
  - Distribuição por gênero
  - Tipos de check-in
  - Tipos de tratamento (quimioterapia, radioterapia, cirurgia, exames, consultas)
  - Serviços da casa
  - Vagas sociais

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
- Forma

### Views

- Add class methods (choose right)
- Add view custom rules
- Add filters
- Add search
- Add ordering
- Add pagination
- Add authentications, authorization, permissions
