# Patient Gateway (PIGW)

## Overview
A HIPAA-compliant Django microservice for ingesting, storing, and retrieving FHIR Patient data securely.

## Tech Stack
- Django 5
- DRF
- PostgreSQL
- Celery + Redis
- Fernet Encryption

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
