"""
utils.py

Utility functions for the family tree project.
"""
def validate_input(value, expected_type, var_name="Variable", allow_none=False):
    """Validates input type and ensures it matches the expected type."""
    if value is None and not allow_none:
        raise ValueError(f"{var_name} must not be None.")
    if value is None and allow_none:
        return
    if not isinstance(value, expected_type):
        raise TypeError(f"Expected {var_name} to be {expected_type.__name__}, \
                        but got {type(value).__name__}.")
