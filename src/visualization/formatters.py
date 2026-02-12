"""
Number and currency formatting utilities.
"""


def format_billions(value: float, decimals: int = 1) -> str:
    """Format a number in billions with $ prefix."""
    if abs(value) >= 1000:
        return f"${value / 1000:,.{decimals}f}T"
    elif abs(value) >= 1:
        return f"${value:,.{decimals}f}B"
    elif abs(value) >= 0.001:
        return f"${value * 1000:,.{decimals}f}M"
    else:
        return f"${value * 1_000_000:,.0f}K"


def format_number(value: float, decimals: int = 0) -> str:
    """Format a number with commas."""
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:,.{decimals}f}M"
    elif abs(value) >= 1_000:
        return f"{value / 1_000:,.{decimals}f}K"
    else:
        return f"{value:,.{decimals}f}"


def format_pct(value: float, decimals: int = 1) -> str:
    """Format a decimal as percentage."""
    return f"{value * 100:,.{decimals}f}%"


def format_ratio(value: float, decimals: int = 2) -> str:
    """Format a benefit-cost ratio."""
    return f"{value:,.{decimals}f}x"


def delta_color(value: float) -> str:
    """Return 'normal' or 'inverse' for st.metric delta_color."""
    return "normal" if value >= 0 else "inverse"
