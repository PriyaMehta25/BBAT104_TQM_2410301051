import re


def required(value, label, max_len=100):
    value = str(value).strip()
    if not value:
        raise ValueError(f'{label} cannot be empty.')
    if len(value) > max_len:
        raise ValueError(f'{label} is too long.')
    return value


def year(value):
    try:
        value = int(value)
    except (TypeError, ValueError):
        raise ValueError('Year must be a number.')
    if not 1000 <= value <= 2100:
        raise ValueError('Enter a valid publication year.')
    return value


def copies(value):
    try:
        value = int(value)
    except (TypeError, ValueError):
        raise ValueError('Copies must be a number.')
    if value < 0:
        raise ValueError('Copies cannot be negative.')
    return value


def email(value):
    value = required(value, 'Email')
    if not re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+', value):
        raise ValueError('Enter a valid email address.')
    return value


def phone(value):
    value = required(value, 'Phone')
    if not value.isdigit() or len(value) != 10:
        raise ValueError('Phone must contain exactly 10 digits.')
    return value
