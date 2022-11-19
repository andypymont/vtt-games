import math
from typing import Sequence, Tuple

Point = Tuple[float, float]

def hex_points(radius: float) -> Tuple[Point, ...]:
    cx = cy = radius
    return tuple(
        (
            cx + (radius * math.sin(i * 2 * math.pi / 6)),
            cy + (radius * math.cos(i * 2 * math.pi / 6)),
        ) for i in range(6)
    )