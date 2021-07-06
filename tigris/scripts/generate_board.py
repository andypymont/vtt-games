"""Generate the Tigris & Euphrates board SVG."""

import xml.etree.ElementTree as ET
from xml.dom import minidom

WIDTH = 16
HEIGHT = 11
SQUARE_SIZE = 90

water_tiles = {
    (0, 3),
    (1, 3),
    (2, 3),
    (3, 3),
    (3, 2),
    (4, 2),
    (4, 1),
    (4, 0),
    (5, 0),
    (6, 0),
    (7, 0),
    (8, 0),
    (12, 0),
    (12, 1),
    (12, 2),
    (13, 2),
    (13, 3),
    (14, 3),
    (15, 3),
    (15, 4),
    (14, 4),
    (14, 5),
    (14, 6),
    (13, 6),
    (12, 6),
    (12, 7),
    (12, 8),
    (11, 8),
    (10, 8),
    (9, 8),
    (8, 8),
    (7, 8),
    (6, 8),
    (6, 7),
    (5, 7),
    (4, 7),
    (3, 7),
    (3, 6),
    (2, 6),
    (1, 6),
    (0, 6)
}

def square(doc, x_pos, y_pos, is_river):
    """Generate the SVG element for one square on the board."""
    sqr = ET.SubElement(doc, 'rect')
    sqr.set('x', '{}'.format(x_pos * SQUARE_SIZE))
    sqr.set('y', '{}'.format(y_pos * SQUARE_SIZE))
    sqr.set('width', '{}'.format(SQUARE_SIZE))
    sqr.set('height', '{}'.format(SQUARE_SIZE))

    colour = ('67a7c4' if is_river else 'fcefde')
    sqr.set('style', 'fill:#{};stroke:#000000;stroke-width:1px'.format(colour))

    return sqr

def main():
    """Generate and output the board."""
    total_width = WIDTH * SQUARE_SIZE
    total_height = HEIGHT * SQUARE_SIZE

    doc = ET.Element('svg')
    doc.set('xmlns', 'http://www.w3.org/2000/svg')
    doc.set('width', '{}'.format(total_width))
    doc.set('height', '{}'.format(total_height))
    doc.set('viewbox', '0 0 {} {}'.format(total_width, total_height))

    for x_pos in range(WIDTH):
        for y_pos in range(HEIGHT):
            is_river = (x_pos, y_pos) in water_tiles
            square(doc, x_pos, y_pos, is_river)
    
    rough_string = ET.tostring(doc, 'utf-8')
    reparsed = minidom.parseString(rough_string)

    with open('../assets/board.svg', 'w') as board_svg:
        board_svg.write(reparsed.toprettyxml(indent='    '))

if __name__ == '__main__':
    main()
