def clamp(value, min_val=None, max_val=None):
    if max_val is not None and min_val is not None and max_val < min_val:
        raise ValueError("max_val cannot be less than min_val")

    if min_val is not None:
        value = max(value, min_val)

    if max_val is not None:
        value = min(value, max_val)

    return value
