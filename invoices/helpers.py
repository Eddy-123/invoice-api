def is_convertible_to_number(s):
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False
