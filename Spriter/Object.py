__author__ = 'Malhavok'

from KeyElem import KeyElem
import math

class Object(KeyElem):
    type = 'object'

    def __init__(self, node):
        super(self.__class__, self).__init__(Object.type)

        self.folder = None
        self.file = None
        self.x = None
        self.y = None
        self.pivot_x = None
        self.pivot_y = None
        self.angle = None
        self.angle_deg = None
        self.scale_x = None
        self.scale_y = None

        self.parse(node)

    def parse(self, node):
        self.folder = int(node.attrib['folder'])
        self.file = int(node.attrib['file'])
        self.x = float(node.attrib.get('x', 0.0))
        self.y = float(node.attrib.get('y', 0.0))

        if 'pivot_x' in node.attrib:
            self.pivot_x = float(node.attrib['pivot_x'])

        if 'pivot_y' in node.attrib:
            self.pivot_y = float(node.attrib['pivot_y'])

        self.angle_deg = float(node.attrib.get('angle', 0.0))
        self.angle = self.angle_deg * math.pi / 180.0
        self.scale_x = float(node.attrib.get('scale_x', 1.0))
        self.scale_y = float(node.attrib.get('scale_y', 1.0))

    def __str__(self):
        return 'Object (folder: %d, file: %d, x: %f, y: %f, px: %s, py: %s, sx: %f, sy: %f, a: %f [deg: %f])'\
                % (self.folder, self.file, self.x, self.y, str(self.pivot_x), str(self.pivot_y), self.scale_x, self.scale_y, self.angle, self.angle_deg)