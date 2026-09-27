"""Dimension management and portal travel logic for Overworld, Nether, and The End."""

from typing import Tuple, Optional
from textcraft.config import (
    DIMENSION_OVERWORLD, DIMENSION_NETHER, DIMENSION_END
)

DIMENSION_NAMES = {
    DIMENSION_OVERWORLD: "The Overworld",
    DIMENSION_NETHER: "The Nether",
    DIMENSION_END: "The End",
}

DIMENSION_ATMOSPHERES = {
    DIMENSION_OVERWORLD: "The breeze whispers gently across the wild lands.",
    DIMENSION_NETHER: "Heat radiates through your boots. The acrid stench of sulfur fills the air.",
    DIMENSION_END: "An unsettling silence pervades the cosmic void. Gravity feels detached and eerie.",
}

def get_portal_destination(current_dim: str, current_coords: Tuple[int, int, int]) -> Tuple[str, Tuple[int, int, int]]:
    """Calculates destination dimension and coordinates when entering a portal."""
    x, y, z = current_coords
    if current_dim == DIMENSION_OVERWORLD:
        # Overworld to Nether: scale X and Z by 1/8
        nx = max(-1000, min(1000, x // 8))
        nz = max(-1000, min(1000, z // 8))
        return DIMENSION_NETHER, (nx, 64, nz)
    elif current_dim == DIMENSION_NETHER:
        # Nether to Overworld: scale X and Z by 8
        ox = max(-8000, min(8000, x * 8))
        oz = max(-8000, min(8000, z * 8))
        return DIMENSION_OVERWORLD, (ox, 64, oz)
    elif current_dim == DIMENSION_END:
        # Exit End back to Overworld spawn
        return DIMENSION_OVERWORLD, (0, 64, 0)
    return DIMENSION_OVERWORLD, (0, 64, 0)
