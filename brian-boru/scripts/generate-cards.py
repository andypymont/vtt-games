import math
import os
from enum import Enum
from typing import Iterator, Sequence, Tuple
from xml.dom import minidom


class Colour(Enum):
    BLACK = "000000"
    CORNFLOWER_BLUE = "6495ed"
    DAFFODIL = "ffff31"
    GOLD = "ffd700"
    GREEN = "008000"
    IVORY = "fffff0"
    PALE_AQUA = "bcd4e6"
    SAND = "c2b280"
    SCARLET = "ff2400"
    SIENNA = "a0522d"
    SLATE = "708090"
    TEA_GREEN = "d0f0c0"


class Part:
    def __init__(self):
        self.height = 24
        self.width = 20

    def svg(self, doc: minidom.Document, x: int, y: int) -> minidom.Element:
        rect = doc.createElement("rect")
        rect.setAttribute("x", f"{x}")
        rect.setAttribute("y", f"{y}")
        rect.setAttribute("height", f"{self.height}")
        rect.setAttribute("width", f"{self.width}")
        rect.setAttribute("style", "fill:#000000;stroke:#00ff00;stroke-width:0.5px")
        return rect


class Path(Part):
    def __init__(self, d: str, fill: Colour = Colour.BLACK, stroke: Colour = Colour.BLACK, stroke_width: int = 0.3):
        self.d = d
        self.fill = fill
        self.stroke = stroke
        self.stroke_width = stroke_width

    def svg(self, doc: minidom.Document, x: int, y: int) -> minidom.Element:
        path = doc.createElement("path")
        path.setAttribute("d", self.d)
        path.setAttribute("style", f"fill:#{self.fill.value};stroke:#{self.stroke.value};stroke-width:{self.stroke_width}px")
        return path

class Polygon(Part):
    def __init__(self, points: str, fill: Colour = Colour.BLACK, stroke: Colour = Colour.BLACK, stroke_width: int = 0.3):
        self.points = points
        self.fill = fill
        self.stroke = stroke
        self.stroke_width = stroke_width
    
    def svg(self, doc: minidom.Document, x: int, y: int) -> minidom.Element:
        poly = doc.createElement("polygon")
        poly.setAttribute("points", self.points)
        poly.setAttribute("style", f"fill:#{self.fill.value};stroke:#{self.stroke.value};stroke-width:{self.stroke_width}px")
        return poly

class Circle(Part):
    def __init__(self, cx: int, cy: int, r: int, fill: Colour = Colour.BLACK, stroke: Colour = Colour.BLACK, stroke_width: int = 0.3):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.fill = fill
        self.stroke = stroke
        self.stroke_width = stroke_width
    
    def svg(self, doc: minidom.Document, x: int, y: int) -> minidom.Element:
        circle = doc.createElement('circle')
        circle.setAttribute("cx", f"{self.cx}")
        circle.setAttribute("cy", f"{self.cy}")
        circle.setAttribute("r", f"{self.r}")
        circle.setAttribute("style", f"fill:#{self.fill.value};stroke:#{self.stroke.value};stroke-width:{self.stroke_width}px")
        return circle

class Rect(Part):
    def __init__(self, x: int, y: int, height: int, width: int, fill: Colour = Colour.BLACK, stroke: Colour = Colour.BLACK, stroke_width: int = 0.3):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.fill = fill
        self.stroke = stroke
        self.stroke_width = stroke_width
    
    def svg(self, doc: minidom.Document, x: int, y: int) -> minidom.Element:
        rect = doc.createElement('rect')
        rect.setAttribute("x", f"{self.x}")
        rect.setAttribute("y", f"{self.y}")
        rect.setAttribute("height", f"{self.height}")
        rect.setAttribute("width", f"{self.width}")
        rect.setAttribute("style", f"fill:#{self.fill.value};stroke:#{self.stroke.value};stroke-width:{self.stroke_width}px")
        return rect

class Line(Part):
    def __init__(self, x1: int, y1: int, x2: int, y2: int, stroke: Colour = Colour.BLACK, stroke_width: int = 0.3):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.stroke = stroke
        self.stroke_width = stroke_width
    
    def svg(self, doc: minidom.Document, x: int, y: int) -> minidom.Element:
        line = doc.createElement('line')
        line.setAttribute("x1", f"{self.x1}")
        line.setAttribute("y1", f"{self.y1}")
        line.setAttribute("x2", f"{self.x2}")
        line.setAttribute("y2", f"{self.y2}")
        line.setAttribute("style", f"stroke:#{self.stroke.value};stroke-width:{self.stroke_width}px")
        return line

class Icon:
    def __init__(self, parts: Sequence[Part]):
        self.parts = parts
        self.height = 24
        self.width = 20

    def svg(self, doc: minidom.Document, x: int, y: int) -> minidom.Element:
        group = doc.createElement("g")
        group.setAttribute("transform", f"translate({x},{y})")
        for part in self.parts:
            group.appendChild(part.svg(doc, x, y))
        return group


class Digit(Icon):
    def __init__(self, parts: Sequence[str]):
        self.parts = parts
        self.height = 32
        self.width = 20


coin_base = Circle(
    cx=10,
    cy=12,
    r=10,
    fill=Colour.GOLD,
)
hex = Polygon(
    "20.0,10.0 15.0,18.66, 5.00,18.66 0.00,10.00 5.00,1.34 15.00,1.34",
    Colour.TEA_GREEN,
)
triquetra = Path(
    "m 10.0,4.52 c 1.35,1.62 2.16,3.70 2.16,5.97 0,0.88 -0.12,1.72 -0.35,2.53 -1.19,-0.22 -2.41,-0.22 -3.62,0 -0.22,-0.80 -0.35,-1.65 -0.35,-2.53 0,-2.27 0.81,-4.35 2.16,-5.97 z m -0.02,9.07 c 0.54,0 1.08,0.05 1.61,0.14 -0.37,1.0 -0.91,1.93 -1.58,2.74 -0.67,-0.81 -1.21,-1.73 -1.58,-2.73 0.52,-0.09 1.04,-0.13 1.56,-0.13 z m -2.29,0.29 c 0.41,1.16 1.03,2.21 1.81,3.13 -1.70,1.74 -4.06,2.82 -6.69,2.82 -0.54,0 -1.07,-0.05 -1.58,-0.13 0.73,-1.97 2.13,-3.72 4.09,-4.85 0.76,-0.44 1.55,-0.76 2.36,-0.96 z m 4.62,0 c 2.35,0.60 4.47,2.11 5.78,4.38 0.27,0.47 0.49,0.95 0.67,1.43 -0.51,0.08 -1.04,0.13 -1.58,0.13 -2.62,0 -4.99,-1.08 -6.69,-2.82 0.78,-0.92 1.40,-1.98 1.81,-3.13 z m 7.41,6.37 -0.22,-0.71 c -0.20,-0.56 -0.46,-1.11 -0.76,-1.65 -1.40,-2.43 -3.67,-4.06 -6.20,-4.71 0.24,-0.86 0.36,-1.76 0.36,-2.69 0,-2.49 -0.90,-4.76 -2.40,-6.52 L 10.0,3.43 9.50,3.97 C 8.01,5.73 7.10,8.01 7.10,10.49 c 0,0.93 0.13,1.83 0.36,2.68 -0.86,0.22 -1.70,0.56 -2.51,1.03 -2.15,1.24 -3.67,3.16 -4.45,5.34 l -0.22,0.71 0.72,0.16 c 0.59,0.11 1.19,0.16 1.81,0.16 2.81,0 5.35,-1.15 7.18,-3.01 1.83,1.86 4.37,3.01 7.18,3.01 0.62,0 1.22,-0.06 1.81,-0.16 z",
    fill=Colour.CORNFLOWER_BLUE,
    stroke=Colour.BLACK,
    stroke_width=0.45,
)
viking_shield = Path(
    "m 10.27,2.52 a 9.44,9.44 0 0 0 -9.71,9.44 9.44,9.44 0 1 0 18.88,0 9.44,9.44 0 0 0 -9.17,-9.44 z m -0.23,0.45 0.44,0.25 V 3.73 L 10.05,3.98 9.61,3.73 V 3.22 Z m 0.17,1.44 a 7.55,7.55 0 0 1 7.33,7.55 7.55,7.55 0 0 1 -15.11,0 7.55,7.55 0 0 1 7.77,-7.55 z M 9.65,5.39 A 6.58,6.58 0 0 0 6.44,6.42 V 17.48 a 6.58,6.58 0 0 0 3.21,1.04 V 5.39 Z m 0.87,0.02 V 18.51 A 6.58,6.58 0 0 0 13.65,17.43 V 6.49 A 6.58,6.58 0 0 0 10.52,5.41 Z M 5.58,7.10 a 6.58,6.58 0 0 0 -2.15,4.86 6.58,6.58 0 0 0 2.15,4.86 V 7.10 Z M 2.59,7.18 3.02,7.43 V 7.94 L 2.59,8.19 2.15,7.94 V 7.43 L 2.59,7.18 Z m 14.79,0 0.44,0.25 V 7.94 L 17.38,8.19 16.94,7.94 V 7.43 l 0.44,-0.25 z m -2.86,0 v 9.55 a 6.58,6.58 0 0 0 2.06,-4.78 6.58,6.58 0 0 0 -2.06,-4.77 z m 2.85,8.52 0.44,0.25 v 0.51 l -0.44,0.25 -0.44,-0.25 v -0.51 l 0.44,-0.25 z m -14.76,0.04 0.44,0.25 V 16.51 L 2.60,16.76 2.16,16.51 v -0.51 l 0.44,-0.25 z m 7.38,4.19 0.44,0.25 V 20.70 L 9.98,20.95 9.54,20.70 v -0.51 l 0.44,-0.25 z",
    Colour.SIENNA,
)


city = Icon((triquetra,))
expand = Icon(
    (
        Path(
            "m 12.65,10.76 2.73,-2.74 -1.10,-1.09 -1.10,-1.09 3.28,0 3.28,0 0.01,3.27 0.01,3.27 -1.09,-1.08 -1.09,-1.08 -2.72,2.74 -2.72,2.74 -0.63,-0.62 c -0.35,-0.34 -0.84,-0.83 -1.10,-1.08 L 9.92,13.51 z"
        ),
        triquetra,
        Circle(
            cx=14.11,
            cy=16.54,
            r=5.25,
            fill=Colour.GOLD,
        ),
        Path(
            "m 15.95,13.69 q 0,0.17 -0.10,0.28 -0.10,0.10 -0.35,0.10 H 13.50 l -0.29,1.66 q 0.25,-0.06 0.47,-0.08 0.23,-0.03 0.44,-0.03 0.49,0 0.88,0.15 0.38,0.15 0.63,0.40 0.26,0.26 0.38,0.60 0.13,0.35 0.13,0.76 0,0.50 -0.18,0.91 -0.17,0.41 -0.48,0.70 -0.30,0.29 -0.72,0.44 -0.41,0.15 -0.90,0.15 -0.28,0 -0.54,-0.06 -0.25,-0.05 -0.48,-0.15 -0.22,-0.09 -0.41,-0.21 -0.19,-0.12 -0.34,-0.25 l 0.24,-0.34 q 0.08,-0.11 0.21,-0.11 0.09,0 0.20,0.07 0.11,0.07 0.27,0.15 0.16,0.08 0.37,0.15 0.22,0.07 0.51,0.07 0.33,0 0.60,-0.10 0.27,-0.10 0.46,-0.30 0.19,-0.20 0.29,-0.47 0.10,-0.27 0.10,-0.61 0,-0.30 -0.09,-0.54 -0.08,-0.24 -0.26,-0.41 -0.17,-0.17 -0.43,-0.26 -0.26,-0.09 -0.61,-0.09 -0.24,0 -0.50,0.04 -0.26,0.04 -0.52,0.13 l -0.50,-0.15 0.51,-2.96 h 3.00 z"
        )
    )
)
marriage = Icon(
    (
        Rect(
            x=0,
            y=4,
            height=12,
            width=20,
            fill=Colour.SAND,
        ),
        Line(0, 4, 10, 10),
        Line(10, 10, 20, 4),
        Path(
            "m 10.34,13.81 C 10.07,13.78 9.90,13.69 9.67,13.48 9.34,13.16 9.02,13.08 8.35,13.14 8.16,13.16 8.13,13.16 8.03,13.14 7.70,13.09 7.45,12.89 7.35,12.59 7.32,12.52 7.32,12.48 7.32,12.39 7.32,12.19 7.37,12.06 7.53,11.88 7.76,11.62 7.86,11.35 7.85,11.07 7.83,10.76 7.69,10.49 7.39,10.21 7.23,10.06 7.19,10.00 7.18,9.87 7.16,9.62 7.38,9.33 7.69,9.18 7.79,9.14 7.87,9.11 8.05,9.07 8.31,9.01 8.58,8.90 8.92,8.72 c 0.59,-0.31 0.70,-0.35 0.97,-0.42 0.34,-0.09 0.61,-0.08 0.81,0.02 0.05,0.03 0.14,0.11 0.34,0.30 0.44,0.44 0.53,0.48 0.97,0.50 0.28,0.01 0.34,0.02 0.46,0.08 0.21,0.10 0.32,0.31 0.30,0.54 -0.01,0.12 -0.04,0.21 -0.15,0.44 -0.18,0.38 -0.22,0.58 -0.15,0.80 0.01,0.04 0.05,0.11 0.08,0.15 0.18,0.26 0.20,0.31 0.22,0.46 0.01,0.08 0.01,0.11 0,0.19 -0.05,0.24 -0.20,0.42 -0.44,0.52 -0.17,0.07 -0.25,0.12 -0.34,0.20 -0.14,0.13 -0.23,0.27 -0.25,0.54 -0.04,0.10 -0.09,0.19 -0.10,0.22 -0.17,0.28 -0.51,0.48 -0.90,0.53 -0.12,0.01 -0.15,0.01 -0.28,0 z m 1.76,-0.26 c -0.08,-0.04 -0.12,-0.09 -0.14,-0.19 -0.04,-0.16 0.08,-0.36 0.27,-0.46 0.06,-0.03 0.08,-0.03 0.19,-0.03 0.14,0 0.17,0.01 0.24,0.08 0.05,0.05 0.07,0.09 0.07,0.16 0,0.09 -0.04,0.18 -0.15,0.28 -0.12,0.12 -0.25,0.19 -0.37,0.19 -0.05,0 -0.09,-0.01 -0.12,-0.02 z",
            Colour.SCARLET,
            Colour.SCARLET,
        )
    )
)
coin = Icon(
    (
        coin_base,
        Path(
            "m 11.02,4.19 v 6.77 h 6.77 v 2.07 h -6.77 v 6.77 H 8.98 V 13.03 H 2.21 V 10.97 H 8.98 V 4.19 z",
            Colour.GREEN,
        )
    )
)
pay = Icon(
    (
        coin_base,
        Path(
            "M 19.08,2.26 12.04,11.74 19.45,21.74 H 15.67 L 10.0,14.09 4.33,21.74 H 0.55 L 8.12,11.55 1.19,2.26 h 3.78 l 5.17,6.94 5.17,-6.94 z",
        )
    )
)
viking = Icon(
    (
        Path(
            "m 11.0,2.77 -1.38,2.11 3.19,2.06 2.22,5.15 c 0.22,-0.10 0.53,-0.27 0.87,-0.51 0.51,-0.35 1.08,-0.83 1.61,-1.37 0.53,-0.54 1.00,-1.13 1.30,-1.70 0.26,-0.50 0.39,-0.98 0.36,-1.39 L 14.11,4.79 Z",
            Colour.SLATE,
        ),
        Path(
            "M 9.66,5.76 C 6.35,10.34 4.10,14.76 0.84,19.86 c 0,0 0,0 0.01,0.02 0.01,0.04 0.06,0.14 0.14,0.23 0.16,0.20 0.45,0.45 0.77,0.66 0.31,0.20 0.66,0.37 0.91,0.43 0.13,0.03 0.23,0.04 0.27,0.03 0.01,0 0.01,0 0.02,0 0.88,-1.35 1.27,-1.95 1.92,-4.39 l 0.01,-0.05 0.03,-0.04 c 2.41,-3.89 3.38,-6.25 6.17,-10.06 z",
            Colour.SIENNA,
        )

    )
)
remove_viking = Icon(
    (
        viking_shield,
        Path(
            "M 19.08,2.26 12.04,11.74 19.45,21.74 H 15.67 L 10.0,14.09 4.33,21.74 H 0.55 L 8.12,11.55 1.19,2.26 h 3.78 l 5.17,6.94 5.17,-6.94 z",
        ),
    )
)
renown = Icon(
    (
        Path(
            "m 10.00,2.91 c -0.94,0 -2.77,4.60 -3.53,5.15 C 5.71,8.61 0.77,8.93 0.48,9.83 0.19,10.72 4.00,13.88 4.29,14.77 4.58,15.66 3.36,20.46 4.12,21.02 4.87,21.57 9.06,18.92 10,18.92 c 0.94,0 5.13,2.64 5.88,2.09 0.76,-0.55 -0.46,-5.35 -0.17,-6.24 C 16.00,13.88 19.81,10.72 19.52,9.83 19.23,8.93 14.29,8.61 13.53,8.06 12.77,7.51 10.94,2.91 10.00,2.91 Z",
            Colour.GOLD
        ),
    )
)
church = Icon(
    (
        Path(
            "M 8.41,16.56 V 9.88 H 5.44 2.47 V 8.30 6.73 h 2.97 2.97 l 0.01,-2.98 0.01,-2.98 1.56,-0.01 1.56,-0.01 0.01,2.98 0.01,2.98 2.98,0.01 2.98,0.01 v 1.57 1.57 h -2.99 -2.99 v 6.68 6.68 H 9.98 8.41 Z",
            Colour.SIENNA
        ),
    )
)
digits = {
    0: Digit(
        (
            Path(
                "m 18.32,16.02 q 0,3.01 -0.66,5.22 -0.64,2.19 -1.76,3.63 -1.12,1.44 -2.66,2.14 -1.52,0.70 -3.26,0.70 -1.76,0 -3.28,-0.70 Q 5.20,26.30 4.08,24.86 2.96,23.42 2.32,21.23 1.68,19.02 1.68,16.02 1.68,13.01 2.32,10.80 2.96,8.59 4.08,7.15 q 1.12,-1.46 2.62,-2.16 1.52,-0.70 3.28,-0.70 1.74,0 3.26,0.70 1.54,0.70 2.66,2.16 1.12,1.44 1.76,3.65 0.66,2.21 0.66,5.22 z m -2.96,0 q 0,-2.62 -0.45,-4.40 -0.43,-1.79 -1.18,-2.88 -0.74,-1.09 -1.71,-1.55 -0.98,-0.48 -2.03,-0.48 -1.06,0 -2.03,0.48 -0.98 0.46 -1.71,1.55 -0.74,1.09 -1.18,2.88 -0.43,1.78 -0.43,4.40 0,2.62 0.43,4.40 0.45,1.78 1.18,2.86 0.74,1.09 1.71,1.57 0.98,0.46 2.03,0.46 1.06,0 2.03,-0.46 0.98,-0.48 1.71,-1.57 0.75,-1.09 1.18,-2.86 0.45,-1.78 0.45,-4.40 z"
            ),
        )
    ),
    1: Digit(
        (
            Path(
                "m 4.72,25.30 H 9.63 V 9.66 q 0,-0.67 0.05,-1.42 L 5.60,11.74 Q 5.39,11.92 5.18,11.97 4.98,12.00 4.80,11.97 4.62,11.94 4.46,11.84 4.32,11.74 4.24,11.63 L 3.34,10.40 10.18,4.50 h 2.32 V 25.30 h 4.51 v 2.18 H 4.72 Z"
            ),
        )
    ),
    2: Digit(
        (
            Path(
                "m 10.18,4.29 q 1.46,0 2.72,0.43 1.26,0.43 2.19,1.26 0.93,0.82 1.46,2.00 0.53,1.18 0.53,2.69 0,1.28 -0.38,2.38 -0.38,1.09 -1.04,2.08 -0.66,0.99 -1.52,1.94 -0.85,0.94 -1.81,1.90 l -6.05,6.18 q 0.64,-0.18 1.30,-0.27 0.66,-0.11 1.26,-0.11 h 7.68 q 0.46,0 0.74,0.27 0.27,0.27 0.27,0.70 v 1.73 H 2.22 v -0.98 q 0,-0.30 0.13,-0.62 0.13,-0.32 0.40,-0.59 l 7.34,-7.38 q 0.91,-0.93 1.66,-1.78 0.75,-0.86 1.28,-1.73 0.53,-0.86 0.82,-1.74 0.29,-0.90 0.29,-1.90 0,-1.01 -0.32,-1.76 -0.32,-0.77 -0.88,-1.26 -0.54,-0.50 -1.30,-0.74 -0.75,-0.26 -1.62,-0.26 -0.88,0 -1.62,0.26 -0.74,0.26 -1.312,0.72 -0.56,0.45 -0.94,1.07 -0.38,0.62 -0.54,1.38 -0.19,0.56 -0.53,0.75 -0.32,0.18 -0.91,0.10 L 2.69,10.75 q 0.22,-1.57 0.86,-2.77 0.66,-1.22 1.63,-2.03 0.99,-0.82 2.26,-1.23 1.26,-0.43 2.74,-0.43 z"
            ),
        )
    ),
    3: Digit(
        (
            Path(
                "m 10.29,4.29 q 1.46,0 2.69,0.42 1.23,0.42 2.11,1.18 0.90,0.77 1.39,1.86 0.50,1.09 0.50,2.42 0,1.09 -0.29,1.95 -0.27,0.85 -0.80,1.50 -0.51,0.64 -1.25,1.09 -0.74,0.45 -1.65,0.72 2.24,0.59 3.36,1.98 1.14,1.39 1.14,3.49 0,1.58 -0.61,2.85 -0.59,1.26 -1.63,2.16 -1.04,0.88 -2.43,1.36 -1.38,0.46 -2.96,0.46 -1.82,0 -3.12,-0.45 Q 5.44,26.82 4.54,26.02 3.65,25.22 3.07,24.13 2.50,23.02 2.10,21.74 l 1.23,-0.51 q 0.48,-0.21 0.93,-0.11 0.46,0.10 0.67,0.53 0.21,0.45 0.51,1.07 0.32,0.62 0.86,1.20 0.54,0.58 1.38,0.98 0.85,0.40 2.14,0.40 1.20,0 2.10,-0.38 0.91,-0.40 1.50,-1.02 0.61,-0.62 0.91,-1.39 0.30,-0.77 0.30,-1.52 0,-0.93 -0.24,-1.70 -0.24,-0.77 -0.90,-1.33 -0.66,-0.56 -1.81,-0.88 -1.14,-0.32 -2.93,-0.32 v -2.06 q 1.47,-0.02 2.50,-0.32 1.04,-0.30 1.68,-0.83 0.66,-0.53 0.94,-1.26 0.30,-0.74 0.30,-1.63 0,-0.99 -0.32,-1.73 -0.30,-0.74 -0.85,-1.22 -0.54,-0.48 -1.30,-0.72 -0.74,-0.24 -1.60,-0.24 -0.86,0 -1.62,0.26 -0.74,0.26 -1.31,0.72 -0.56,0.45 -0.94,1.07 Q 5.87,9.41 5.71,10.16 5.50,10.72 5.18,10.91 4.88,11.09 4.29,11.01 L 2.80,10.75 q 0.22,-1.57 0.86,-2.77 0.64,-1.22 1.62,-2.03 0.99,-0.82 2.26,-1.23 1.28,-0.43 2.75,-0.43 z"
            ),
        )
    ),
    4: Digit(
        (
            Path(
                "m 14.90,19.20 h 3.47 v 1.63 q 0,0.26 -0.16,0.43 -0.14,0.18 -0.46,0.18 h -2.85 v 6.03 H 12.40 V 21.44 H 2.22 q -0.32,0 -0.56,-0.18 Q 1.44,21.07 1.38,20.80 L 1.09,19.34 12.24,4.54 h 2.66 z M 12.40,9.74 q 0,-0.42 0.02,-0.90 0.03,-0.50 0.11,-1.01 L 4.18,19.20 H 12.40 z"
            ),
        )
    ),
    5: Digit(
        (
            Path(
                "m 16.43,5.79 q 0,0.61 -0.38,1.01 -0.37,0.38 -1.28,0.38 h -7.20 L 6.51,13.20 q 0.91,-0.21 1.71,-0.29 0.82,-0.10 1.58,-0.10 1.79,0 3.17,0.53 1.38,0.53 2.29,1.46 0.93,0.93 1.39,2.19 0.48,1.26 0.48,2.75 0,1.82 -0.64,3.30 -0.62,1.47 -1.74,2.53 -1.10,1.04 -2.61,1.60 -1.50,0.56 -3.25,0.56 -1.01,0 -1.94,-0.21 Q 6.03,27.33 5.22,26.99 4.42,26.66 3.73,26.22 3.04,25.79 2.51,25.31 l 0.88,-1.22 Q 3.68,23.68 4.14,23.68 q 0.32,0 0.72,0.26 0.40,0.24 0.98,0.54 0.58,0.30 1.34,0.56 0.78,0.24 1.86,0.24 1.20,0 2.16,-0.38 0.96,-0.38 1.65,-1.09 0.69,-0.72 1.06,-1.71 0.37,-0.99 0.37,-2.22 0,-1.07 -0.32,-1.94 -0.30,-0.86 -0.94,-1.47 -0.62,-0.61 -1.57,-0.94 -0.94,-0.34 -2.21,-0.34 -0.86,0 -1.81,0.14 -0.93,0.14 -1.90,0.46 L 3.73,15.26 5.57,4.54 h 10.86 z"
            ),
        )
    ),
    6: Digit(
        (
            Path(
                "m 8.30,13.14 q -0.32,0.38 -0.59,0.75 -0.27,0.37 -0.54,0.72 0.82,-0.56 1.79,-0.86 0.99,-0.32 2.14,-0.32 1.39,0 2.62,0.46 1.23,0.45 2.14,1.33 0.93,0.86 1.47,2.14 0.54,1.26 0.54,2.90 0,1.58 -0.58,2.94 -0.58,1.36 -1.62,2.37 -1.02,1.01 -2.48,1.58 -1.44,0.58 -3.18,0.58 -1.73,0 -3.14,-0.54 -1.41,-0.56 -2.40,-1.57 -0.98,-1.02 -1.52,-2.46 -0.53,-1.46 -0.53,-3.25 0,-1.50 0.66,-3.20 0.67,-1.71 2.13,-3.65 l 5.82,-7.82 q 0.22,-0.29 0.61,-0.48 0.40,-0.21 0.91,-0.21 h 2.53 z M 5.18,20.40 q 0,1.10 0.32,2.02 0.32,0.91 0.93,1.57 0.62,0.66 1.50,1.02 0.90,0.35 2.03,0.35 1.15,0 2.08,-0.37 0.94,-0.37 1.60,-1.02 0.67,-0.66 1.02,-1.55 0.37,-0.90 0.37,-1.95 0,-1.12 -0.35,-2.02 Q 14.34,17.54 13.68,16.91 13.04,16.27 12.14,15.94 11.25,15.60 10.18,15.60 9.02,15.60 8.10,16.00 7.17,16.38 6.51,17.06 5.87,17.71 5.52,18.59 5.18,19.46 5.18,20.40 z"
            ),
        )
    ),
    7: Digit(
        (
            Path(
                "m 18.02,4.54 v 1.28 q 0,0.54 -0.13,0.90 -0.11,0.35 -0.22,0.59 L 8.16,26.46 Q 7.95,26.88 7.58,27.18 7.22,27.47 6.61,27.47 H 4.56 L 14.19,8.56 q 0.21,-0.40 0.42,-0.74 0.22,-0.34 0.50,-0.64 H 3.14 q -0.27,0 -0.48,-0.21 -0.21,-0.22 -0.21,-0.50 v -1.94 z"
            ),
        )
    ),
    8: Digit(
        (
            Path(
                "M 10.00,27.73 Q 8.29,27.73 6.86,27.28 5.44,26.82 4.42,25.97 3.39,25.12 2.83,23.92 2.27,22.70 2.27,21.20 q 0,-2.21 1.15,-3.63 1.15,-1.44 3.30,-2.05 -1.81,-0.67 -2.74,-2.00 -0.91,-1.34 -0.91,-3.20 0,-1.26 0.50,-2.37 0.50,-1.10 1.41,-1.92 0.91,-0.82 2.18,-1.28 1.28,-0.46 2.85,-0.46 1.55,0 2.83,0.46 1.28,0.46 2.19,1.28 0.91,0.82 1.41,1.92 0.50,1.10 0.50,2.37 0,1.86 -0.93,3.20 -0.93,1.33 -2.72,2.00 2.14,0.61 3.30,2.05 1.15,1.42 1.15,3.63 0,1.50 -0.58,2.72 -0.56,1.20 -1.58,2.05 -1.01,0.85 -2.43,1.31 -1.42,0.45 -3.14,0.45 z m 0,-2.27 q 1.12,0 2.00,-0.30 0.90,-0.32 1.50,-0.88 0.62,-0.58 0.94,-1.36 0.34,-0.80 0.34,-1.76 0,-1.18 -0.40,-2.02 Q 14.00,18.29 13.33,17.76 12.67,17.23 11.81,16.99 10.94,16.74 10.00,16.74 9.06,16.74 8.19,16.99 7.33,17.23 6.66,17.76 6.00,18.29 5.60,19.14 q -0.38,0.83 -0.38,2.02 0,0.96 0.32,1.76 0.34,0.78 0.94,1.36 0.62,0.56 1.50,0.88 0.90,0.30 2.02,0.30 z m 0,-11.01 q 1.12,0 1.904,-0.34 0.80,-0.35 1.30,-0.91 0.50,-0.58 0.72,-1.31 0.22,-0.74 0.22,-1.52 0,-0.80 -0.27,-1.50 -0.26,-0.70 -0.78,-1.23 -0.51,-0.53 -1.30,-0.83 -0.77,-0.30 -1.79,-0.30 -1.02,0 -1.81,0.30 -0.77,0.30 -1.30,0.83 -0.51,0.53 -0.78,1.23 -0.26,0.70 -0.26,1.50 0,0.78 0.22,1.52 0.22,0.74 0.72,1.31 0.50,0.56 1.28,0.91 0.80,0.34 1.92,0.34 z"
            ),
        )
    ),
    9: Digit(
        (
            Path(
                "m 11.90,18.34 q 0.35,-0.46 0.66,-0.88 0.30,-0.42 0.58,-0.83 -0.88,0.70 -1.98,1.07 -1.10,0.37 -2.34,0.37 -1.30,0 -2.46,-0.43 Q 5.20,17.20 4.32,16.37 3.44,15.52 2.91,14.30 2.40,13.07 2.40,11.49 q 0,-1.50 0.56,-2.82 0.56,-1.31 1.57,-2.29 1.01,-0.98 2.40,-1.54 1.39,-0.56 3.06,-0.56 1.65,0 2.99,0.54 1.34,0.54 2.30,1.52 0.96,0.98 1.47,2.34 Q 17.28,10.05 17.28,11.70 q 0,0.99 -0.19,1.89 -0.18,0.88 -0.53,1.74 -0.34,0.85 -0.83,1.70 -0.50,0.83 -1.12,1.71 L 9.02,26.80 q -0.21,0.30 -0.59,0.50 -0.38,0.18 -0.88,0.18 H 4.93 Z m 2.64,-6.98 q 0,-1.07 -0.35,-1.94 -0.34,-0.88 -0.94,-1.49 -0.61,-0.61 -1.46,-0.93 -0.83,-0.34 -1.84,-0.34 -1.06,0 -1.92,0.35 -0.86,0.34 -1.49,0.94 -0.62,0.61 -0.96,1.46 Q 5.25,10.27 5.25,11.28 q 0,1.09 0.30,1.95 0.32,0.85 0.90,1.44 0.59,0.59 1.42,0.90 0.85,0.30 1.89,0.30 1.15,0 2.03,-0.37 0.90,-0.38 1.50,-1.01 0.61,-0.62 0.93,-1.44 0.32,-0.82 0.32,-1.70 z"
            ),
        )
    ),
}


class Card:
    def __init__(self, colour: Colour):
        self.colour = colour
        self.height = 148
        self.width = 100

    @property
    def filename(self) -> str:
        raise NotImplementedError
    
    @classmethod
    def position(
        cls, icon: Icon, gsw: int, gsh: int, x: int, y: int, x_offset: int = 0
    ) -> Tuple[int, int]:
        x_diff = (gsw - icon.width) // 2
        y_diff = (gsh - icon.height) // 2
        return [(gsw * x) + x_diff + x_offset, (gsh * y) + y_diff]

    def elements(self, doc: minidom.Document) -> Iterator[minidom.Element]:
        for element in []:
            yield element

    def svg(self) -> minidom.Element:
        doc = minidom.Document()

        svg = doc.createElement("svg")
        svg.setAttribute("xmlns", "http://www.w3.org/2000/svg")
        svg.setAttribute("height", f"{self.height}")
        svg.setAttribute("width", f"{self.width}")
        svg.setAttribute("viewbox", f"0 0 {self.width} {self.height}")

        rect = doc.createElement("rect")
        rect.setAttribute("x", "0")
        rect.setAttribute("y", "0")
        rect.setAttribute("height", f"{self.height}")
        rect.setAttribute("width", f"{self.width}")
        rect.setAttribute(
            "style", f"fill:#{self.colour.value};stroke:#000000;stroke-width:0.5px"
        )
        svg.appendChild(rect)

        for element in self.elements(doc):
            svg.appendChild(element)

        return svg

    def render(self) -> str:
        return self.svg().toprettyxml()


class CardBack(Card):
    def __init__(self, colour: Colour, deckname: str):
        super().__init__(colour)
        self.deckname = deckname
    
    @property
    def filename(self) -> str:
        return f"card-{self.deckname}-back.svg"


class ActionCard(Card):
    def __init__(self, number: int, colour: Colour, rows: Sequence[Sequence[Icon]]):
        super().__init__(colour)
        self.number = number
        self.rows = rows

    @property
    def filename(self) -> str:
        return f"card-action-{self.number:02}.svg"

    def divider(self, doc: minidom.Document, y: int) -> minidom.Element:
        return Line(0, y, self.width, y, Colour.BLACK, 1).svg(doc, 0, 0)

    def elements(self, doc: minidom.Document) -> Iterator[minidom.Element]:
        # calculate width and height of grid sections
        gsw = self.width // 4
        gsh = self.height // 4

        # dividers:
        yield self.divider(doc, gsh * 2)
        if len(self.rows) > 2:
            yield self.divider(doc, gsh * 3)

        # card number:
        if self.number < 10:
            digit = digits[self.number]
            yield digit.svg(doc, *self.position(digit, gsw, gsh, 0, 0))
        else:
            first = digits[self.number // 10]
            yield first.svg(doc, *self.position(first, gsw, gsh, 0, 0))
            second = digits[self.number % 10]
            yield second.svg(doc, *self.position(second, gsw, gsh, 1, 0, -8))

        # rows of icons:
        for y, row in enumerate(self.rows):
            x_offset = gsw * (4 - len(row)) // 2
            for x, icon in enumerate(row):
                yield icon.svg(doc, *self.position(icon, gsw, gsh, x, y + 1, x_offset))


class MarriageCard(Card):
    def __init__(self, name: str, icon_rows: Sequence[Sequence[Icon]]):
        super().__init__(Colour.DAFFODIL)
        self.name = name
        self.icon_rows = icon_rows
    
    @property
    def filename(self) -> str:
        return f"card-marriage-{self.name.lower()}.svg"

    def elements(self, doc: minidom.Document) -> Iterator[minidom.Element]:
        # calculate width and height of grid sections
        gsw = self.width // 4
        gsh = self.height // 4

        # icons
        for y, row in enumerate(self.icon_rows):
            x_offset = gsw * (4 - len(row)) // 2
            for x, icon in enumerate(row):
                yield icon.svg(doc, *self.position(icon, gsw, gsh, x, 1 + y, x_offset))



wreath = Path(
    "M 5.91,1.18 C 5.04,1.46 4.36,1.77 3.52,2.38 3.41,2.49 3.30,2.60 3.19,2.70 c 0.01,0.03 0.03,0.06 0.06,0.11 0.05,0.09 0.14,0.20 0.25,0.31 C 3.33,3.40 3.17,3.68 3.03,3.95 2.84,3.80 2.68,3.63 2.55,3.44 2.17,3.92 1.83,4.42 1.53,4.96 c 0.02,0.08 0.08,0.17 0.19,0.29 C 1.85,5.39 2.06,5.54 2.30,5.66 2.20,5.97 2.11,6.27 2.04,6.57 1.67,6.41 1.33,6.19 1.06,5.91 0.77,6.60 0.54,7.33 0.40,8.08 0.46,8.21 0.58,8.32 0.76,8.43 1.01,8.60 1.38,8.74 1.77,8.82 1.77,9.14 1.78,9.45 1.81,9.77 1.24,9.69 0.69,9.51 0.25,9.21 c 0,0 -0.01,0 -0.01,0 -0.07,0.78 -0.04,1.54 0.05,2.29 0.12,0.17 0.31,0.30 0.59,0.40 0.37,0.13 0.87,0.17 1.38,0.12 0.10,0.30 0.21,0.60 0.34,0.90 -0.70,0.10 -1.41,0.08 -2.02,-0.13 -0.02,-0.01 -0.03,-0.01 -0.05,-0.02 0.20,0.77 0.48,1.51 0.84,2.21 0.18,0.14 0.42,0.21 0.73,0.23 0.46,0.03 1.05,-0.09 1.62,-0.32 0.18,0.26 0.38,0.52 0.59,0.76 -0.73,0.33 -1.51,0.53 -2.24,0.49 0.50,0.73 1.08,1.39 1.74,1.98 0.21,0.07 0.46,0.07 0.77,0.01 0.48,-0.09 1.04,-0.37 1.55,-0.75 0,0 0,0 0,0 0.26,0.20 0.52,0.39 0.79,0.56 -0.60,0.49 -1.28,0.88 -1.97,1.06 0.58,0.39 1.20,0.73 1.86,1.01 0.25,0.02 0.51,-0.05 0.81,-0.19 0.38,-0.19 0.79,-0.51 1.15,-0.91 0.85,0.34 1.73,0.56 2.62,0.64 l 0.09,-0.93 c -0.71,-0.07 -1.42,-0.24 -2.12,-0.50 0.34,-0.55 0.58,-1.15 0.64,-1.67 0.06,-0.45 0,-0.80 -0.19,-1.07 -0.40,-0.08 -0.79,-0.20 -1.16,-0.35 -0.01,0.32 -0.08,0.65 -0.21,0.95 -0.19,0.45 -0.47,0.89 -0.82,1.28 C 7.34,17.10 7.08,16.92 6.82,16.73 7.15,16.37 7.42,15.99 7.57,15.62 7.76,15.16 7.78,14.80 7.60,14.49 7.21,14.24 6.85,13.95 6.52,13.63 6.43,13.84 6.31,14.05 6.17,14.23 5.89,14.59 5.54,14.91 5.14,15.17 4.94,14.94 4.74,14.70 4.56,14.44 4.91,14.21 5.22,13.94 5.43,13.67 5.68,13.34 5.79,13.05 5.75,12.77 5.50,12.44 5.28,12.09 5.08,11.72 4.96,11.85 4.83,11.98 4.70,12.08 4.36,12.34 3.96,12.54 3.53,12.68 3.40,12.40 3.28,12.11 3.18,11.81 3.55,11.69 3.88,11.53 4.13,11.34 4.41,11.13 4.57,10.92 4.60,10.68 4.45,10.29 4.33,9.87 4.23,9.44 4.14,9.50 4.04,9.54 3.95,9.58 3.57,9.73 3.16,9.80 2.74,9.82 2.70,9.51 2.68,9.20 2.68,8.89 3.03,8.87 3.35,8.82 3.60,8.71 3.83,8.63 3.98,8.53 4.07,8.41 4.02,7.92 4.00,7.43 4.03,6.92 c -0.03,0.01 -0.06,0.01 -0.10,0.01 C 3.60,6.97 3.26,6.94 2.91,6.87 2.98,6.57 3.07,6.27 3.17,5.97 3.41,6.01 3.64,6.03 3.83,6.01 3.96,5.99 4.06,5.97 4.13,5.94 4.20,5.49 4.30,5.06 4.43,4.64 4.22,4.60 4.01,4.54 3.82,4.45 3.96,4.18 4.11,3.90 4.28,3.63 c 0.12,0.05 0.23,0.08 0.33,0.10 0.06,0.01 0.10,0.01 0.14,0.01 C 4.84,3.51 4.95,3.29 5.07,3.07 5.36,2.48 5.68,1.86 5.91,1.18 Z m 12.17,0 c 0.23,0.68 0.55,1.30 0.85,1.89 0.11,0.22 0.22,0.44 0.31,0.68 0.04,0 0.08,-0.01 0.14,-0.01 0.10,-0.02 0.21,-0.05 0.33,-0.10 0.17,0.27 0.32,0.55 0.47,0.82 -0.20,0.09 -0.40,0.16 -0.61,0.19 0.13,0.42 0.23,0.85 0.30,1.30 0.07,0.03 0.17,0.06 0.30,0.07 0.19,0.02 0.42,0.01 0.66,-0.04 0.10,0.30 0.18,0.60 0.25,0.90 -0.34,0.07 -0.69,0.10 -1.01,0.07 -0.03,0 -0.07,-0.01 -0.10,-0.01 0.03,0.50 0.01,1.00 -0.04,1.49 0.09,0.12 0.24,0.22 0.47,0.31 0.25,0.10 0.57,0.16 0.92,0.17 0,0.31 -0.02,0.63 -0.05,0.93 -0.42,-0.02 -0.84,-0.09 -1.21,-0.24 -0.10,-0.04 -0.20,-0.09 -0.29,-0.14 -0.09,0.43 -0.22,0.84 -0.37,1.24 0.04,0.24 0.19,0.44 0.47,0.66 0.24,0.19 0.58,0.35 0.95,0.47 -0.10,0.30 -0.22,0.59 -0.35,0.87 -0.43,-0.14 -0.83,-0.34 -1.16,-0.60 -0.14,-0.11 -0.27,-0.23 -0.38,-0.36 -0.20,0.37 -0.43,0.72 -0.67,1.05 -0.04,0.28 0.07,0.57 0.32,0.90 0.21,0.27 0.51,0.54 0.87,0.78 -0.18,0.25 -0.38,0.50 -0.59,0.73 -0.40,-0.27 -0.75,-0.58 -1.02,-0.94 -0.14,-0.19 -0.26,-0.39 -0.35,-0.60 -0.33,0.32 -0.70,0.61 -1.08,0.86 -0.18,0.31 -0.16,0.68 0.03,1.14 0.15,0.36 0.41,0.75 0.74,1.11 -0.25,0.19 -0.51,0.37 -0.78,0.53 -0.35,-0.39 -0.64,-0.83 -0.82,-1.28 -0.13,-0.30 -0.20,-0.63 -0.21,-0.95 -0.37,0.15 -0.76,0.27 -1.17,0.35 -0.19,0.26 -0.25,0.61 -0.19,1.07 0.07,0.51 0.30,1.11 0.65,1.67 -0.70,0.26 -1.41,0.43 -2.12,0.50 l 0.09,0.93 c 0.89,-0.08 1.77,-0.30 2.62,-0.64 0.36,0.40 0.77,0.72 1.15,0.91 0.30,0.15 0.57,0.22 0.81,0.19 0.66,-0.27 1.28,-0.61 1.86,-1.01 -0.69,-0.18 -1.37,-0.56 -1.97,-1.06 0.27,-0.17 0.54,-0.36 0.79,-0.56 0.51,0.38 1.07,0.65 1.55,0.75 0.30,0.06 0.55,0.06 0.76,-0.01 0.66,-0.59 1.24,-1.25 1.74,-1.98 -0.73,0.05 -1.52,-0.15 -2.25,-0.49 0.21,-0.24 0.40,-0.50 0.59,-0.76 0.56,0.23 1.15,0.35 1.62,0.32 0.32,-0.02 0.56,-0.09 0.73,-0.23 0.36,-0.70 0.64,-1.44 0.84,-2.21 -0.02,0.01 -0.03,0.01 -0.05,0.02 -0.62,0.21 -1.33,0.24 -2.02,0.13 0.13,-0.29 0.24,-0.59 0.34,-0.90 0.51,0.05 1.01,0.01 1.38,-0.12 0.29,-0.10 0.48,-0.22 0.60,-0.40 0.10,-0.74 0.12,-1.51 0.05,-2.29 0,0 0,0 -0.01,0 -0.45,0.29 -0.99,0.47 -1.56,0.56 0.03,-0.31 0.04,-0.63 0.04,-0.95 0.39,-0.08 0.76,-0.22 1.01,-0.28 C 23.42,8.32 23.54,8.21 23.60,8.08 23.46,7.33 23.23,6.60 22.94,5.91 22.67,6.19 22.33,6.41 21.96,6.57 21.89,6.27 21.80,5.97 21.70,5.66 21.94,5.54 22.15,5.39 22.28,5.25 22.39,5.13 22.45,5.04 22.47,4.96 22.17,4.42 21.83,3.92 21.45,3.44 21.32,3.63 21.16,3.80 20.97,3.95 20.83,3.68 20.68,3.40 20.50,3.12 c 0.10,-0.10 0.20,-0.22 0.25,-0.31 0.03,-0.05 0.05,-0.08 0.06,-0.11 C 20.70,2.60 20.59,2.49 20.48,2.38 19.64,1.77 18.96,1.46 18.09,1.18 Z",
    fill=Colour.GREEN,
)
vp_icons = {
    2: Icon((
        wreath,
        Path("m 10.31,11.36 h 5.16 v 1.25 H 8.53 V 11.36 q 0.84,-0.87 2.29,-2.34 1.46,-1.47 1.83,-1.90 0.71,-0.80 0.99,-1.35 0.29,-0.56 0.29,-1.09 0,-0.87 -0.62,-1.42 -0.61,-0.55 -1.59,-0.55 -0.70,0 -1.47,0.24 Q 9.48,3.20 8.60,3.69 V 2.20 q 0.89,-0.36 1.67,-0.54 0.78,-0.18 1.42,-0.18 1.70,0 2.71,0.85 1.01,0.85 1.01,2.27 0,0.67 -0.26,1.28 -0.25,0.60 -0.92,1.42 -0.18,0.21 -1.16,1.23 -0.98,1.01 -2.77,2.83 z"),
    )),
    4: Icon((
        wreath,
        Path("M 12.95,2.96 9.22,8.80 H 12.95 Z M 12.56,1.67 h 1.86 v 7.13 h 1.56 v 1.23 h -1.56 v 2.58 H 12.95 V 10.03 H 8.02 V 8.60 z"),
    ))
}
hex_icons = {
    "C": Icon((
        hex,
        Path(
            "M 14.41,5.37 V 6.93 Q 13.66,6.24 12.81,5.89 11.97,5.55 11.02,5.55 q -1.87,0 -2.87,1.15 -1.00,1.14 -1.00,3.31 0,2.16 1.00,3.31 1.00,1.14 2.87,1.14 0.95,0 1.79,-0.34 0.85,-0.34 1.60,-1.04 v 1.54541 q -0.78,0.53 -1.65,0.79 -0.86,0.26 -1.83,0.26 -2.48,0 -3.91,-1.52 -1.43,-1.52 -1.43,-4.15 0,-2.64 1.43,-4.15 1.43,-1.52 3.91,-1.52 0.98,0 1.85,0.26 0.87,0.26 1.63,0.78 z"
        ),
    )),
    "L": Icon((
        hex,
        Path(
            "M 6.60,4.53 H 8.08 V 14.22 H 13.40 v 1.25 H 6.60 Z"
        ),
    )),
    "N": Icon((
        hex,
        Path(
            "M 5.86,4.53 H 7.85 L 12.70,13.68 V 4.53 h 1.44 V 15.47 H 12.15 L 7.30,6.32 V 15.47 H 5.86 Z"
        ),
    )),
    "M": Icon((
        hex,
        Path(
            "M 5.00,4.53 H 7.20 L 9.99,11.97 12.80,4.53 h 2.20 V 15.47 H 13.56 V 5.87 L 10.74,13.37 H 9.95 L 6.43,5.87 V 15.47 H 5.00 Z"
        ),
    )),
    "S": Icon((
        hex,
        Path(
            "M 13.19,4.89 V 6.33 Q 12.35,5.93 11.60,5.73 10.85,5.54 10.16,5.54 q -1.21,0 -1.87,0.47 -0.65,0.47 -0.65,1.33 0,0.73 0.43,1.10 0.44,0.37 1.66,0.59 l 0.89,0.18 q 1.66,0.31 2.44,1.11 0.80,0.79 0.79,2.12 0,1.59 -1.07,2.41 -1.06,0.82 -3.12,0.82 -0.78,0 -1.66,-0.18 -0.87,-0.18 -1.81,-0.52 v -1.52 q 0.90,0.51 1.77,0.76 0.86,0.26 1.70,0.26 1.27,0 1.96,-0.50 0.69,-0.50 0.69,-1.42 0,-0.81 -0.50,-1.26 -0.49,-0.45 -1.62,-0.68 L 9.29,10.44 Q 7.63,10.11 6.89,9.41 6.15,8.71 6.15,7.45 q 0,-1.45 1.02,-2.29 1.03,-0.83 2.82,-0.83 0.77,0 1.57,0.14 0.80,0.14 1.63,0.42 z"
        ),
    )),
}

class VikingCard(Card):
    def __init__(self, number: int):
        super().__init__(Colour.SCARLET)
        self.number = number

    @property
    def filename(self) -> str:
        return f"card-viking-{self.number:02}.svg"

    def elements(self, doc: minidom.Document) -> Iterator[minidom.Element]:
        # calculate width and height of grid sections
        gsw = self.width // 4
        gsh = self.height // 4

        # number
        x_offset = gsw // 2
        if self.number < 10:
            digit = digits[self.number]
            yield digit.svg(doc, *self.position(digit, gsw, gsh, 1, 1, x_offset))
        else:
            first = digits[self.number // 10]
            yield first.svg(doc, *self.position(first, gsw, gsh, 1, 1, 4))
            second = digits[self.number % 10]
            yield second.svg(doc, *self.position(second, gsw, gsh, 2, 1, -4))

        # axe icon
        yield viking.svg(doc, *self.position(viking, gsw, gsh, 1, 2, x_offset))

class Hex(Part):
    def __init__(self, radius: int, x: int, y: int, fill: Colour = Colour.TEA_GREEN, stroke: Colour = Colour.BLACK, stroke_width: int = 2):
        self.radius = radius
        self.x = x
        self.y = y
        self.fill = fill
        self.stroke = stroke
        self.stroke_width = stroke_width
    
    @classmethod
    def from_doubled_coordinates(cls, col: int, row: int, radius: float) -> 'Hex':
        x = radius * 3/2 * col
        y = radius * math.sqrt(3)/2 * row
        return cls(radius, x, y)

    def points(self, x: float, y: float) -> Sequence[Tuple[float, float]]:
        first = (
            x + (self.radius * math.cos(0)),
            y + (self.radius * math.sin(0)),
        )

        return (first,) + tuple(
            (
                x + (self.radius * math.cos(i * 2 * math.pi / 6)),
                y + (self.radius * math.sin(i * 2 * math.pi / 6))
            ) for i in range(1, 6)
        )

    def points_text(self, x: float, y: float) -> str:
        return ' '.join(
            f'{x:.2f},{y:.2f}' for (x, y) in self.points(x, y)
        )

    def svg(self, doc: minidom.Document, x: int, y: int) -> minidom.Element:
        poly = doc.createElement("polygon")
        poly.setAttribute("style", f"fill:#{self.fill.value};stroke:#{self.stroke.value};stroke-width:{self.stroke_width}px")
        poly.setAttribute("points", self.points_text(x + self.x, y + self.y))
        return poly

def board():
    doc = minidom.Document()

    svg = doc.createElement("svg")
    svg.setAttribute("xmlns", "http://www.w3.org/2000/svg")
    svg.setAttribute("width", "960")
    svg.setAttribute("height", "680")
    svg.setAttribute("viewbox", "0 0 960 680")

    rect = doc.createElement("rect")
    rect.setAttribute("x", "0")
    rect.setAttribute("y", "0")
    rect.setAttribute("width", "960")
    rect.setAttribute("height", "680")
    rect.setAttribute("style", f"fill:#{Colour.PALE_AQUA.value};stroke:#000000;stoke-width:2px")
    svg.appendChild(rect)

    for hex in (
        Hex.from_doubled_coordinates(1, 1, 96),
        Hex.from_doubled_coordinates(1, 3, 96),
        Hex.from_doubled_coordinates(1, 5, 96),
        Hex.from_doubled_coordinates(2, 0, 96),
        Hex.from_doubled_coordinates(2, 2, 96),
        Hex.from_doubled_coordinates(2, 4, 96),
        Hex.from_doubled_coordinates(3, 1, 96),
        Hex.from_doubled_coordinates(3, 3, 96),
    ):
        svg.appendChild(hex.svg(doc, 190, 120))
  
    return svg


action_cards = [
    ActionCard(
        1,
        Colour.DAFFODIL,
        (
            (city, marriage, marriage, coin),
            (coin, coin, coin, expand),
            (marriage, marriage),
        ),
    ),
    ActionCard(
        2,
        Colour.SCARLET,
        (
            (city, viking, viking, coin),
            (coin, coin, coin, expand),
            (viking, viking),
        ),
    ),
    ActionCard(
        3,
        Colour.CORNFLOWER_BLUE,
        (
            (city, church, church, coin),
            (coin, coin, coin, expand),
            (church, church),
        ),
    ),
    ActionCard(
        4,
        Colour.DAFFODIL,
        (
            (city, marriage, marriage),
            (coin, coin, coin, expand),
            (marriage, marriage),
        ),
    ),
    ActionCard(
        5,
        Colour.SCARLET,
        (
            (city, viking, viking),
            (coin, coin, expand),
            (viking, viking),
        ),
    ),
    ActionCard(
        6,
        Colour.CORNFLOWER_BLUE,
        (
            (city, church, church),
            (coin, coin, coin, expand),
            (church, church),
        ),
    ),
    ActionCard(
        7,
        Colour.DAFFODIL,
        (
            (city, marriage, coin),
            (coin, coin, expand),
            (marriage, marriage),
        ),
    ),
    ActionCard(
        8,
        Colour.SCARLET,
        (
            (city, viking, coin),
            (coin, coin, expand),
            (viking, viking),
        ),
    ),
    ActionCard(
        9,
        Colour.CORNFLOWER_BLUE,
        (
            (city, church, coin),
            (coin, coin, expand),
            (church, church),
        ),
    ),
    ActionCard(
        10,
        Colour.DAFFODIL,
        (
            (city, coin, coin),
            (coin, coin, expand),
            (marriage, marriage),
        ),
    ),
    ActionCard(
        11,
        Colour.SCARLET,
        (
            (city, coin, coin),
            (coin, coin, expand),
            (viking, viking),
        ),
    ),
    ActionCard(
        12,
        Colour.CORNFLOWER_BLUE,
        (
            (city, coin, coin),
            (coin, coin, expand),
            (church, church),
        ),
    ),
    ActionCard(
        13,
        Colour.IVORY,
        (
            (city, coin),
            (coin, coin, expand),
            (remove_viking, pay),
        ),
    ),
    ActionCard(
        14,
        Colour.DAFFODIL,
        (
            (city,),
            (coin, expand),
            (marriage, marriage, marriage),
        ),
    ),
    ActionCard(
        15,
        Colour.SCARLET,
        (
            (city,),
            (coin, expand),
            (viking, viking, viking),
        ),
    ),
    ActionCard(
        16,
        Colour.CORNFLOWER_BLUE,
        (
            (city,),
            (coin, expand),
            (church, church, church),
        ),
    ),
    ActionCard(
        17,
        Colour.DAFFODIL,
        (
            (city, pay),
            (coin, expand),
            (marriage, marriage, marriage),
        ),
    ),
    ActionCard(
        18,
        Colour.SCARLET,
        (
            (city, pay),
            (coin, expand),
            (viking, viking, viking),
        ),
    ),
    ActionCard(
        19,
        Colour.CORNFLOWER_BLUE,
        (
            (city, pay),
            (coin, expand),
            (church, church, church),
        ),
    ),
    ActionCard(
        20,
        Colour.IVORY,
        (
            (city,),
            (coin, coin, expand),
        ),
    ),
    ActionCard(
        21,
        Colour.IVORY,
        (
            (city, pay),
            (coin, coin, expand),
        ),
    ),
    ActionCard(
        22,
        Colour.IVORY,
        (
            (city, pay, pay),
            (coin, coin, expand),
        ),
    ),
    ActionCard(
        23,
        Colour.DAFFODIL,
        (
            (city, pay, pay),
            (coin, expand),
            (marriage, marriage, marriage),
        ),
    ),
    ActionCard(
        24,
        Colour.SCARLET,
        (
            (city, pay, pay),
            (coin, expand),
            (viking, viking, viking),
        ),
    ),
    ActionCard(
        25,
        Colour.CORNFLOWER_BLUE,
        (
            (city, pay, pay),
            (coin, expand),
            (church, church, church),
        ),
    ),
]

card_backs = (
    CardBack(Colour.CORNFLOWER_BLUE, "action"),
    CardBack(Colour.DAFFODIL, "marriage"),
    CardBack(Colour.SCARLET, "viking"),
)

marriage_cards = [
    MarriageCard("Aodhán", ((vp_icons[2],), (Icon((triquetra,)), hex_icons["L"]))),
    MarriageCard("Aoife", ((vp_icons[2],), (renown,))),
    MarriageCard("Brigid", ((vp_icons[4],), ())),
    MarriageCard("Conall", ((vp_icons[2],), (Icon((triquetra,)), hex_icons["S"]))),
    MarriageCard("Cormac", ((vp_icons[2],), (Icon((triquetra,)), hex_icons["C"]))),
    MarriageCard("Niall", ((vp_icons[2],), (Icon((triquetra,)), hex_icons["N"]))),
    MarriageCard("Orlaith", ((vp_icons[2],), (Icon((triquetra,)), hex_icons["M"]))),
    # MarriageCard("Estrid", ()), # Military Support / discard & 4vp; Establish Trade / discard & 4vp
]

viking_cards = [
    VikingCard(9),
    VikingCard(10),
    VikingCard(11),
    VikingCard(12),
    VikingCard(13),
    VikingCard(14),
]

def remove_file_if_exists(path: str) -> None:
    try:
        os.remove(path)
    except FileNotFoundError:
        pass

def write_svg_to_file(path: str, svg: str) -> None:
    with open(path, "w") as f:
        f.write(svg)

def save_asset(asset: Card) -> None:
    path = f"brian-boru/assets/{asset.filename}"
    remove_file_if_exists(path)
    write_svg_to_file(path, asset.render())

if __name__ == "__main__":
    for card in card_backs:
        save_asset(card)
    for card in action_cards:
        save_asset(card)
    for card in marriage_cards:
        save_asset(card)
    for card in viking_cards:
        save_asset(card)
    
    remove_file_if_exists("brian-boru/assets/board.svg")
    write_svg_to_file("brian-boru/assets/board.svg", board().toprettyxml())