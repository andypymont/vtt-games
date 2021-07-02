"""Generate the Rheinalnder board SVG."""

import xml.etree.ElementTree as ET
from statistics import mean
from xml.dom import minidom

points = {
    1: (0, 624),
    2: (0, 671),
    3: (0, 712),
    4: (0, 763),
    5: (31, 621),
    6: (56, 663),
    7: (80, 700),
    8: (109, 741),
    9: (52, 593),
    10: (98, 613),
    11: (137, 629),
    12: (190, 649),
    13: (59, 550),
    14: (108, 555),
    15: (150, 559),
    16: (191, 563),
    17: (54, 499),
    18: (105, 498),
    19: (147, 496),
    20: (191, 494),
    21: (44, 444),
    22: (95, 441),
    23: (138, 438),
    24: (183, 437),
    25: (191, 448),
    26: (199, 436),
    27: (27, 373),
    28: (76, 373),
    29: (120, 373),
    30: (166, 373),
    31: (14, 295),
    32: (66, 303),
    33: (109, 310),
    34: (161, 318),
    35: (18, 206),
    36: (66, 226),
    37: (107, 245),
    38: (159, 269),
    39: (83, 104),
    40: (110, 148),
    41: (134, 184),
    42: (167, 238),
    43: (193, 74),
    44: (193, 126),
    45: (193, 168),
    46: (193, 234),
    47: (295, 102),
    48: (268, 148),
    49: (246, 184),
    50: (215, 240),
    51: (364, 196),
    52: (315, 222),
    53: (275, 243),
    54: (223, 272),
    55: (368, 283),
    56: (317, 296),
    57: (274, 307),
    58: (220, 319),
    59: (360, 360),
    60: (306, 364),
    61: (261, 368),
    62: (213, 369),
    63: (347, 430),
    64: (291, 431),
    65: (247, 433),
    66: (333, 489),
    67: (281, 490),
    68: (238, 492),
    69: (331, 538),
    70: (278, 548),
    71: (235, 556),
    72: (335, 588),
    73: (283, 612),
    74: (243, 629),
    75: (348, 628),
    76: (302, 669),
    77: (269, 697),
    78: (231, 731),
    79: (369, 650),
    80: (349, 710),
    81: (335, 750),
    82: (320, 798),
    83: (398, 655),
    84: (408, 714),
    85: (416, 754),
    86: (424, 803),
    87: (436, 643),
    88: (465, 695),
    89: (485, 731),
    90: (508, 775),
    91: (467, 621),
    92: (510, 658),
    93: (543, 684),
    94: (580, 716),
    95: (481, 591),
    96: (537, 605),
    97: (578, 616),
    98: (628, 627),
    99: (485, 539),
    100: (541, 542),
    101: (584, 546),
    102: (634, 549),
    103: (467, 489),
    104: (522, 486),
    105: (568, 483),
    106: (621, 481),
    107: (428, 434),
    108: (485, 430),
    109: (534, 425),
    110: (595, 420),
    111: (409, 360),
    112: (463, 366),
    113: (506, 371),
    114: (569, 378),
    115: (411, 281),
    116: (457, 297),
    117: (514, 317),
    118: (578, 341),
    119: (438, 181),
    120: (476, 209),
    121: (504, 266),
    122: (564, 281),
    123: (507, 205),
    124: (516, 248),
    125: (562, 250),
    126: (613, 321),
    127: (510, 91),
    128: (536, 129),
    129: (555, 156),
    130: (579, 189),
    131: (599, 218),
    132: (619, 245),
    133: (655, 296),
    134: (582, 51),
    135: (600, 92),
    136: (614, 122),
    137: (632, 158),
    138: (647, 190),
    139: (662, 220),
    140: (688, 277),
    141: (649, 26),
    142: (663, 69),
    143: (673, 100),
    144: (685, 137),
    145: (697, 172),
    146: (708, 205),
    147: (726, 262),
    148: (766, 25),
    149: (765, 72),
    150: (738, 93),
    151: (790, 125),
    152: (776, 125),
    153: (755, 160),
    154: (776, 178),
    155: (777, 239),
    156: (865, 70),
    157: (848, 121),
    158: (830, 174),
    159: (810, 232),
    160: (942, 151),
    161: (903, 189),
    162: (871, 221),
    163: (822, 268),
    164: (966, 227),
    165: (917, 257),
    166: (877, 285),
    167: (823, 316),
    168: (970, 307),
    169: (917, 328),
    170: (873, 346),
    171: (819, 368),
    172: (965, 381),
    173: (910, 397),
    174: (865, 409),
    175: (810, 426),
    176: (951, 455),
    177: (897, 465),
    178: (853, 473),
    179: (797, 482),
    180: (937, 524),
    181: (886, 528),
    182: (829, 533),
    183: (768, 538),
    184: (939, 597),
    185: (889, 579),
    186: (848, 561),
    187: (791, 586),
    188: (720, 615),
    189: (863, 610),
    190: (845, 578),
    191: (813, 603),
    192: (939, 670),
    193: (891, 664),
    194: (858, 661),
    195: (792, 659),
    196: (757, 663),
    197: (704, 667),
    198: (921, 731),
    199: (868, 730),
    200: (832, 731),
    201: (776, 731),
    202: (738, 730),
    203: (685, 730),
    204: (906, 783),
    205: (852, 783),
    206: (812, 783),
    207: (764, 783),
    208: (722, 783),
    209: (670, 783),
    210: (889, 840),
    211: (836, 840),
    212: (793, 840),
    213: (751, 840),
    214: (709, 840),
    215: (653, 840),
    'L01': (30, 613),
    'L02': (192, 617),
    'L03': (45, 502),
    'L04': (164, 373),
    'L05': (26, 207),
    'L06': (190, 248),
    'L07': (368, 199),
    'L08': (215, 376),
    'L09': (342, 491),
    'L10': (355, 622),
    'L11': (422, 792),
    'L12': (458, 617),
    'L13': (640, 549),
    'L14': (428, 437),
    'L15': (587, 347),
    'L16': (544, 217),
    'L17': (689, 280),
    'L18': (579, 50),
    'L19': (721, 131),
    'L20': (865, 70),
    'L21': (821, 316),
    'L22': (965, 384),
    'L23': (762, 540),
    'L24': (823, 661),
    'L25': (907, 784),
    'L26': (665, 784),
}

def polygon(doc, point_seq, fill, number=None):
    """Generate SVG polygon connecting the given set of points."""
    poly = ET.SubElement(doc, 'polygon')
    poly.set('style', 'fill:#{};stroke:#000000;stroke-width:1px'.format(fill))
    point_locs = [points.get(point) for point in point_seq]
    poly.set('points', ' '.join('{},{}'.format(x, y) for (x, y) in point_locs))
    if number is not None:
        number_label(doc, number, *center(point_locs))
    return poly

def number_label(doc, number, x, y):
    """Generate a number label (for a river space)."""
    text = ET.SubElement(doc, 'text')
    text.set('style', 'font:12px sans-serif;fill:#000000;align:center;text-anchor:middle')
    text.set('x', '{}'.format(x))
    text.set('y', '{}'.format(y))
    text.text = '{}'.format(number)
    return text

def land(doc, *point_seq):
    """Generate a land space connecting a given set of points."""
    return polygon(doc, point_seq, '00ff00')

def center(point_locs):
    """Calculate the center of the given points."""
    return (
        int(mean(pt[0] for pt in point_locs)),
        int(mean(pt[1] for pt in point_locs)),
    )
   
def river(doc, number, *point_seq):
    """Generate a river space connecting a given set of points."""
    return polygon(doc, point_seq, '0099ff', number)

def landmark(doc, location):
    """Generate a circle ready for a Landmark tile."""
    circle = ET.SubElement(doc, 'circle')
    x, y = points.get(location)
    circle.set('cx', '{}'.format(x))
    circle.set('cy', '{}'.format(y))
    circle.set('r', '20')
    circle.set('style', 'fill:#cc9999;stroke:#000000;stroke-width:1px')
    return circle

elements = [
    # 1:
    (land, 1, 2, 6, 5),
    (river, '1', 2, 3, 7, 6),
    (land, 3, 4, 8, 7),
    # 2:
    (land, 5, 6, 10, 9),
    (river, '2', 10, 11, 7, 6),
    (land, 11, 12, 8, 7),
    # 3:
    (land, 13, 14, 10, 9),
    (river, '3', 14, 15, 11, 10),
    (land, 15, 16, 12, 11),
    # 4:
    (land, 17, 18, 14, 13),
    (river, '4', 18, 19, 15, 14),
    (land, 19, 20, 16, 15),
    # 5:
    (land, 21, 22, 18, 17),
    (river, '5', 22, 23, 19, 18),
    (land, 23, 24, 25, 20, 19),
    # 6:
    (land, 27, 28, 22, 21),
    (river, '6', 28, 29, 23, 22),
    (land, 29, 30, 24, 23),
    # 7:
    (land, 31, 32, 28, 27),
    (river, '7', 32, 33, 29, 28),
    (land, 33, 34, 30, 29),
    # 8:
    (land, 35, 36, 32, 31),
    (river, '8', 36, 37, 33, 32),
    (land, 37, 38, 34, 33),
    # 9:
    (land, 39, 40, 36, 35),
    (river, '9', 40, 41, 37, 36),
    (land, 41, 42, 38, 37),
    # 10:
    (land, 39, 40, 44, 43),
    (river, '10', 40, 41, 45, 44),
    (land, 41, 42, 46, 45),
    # 11:
    (land, 43, 44, 48, 47),
    (river, '11', 44, 45, 49, 48),
    (land, 45, 46, 50, 49),
    # 12:
    (land, 47, 48, 52, 51),
    (river, '12', 48, 49, 53, 52),
    (land, 49, 50, 54, 53),
    # 13:
    (land, 53, 54, 58, 57),
    (river, '13', 52, 53, 57, 56),
    (land, 51, 52, 56, 55),
    # 14:
    (land, 58, 57, 61, 62),
    (river, '14', 56, 57, 61, 60),
    (land, 55, 56, 60, 59),
    # 15:
    (land, 61, 62, 26, 65),
    (river, '15', 60, 61, 65, 64),
    (land, 59, 60, 64, 63),
    # 16:
    (land, 65, 26, 25, 20, 68),
    (river, '16', 64, 65, 68, 67),
    (land, 63, 64, 67, 66),
    # 17:
    (land, 20, 16, 71, 68),
    (river, '17', 67, 68, 71, 70),
    (land, 66, 67, 70, 69),
    # 18:
    (land, 16, 12, 74, 71),
    (river, '18', 70, 71, 74, 73),
    (land, 69, 70, 73, 72),
    # 19:
    (land, 74, 77, 78, 12),
    (river, '19', 73, 74, 77, 76),
    (land, 72, 73, 76, 75),
    # 20:
    (land, 75, 76, 80, 79),
    (river, '20', 76, 77, 81, 80),
    (land, 77, 78, 82, 81),
    # 21:
    (land, 79, 80, 84, 83),
    (river, '21', 80, 81, 85, 84),
    (land, 81, 82, 86, 85),
    # 22:
    (land, 83, 84, 88, 87),
    (river, '22', 84, 85, 89, 88),
    (land, 85, 86, 90, 89),
    # 23:
    (land, 87, 88, 92, 91),
    (river, '23', 88, 89, 93, 92),
    (land, 89, 90, 94, 93),
    # 24:
    (land, 91, 92, 96, 95),
    (river, '24', 96, 97, 93, 92),
    (land, 97, 98, 94, 93),
    # 25:
    (land, 95, 96, 100, 99),
    (river, '25', 96, 97, 101, 100),
    (land, 97, 98, 102, 101),
    # 26:
    (land, 99, 100, 104, 103),
    (river, '26', 100, 101, 105, 104),
    (land, 101, 102, 106, 105),
    # 27:
    (land, 103, 104, 108, 107),
    (river, '27', 104, 105, 109, 108),
    (land, 105, 106, 110, 109),
    # 28:
    (land, 107, 108, 112, 111),
    (river, '28', 108, 109, 113, 112),
    (land, 109, 110, 114, 113),
    # 29:
    (land, 111, 112, 116, 115),
    (river, '29', 112, 113, 117, 116),
    (land, 113, 114, 118, 117),
    # 30:
    (land, 115, 116, 120, 119),
    (river, None, 116, 117, 122, 121, 120),
    (number_label, '30', 492, 286),
    (land, 117, 118, 126, 122),
    # 31:
    (land, 119, 120, 128, 127),
    (river, None, 120, 121, 124, 123, 129, 128),
    (number_label, '31', 492, 209),
    (land, 123, 124, 130, 129),
    # 32:
    (land, 130, 131, 125, 124),
    (river, None, 131, 132, 122, 121, 124, 125),
    (number_label, '32', 560, 263),
    (land, 132, 133, 126, 122),
    # 33:
    (land, 127, 128, 135, 134),
    (river, '33', 128, 129, 136, 135),
    (land, 129, 130, 137, 136),
    # 34:
    (land, 130, 131, 138, 137),
    (river, '34', 131, 132, 139, 138),
    (land, 132, 133, 140, 139),
    # 35:
    (land, 134, 135, 142, 141),
    (river, '35', 135, 136, 143, 142),
    (land, 136, 137, 144, 143),
    # 36:
    (land, 137, 138, 145, 144),
    (river, '36', 138, 139, 146, 145),
    (land, 139, 140, 147, 146),
    # 37:
    (land, 141, 142, 149, 148),
    (river, None, 142, 143, 150, 152, 151, 149),
    (number_label, '37', 725, 88),
    (land, 143, 144, 152, 150),
    # 38:
    (land, 144, 145, 153, 152),
    (river, None, 145, 146, 154, 151, 152, 153),
    (number_label, '38', 725, 185),
    (land, 154, 155, 147, 146),
    # 39:
    (land, 148, 149, 157, 156),
    (river, '39', 149, 151, 154, 158, 157),
    (land, 154, 155, 159, 158),
    # 40:
    (land, 156, 157, 161, 160),
    (river, '40', 157, 158, 162, 161),
    (land, 158, 159, 163, 162),
    # 41:
    (land, 162, 163, 167, 166),
    (river, '41', 161, 162, 166, 165),
    (land, 160, 161, 165, 164),
    # 42:
    (land, 166, 167, 171, 170),
    (river, '42', 165, 166, 170, 169),
    (land, 164, 165, 169, 168),
    # 43:
    (land, 170, 171, 175, 174),
    (river, '43', 169, 170, 174, 173),
    (land, 168, 169, 173, 172),
    # 44:
    (land, 174, 175, 179, 178),
    (river, '44', 173, 174, 178, 177),
    (land, 172, 173, 177, 176),
    # 45:
    (land, 176, 177, 181, 180),
    (river, '45', 177, 178, 182, 181),
    (land, 178, 179, 183, 182),
    # 46:
    (land, 180, 181, 185, 184),
    (river, None, 181, 182, 187, 186, 185),
    (number_label, '46', 848, 551),
    (land, 182, 183, 188, 187),
    # 47:
    (land, 187, 188, 197, 196),
    (river, None, 186, 187, 196, 195, 191, 190),
    (number_label, '47', 784, 630),
    (land, 194, 195, 191, 190, 189),
    # 48:
    (land, 184, 185, 193, 192),
    (river, None, 193, 194, 189, 190, 186, 185),
    (number_label, '48', 875, 630),
    # 49:
    (land, 196, 197, 203, 202),
    (river, '49', 195, 196, 202, 201),
    (land, 194, 195, 201, 200),
    # 50:
    (land, 192, 193, 199, 198),
    (river, '50', 193, 194, 200, 199),
    # 51:
    (land, 202, 203, 209, 208),
    (river, '51', 201, 202, 208, 207),
    (land, 200, 201, 207, 206),
    # 52:
    (land, 198, 199, 205, 204),
    (river, '52', 199, 200, 206, 205),
    # 53:
    (land, 208, 209, 215, 214),
    (river, '53', 207, 208, 214, 213),
    (land, 206, 207, 213, 212),
    # 54:
    (land, 204, 205, 211, 210),
    (river, '54', 205, 206, 212, 211),
    # Landmarks:
    (landmark, 'L01'),
    (landmark, 'L02'),
    (landmark, 'L03'),
    (landmark, 'L04'),
    (landmark, 'L05'),
    (landmark, 'L06'),
    (landmark, 'L07'),
    (landmark, 'L08'),
    (landmark, 'L09'),
    (landmark, 'L10'),
    (landmark, 'L11'),
    (landmark, 'L12'),
    (landmark, 'L13'),
    (landmark, 'L14'),
    (landmark, 'L15'),
    (landmark, 'L16'),
    (landmark, 'L17'),
    (landmark, 'L18'),
    (landmark, 'L19'),
    (landmark, 'L20'),
    (landmark, 'L21'),
    (landmark, 'L22'),
    (landmark, 'L23'),
    (landmark, 'L24'),
    (landmark, 'L25'),
    (landmark, 'L26'),
]

def main():
    """Generate and output the document."""
    doc = ET.Element('svg')
    doc.set('xlmns', 'http://www.w3.org/2000/svg')
    doc.set('width', '1000px')
    doc.set('height', '840px')
    doc.set('viewbox', '0 0 1000 840')

    for element in elements:
        func, *args = element
        func(doc, *args)

    rough_string = ET.tostring(doc, 'utf-8')
    reparsed = minidom.parseString(rough_string)

    with open('../assets/board.svg', 'w') as board_svg:
        board_svg.write(reparsed.toprettyxml(indent='    '))

if __name__ == '__main__':
    main()
