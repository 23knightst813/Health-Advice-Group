# validation.py contains functions that validate user input. These functions are used in the routes to validate the input before processing it. The functions are as follows:   

# Import the re module for regular expression operations
import re

# Import the datetime module for date validation
from datetime import datetime

def is_not_empty(value):
    """
    Check if a value is not empty.

    Parameters:
        value (str): The value to check.

    Returns:
        bool: True if the value is not empty, False otherwise.
    """
    # Check if the value is not empty and does not consist of only whitespace
    return bool(value and value.strip())

def is_valid_email(email):
    """
    Validate an email address.

    Parameters:
        email (str): The email address to validate.

    Returns:
        bool: True if the email address is valid, False otherwise.
    """
    # Define a regular expression pattern for a valid email address
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    # Check if the email matches the pattern
    return re.match(pattern, email) is not None

def is_valid_date(date_str):
    """
    Validate a date string.

    Parameters:
        date_str (str): The date string to validate.

    Returns:
        bool: True if the date string is valid, False otherwise.
    """
    try:
        # Try to parse the date string using the specified format
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def is_valid_integer(value):
    """
    Validate if a value is an integer.

    Parameters:
        value (str): The value to validate.

    Returns:
        bool: True if the value is an integer, False otherwise.
    """
    try:
        # Try to convert the value to an integer
        int(value)
        return True
    except ValueError:
        return False

def is_valid_float(value):
    """
    Validate if a value is a float.

    Parameters:
        value (str): The value to validate.

    Returns:
        bool: True if the value is a float, False otherwise.
    """
    try:
        # Try to convert the value to a float
        float(value)
        return True
    except ValueError:
        return False

def is_within_range(value, min_value, max_value):
    """
    Check if a value is within a specified range.

    Parameters:
        value (str): The value to check.
        min_value (float): The minimum value of the range.
        max_value (float): The maximum value of the range.

    Returns:
        bool: True if the value is within the range, False otherwise.
    """
    try:
        # Try to convert the value to a float and check if it is within the range
        num = float(value)
        return min_value <= num <= max_value
    except ValueError:
        return False

def is_within_length(value, max_length):
    """
    Check if a value is within a specified length.

    Parameters:
        value (str): The value to check.
        max_length (int): The maximum length.

    Returns:
        bool: True if the value is within the length, False otherwise.
    """
    # Check if the length of the value is within the specified maximum length
    return len(value) <= max_length

def is_secure_password(password):
    """
    Validate if a password is secure.

    Parameters:
        password (str): The password to validate.

    Returns:
        bool: True if the password is secure, False otherwise.
    """
    # Check if the password meets the security criteria
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