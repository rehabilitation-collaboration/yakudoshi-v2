"""Yakudoshi (unlucky year) age definitions and conversion utilities."""

# Yakudoshi ages in kazoedoshi (traditional Japanese age counting)
# Men: 25, 42 (taiyaku/great unlucky), 61
# Women: 19, 33 (taiyaku/great unlucky), 37, 61
YAKUDOSHI_KAZOEDOSHI = {
    "male": [25, 42, 61],
    "female": [19, 33, 37, 61],
}

# Mae-yaku (pre-unlucky) and ato-yaku (post-unlucky): ±1 year from hon-yaku
MAE_YAKU_OFFSET = -1
ATO_YAKU_OFFSET = +1


def kazoedoshi_to_mannenrei(kazoedoshi: int, offset: int = -1) -> int:
    """Convert kazoedoshi (traditional counting) to mannenrei (Western age).

    The standard conversion subtracts 1 (most people for most of the year).
    Some sources suggest subtracting 2 (before one's birthday in the year).

    Args:
        kazoedoshi: Age in traditional Japanese counting (born = 1, +1 each Jan 1).
        offset: Conversion offset. -1 (default) or -2 for sensitivity analysis.

    Returns:
        Age in Western counting (mannenrei).
    """
    return kazoedoshi + offset


def get_yakudoshi_ages(sex: str, offset: int = -1, include_mae_ato: bool = False) -> list[int]:
    """Get yakudoshi ages in mannenrei (Western age).

    Args:
        sex: "male" or "female".
        offset: Kazoedoshi-to-mannenrei conversion offset (-1 or -2).
        include_mae_ato: If True, include mae-yaku and ato-yaku years.

    Returns:
        Sorted list of yakudoshi ages in mannenrei.
    """
    if sex not in YAKUDOSHI_KAZOEDOSHI:
        raise ValueError(f"sex must be 'male' or 'female', got '{sex}'")

    hon_yaku = [kazoedoshi_to_mannenrei(k, offset) for k in YAKUDOSHI_KAZOEDOSHI[sex]]

    if not include_mae_ato:
        return sorted(hon_yaku)

    all_ages = set()
    for age in hon_yaku:
        all_ages.add(age + MAE_YAKU_OFFSET)
        all_ages.add(age)
        all_ages.add(age + ATO_YAKU_OFFSET)
    return sorted(all_ages)
