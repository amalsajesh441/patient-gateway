def mask_ssn(ssn: str) -> str:
    if not ssn or len(ssn) < 4:
        return None
    return "***-**-" + ssn[-4:]
