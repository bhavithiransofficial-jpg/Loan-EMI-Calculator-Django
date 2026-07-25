from decimal import Decimal


def format_currency(value):
    """
    Format Decimal as Indian Rupee.
    """
    return f"₹ {Decimal(value):,.2f}"