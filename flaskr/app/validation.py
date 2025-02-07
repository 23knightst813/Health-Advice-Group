import re
from datetime import datetime

def is_not_empty(value):
    """
    Check if the given value is not empty or only whitespace.

    Args:
        value (str): The value to check.

    Returns:
        bool: True if the value is not empty, False otherwise.
    """
    return bool(value and value.strip())

def is_valid_email(email):
    """
    Validate the given email address using a regular expression.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email address is valid, False otherwise.
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_valid_date(date_str):
    """
    Validate the given date string in the format 'YYYY-MM-DD'.

    Args:
        date_str (str): The date string to validate.

    Returns:
        bool: True if the date string is valid, False otherwise.
    """
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def is_valid_integer(value):
    """
    Check if the given value can be converted to an integer.

    Args:
        value (str): The value to check.

    Returns:
        bool: True if the value can be converted to an integer, False otherwise.
    """
    try:
        int(value)
        return True
    except ValueError:
        return False

def is_valid_float(value):
    """
    Check if the given value can be converted to a float.

    Args:
        value (str): The value to check.

    Returns:
        bool: True if the value can be converted to a float, False otherwise.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False

def is_within_range(value, min_value, max_value):
    """
    Check if the given value is within the specified range.

    Args:
        value (str): The value to check.
        min_value (float): The minimum value of the range.
        max_value (float): The maximum value of the range.

    Returns:
        bool: True if the value is within the range, False otherwise.
    """
    try:
        num = float(value)
        return min_value <= num <= max_value
    except ValueError:
        return False

def is_within_length(value, max_length):
    """
    Check if the length of the given value is within the specified maximum length.

    Args:
        value (str): The value to check.
        max_length (int): The maximum length.

    Returns:
        bool: True if the length of the value is within the maximum length, False otherwise.
    """
    return len(value) <= max_length

def is_secure_password(password):
    """
    Check if the given password meets the security requirements.

    Args:
        password (str): The password to check.

    Returns:
        bool: True if the password meets the security requirements, False otherwise.
    """
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
