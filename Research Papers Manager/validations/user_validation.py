import re


USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9_]{3,20}$')
EMAIL_REGEX = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')


def validate_username(username):
    return USERNAME_REGEX.match(username)


def validate_email(email):
    return EMAIL_REGEX.match(email)


def validate_user_data(data):
    username = data.get('username', '').strip()
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    department = data.get('department', '').strip()

    if not username or not validate_username(username):
        return False, "Invalid username. Use 3-20 letters, digits, underscores."

    if name and len(name) > 100:
        return False, "Name must be at most 100 characters."

    if email and (not validate_email(email) or len(email) > 100):
        return False, "Invalid email address."

    if department and len(department) > 100:
        return False, "Department must be at most 100 characters."

    return True, None