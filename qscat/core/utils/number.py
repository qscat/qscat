# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

import locale
import re


def locale_safe_float(value):
    """Convert a string to float in a locale-safe manner.
    
    This function handles both comma and dot decimal separators,
    making it work regardless of the system locale settings.
    
    Args:
        value (str): String representation of a number that may use
                    either comma or dot as decimal separator.
                    
    Returns:
        float: The numeric value as a float.
        
    Raises:
        ValueError: If the string cannot be converted to a valid float.
        TypeError: If the input is not a string or numeric type.
        
    Examples:
        >>> locale_safe_float("95.00")
        95.0
        >>> locale_safe_float("95,00") 
        95.0
        >>> locale_safe_float("1,234.56")
        1234.56
        >>> locale_safe_float("1.234,56")
        1234.56
    """
    if value is None:
        raise ValueError("Cannot convert None to float")
    
    # If already a number, return as float
    if isinstance(value, (int, float)):
        return float(value)
        
    # If not a string, try to convert to string first
    if not isinstance(value, str):
        try:
            value = str(value)
        except Exception as e:
            raise TypeError(f"Cannot convert {type(value)} to string: {e}")
    
    # Remove whitespace
    value = value.strip()
    
    if not value:
        raise ValueError("Cannot convert empty string to float")
    
    # Handle the case where the string contains both comma and dot
    # Determine which is the decimal separator based on position
    comma_pos = value.rfind(',')
    dot_pos = value.rfind('.')
    
    # If both comma and dot are present, the rightmost one is likely the decimal separator
    if comma_pos != -1 and dot_pos != -1:
        if comma_pos > dot_pos:
            # Comma is the decimal separator (e.g., "1.234,56")
            value = value.replace('.', '').replace(',', '.')
        else:
            # Dot is the decimal separator (e.g., "1,234.56")
            value = value.replace(',', '')
    elif comma_pos != -1:
        # Only comma present - check if it's a decimal separator or thousands separator
        # If there are digits after comma and they are 1-3 digits, it's likely decimal
        # If there are more than 3 digits after comma, it's likely thousands separator
        parts = value.split(',')
        if len(parts) == 2 and len(parts[1]) <= 3 and parts[1].isdigit():
            # Likely decimal separator
            value = value.replace(',', '.')
        else:
            # Likely thousands separator or invalid format
            value = value.replace(',', '')
    # If only dot present, assume it's correct as-is
    
    try:
        return float(value)
    except ValueError as e:
        raise ValueError(f"Could not convert string to float: '{value}'. {e}")


def locale_safe_int(value):
    """Convert a string to int in a locale-safe manner.
    
    This function handles both comma and dot thousand separators,
    making it work regardless of the system locale settings.
    
    Args:
        value (str): String representation of an integer that may use
                    thousands separators.
                    
    Returns:
        int: The numeric value as an integer.
        
    Raises:
        ValueError: If the string cannot be converted to a valid integer.
        TypeError: If the input is not a string or numeric type.
    """
    if value is None:
        raise ValueError("Cannot convert None to int")
    
    # If already a number, return as int
    if isinstance(value, (int, float)):
        return int(value)
        
    # If not a string, try to convert to string first
    if not isinstance(value, str):
        try:
            value = str(value)
        except Exception as e:
            raise TypeError(f"Cannot convert {type(value)} to string: {e}")
    
    # Remove whitespace
    value = value.strip()
    
    if not value:
        raise ValueError("Cannot convert empty string to int")
    
    # For integers, we need to handle thousands separators and check for decimal parts
    original_value = value
    
    # Handle the case where the string contains both comma and dot
    comma_pos = value.rfind(',')
    dot_pos = value.rfind('.')
    
    if comma_pos != -1 and dot_pos != -1:
        # Both comma and dot present
        if comma_pos > dot_pos:
            # Comma is likely the decimal separator (e.g., "1.234,56")
            decimal_part = value[comma_pos + 1:]
            if decimal_part and not all(c == '0' for c in decimal_part):
                raise ValueError(f"Cannot convert decimal number '{original_value}' to int")
            # Remove decimal part and thousands separators
            value = value[:comma_pos].replace('.', '')
        else:
            # Dot is likely the decimal separator (e.g., "1,234.56")  
            decimal_part = value[dot_pos + 1:]
            if decimal_part and not all(c == '0' for c in decimal_part):
                raise ValueError(f"Cannot convert decimal number '{original_value}' to int")
            # Remove decimal part and thousands separators
            value = value[:dot_pos].replace(',', '')
    elif comma_pos != -1:
        # Only comma present
        # For comma, check the pattern to determine if it's decimal or thousands separator
        parts = value.split(',')
        if len(parts) == 2:
            # Could be either decimal (95,00) or thousands (1,234)
            decimal_candidate = parts[1]
            if len(decimal_candidate) <= 2 and decimal_candidate.isdigit():
                # Likely decimal separator (e.g., "95,00")
                if decimal_candidate and not all(c == '0' for c in decimal_candidate):
                    raise ValueError(f"Cannot convert decimal number '{original_value}' to int")
                value = parts[0]
            elif len(decimal_candidate) == 3 and decimal_candidate.isdigit():
                # Could be thousands separator (e.g., "1,234") or decimal with 3 places
                # Check if the integer part looks like it could have thousands separator
                if len(parts[0]) >= 1:  # Simple heuristic
                    # Treat as thousands separator
                    value = value.replace(',', '')
                else:
                    # Treat as decimal - check if all zeros
                    if not all(c == '0' for c in decimal_candidate):
                        raise ValueError(f"Cannot convert decimal number '{original_value}' to int")
                    value = parts[0]
            else:
                # Multiple commas or invalid format - treat as thousands separators
                value = value.replace(',', '')
        else:
            # Multiple commas - thousands separators
            value = value.replace(',', '')
    elif dot_pos != -1:
        # Only dot present
        parts = value.split('.')
        if len(parts) == 2:
            # Could be either decimal (95.00) or thousands (1.234)
            decimal_candidate = parts[1]
            if len(decimal_candidate) <= 2:
                # Likely decimal separator (e.g., "95.00")
                if decimal_candidate and not all(c == '0' for c in decimal_candidate):
                    raise ValueError(f"Cannot convert decimal number '{original_value}' to int")
                value = parts[0]
            elif len(decimal_candidate) == 3 and decimal_candidate.isdigit():
                # Could be thousands separator
                value = value.replace('.', '')
            else:
                # Invalid format
                raise ValueError(f"Invalid number format: '{original_value}'")
        else:
            # Multiple dots - likely thousands separators (e.g., "1.234.567")
            if parts[-1] and len(parts[-1]) <= 2:
                # Last part might be decimal
                if not all(c == '0' for c in parts[-1]):
                    raise ValueError(f"Cannot convert decimal number '{original_value}' to int")
                # Remove last part and dots
                value = ''.join(parts[:-1])
            else:
                # All thousands separators
                value = value.replace('.', '')
    
    try:
        return int(value)
    except ValueError as e:
        raise ValueError(f"Could not convert string to int: '{original_value}'. {e}")