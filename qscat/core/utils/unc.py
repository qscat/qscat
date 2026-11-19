def get_unc(unc_val, default_unc):
    """Get the uncertainty as float, falling back to the default uncertainty
    if the value is missing, not a number, or not greater than 0.0.

    Args:
        unc_val (int, float, str, None): Uncertainty field value.
        default_unc (int, float, str): Default data uncertainty.

    Returns:
        float: The uncertainty value.
    """
    try:
        unc = float(unc_val)
    except (TypeError, ValueError):
        return float(default_unc)
    return unc if unc > 0.0 else float(default_unc)
