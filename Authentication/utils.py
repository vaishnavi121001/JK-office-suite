# generate password function
def generate_password(full_name, adhar_card):
    return full_name.strip().lower()[:3] + adhar_card.strip()[-4:]
