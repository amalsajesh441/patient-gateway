# Patient Interoperability Gateway (PIGW)

## Overview

Patient Interoperability Gateway (PIGW) is a HIPAA-compliant Django microservice designed to securely ingest, store, and retrieve FHIR R4 Patient data.
It validates incoming healthcare data, encrypts sensitive PHI fields (SSN & Passport), supports audit logging, and exposes sanitized APIs for downstream systems.

This project simulates a real-world healthcare interoperability service.

---

## Tech Stack

* Python 3.10+
* Django 5.x
* Django REST Framework
* PostgreSQL
* Celery + Redis
* Cryptography (Fernet Encryption)

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-private-repo-url>
cd patient-gateway
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key
FERNET_KEY=your-fernet-key
DB_NAME=patients_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379/0
```

Generate Fernet key:

```bash
python - <<EOF
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
EOF
```

---

## Database Setup (PostgreSQL)

```bash
sudo -u postgres createdb patients_db
```

Update `settings.py`:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "patients_db",
        "USER": "postgres",
        "PASSWORD": "yourpassword",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

Run migrations:

```bash
python manage.py migrate
```

---

## Run the Server

```bash
python manage.py runserver
```

Server runs at:

```
http://127.0.0.1:8000/
```

---

## API Endpoints

### 1. Patient Intake (POST)

```
POST /api/v1/patient-intake/
```

Sample Body:

```json
{
  "fhir_payload": {
    "resourceType": "Patient",
    "id": "example-123",
    "birthDate": "1980-12-25",
    "gender": "male",
    "identifier": [
      {
        "system": "http://hl7.org/fhir/sid/us-ssn",
        "value": "000-12-3456"
      }
    ],
    "name": [
      {
        "family": "Chalmers",
        "given": ["Peter", "James"]
      }
    ]
  }
}
```

Success Response:

```json
{
  "message": "Patient intaked successfully",
  "id": "example-123"
}
```

---

### 2. Patient Retrieval (GET)

```
GET /api/v1/patients/<patient_id>/
```

Response:

```json
{
  "patient_id": "example-123",
  "full_name": "Peter James Chalmers",
  "gender": "male",
  "birth_date": "1980-12-25",
  "masked_ssn": "***-**-3456"
}
```

---

### 3. Access Logs

Audit logs are stored in the `AccessLog` model with:

* Timestamp
* IP address
* User
* Patient accessed

You can view logs in Django Admin.

---

## Background Tasks (Celery)

Start Redis:

```bash
redis-server
```

Start Celery worker:

```bash
celery -A pigw worker -l info
```

Welcome emails are triggered after successful patient intake.

---

## Security Design Decisions

### PHI Encryption

* SSN and Passport are encrypted using Fernet symmetric encryption.
* Encryption key is stored in environment variables.
* Raw FHIR payload is stored for audit purposes.

### Masking

Only the last 4 digits of SSN are exposed in API responses.

---

## Running Tests (Optional)

```bash
python manage.py test
```