import re
from datetime import datetime

def is_not_empty(value):
    return bool(value and value.strip())

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def is_valid_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def is_valid_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def is_within_range(value, min_value, max_value):
    try:
        num = float(value)
        return min_value <= num <= max_value
    except ValueError:
        return False

def is_within_length(value, max_length):
    return len(value) <= max_length

def is_secure_password(password):
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[\W_]', password):
        return False
    return True
