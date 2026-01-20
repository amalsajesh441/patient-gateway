from datetime import date, datetime

def calculate_age(birth_date: str) -> int:
    dob = datetime.strptime(birth_date, "%Y-%m-%d").date()
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


def extract_patient_data(data: dict) -> dict:
    if data.get("resourceType") != "Patient":
        raise ValueError("Invalid FHIR resource")

    name_obj = data["name"][0]
    full_name = " ".join(name_obj.get("given", [])) + " " + name_obj.get("family", "")

    ssn = None
    passport = None

    for identifier in data.get("identifier", []):
        system = identifier.get("system", "").lower()
        if "us-ssn" in system:
            ssn = identifier.get("value")
        if "passport" in system:
            passport = identifier.get("value")

    age = calculate_age(data["birthDate"])
    if age < 18:
        raise ValueError("Patient must be at least 18 years old")

    return {
        "patient_id": data["id"],
        "full_name": full_name.strip(),
        "gender": data.get("gender"),
        "birth_date": data["birthDate"],
        "ssn": ssn,
        "passport": passport,
    }
