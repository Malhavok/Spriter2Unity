__author__ = 'Malhavok'

from KeyElem import KeyElem
import math

class Bone(KeyElem):
    type = 'bone'

    def __init__(self, node):
        super(self.__class__, self).__init__(Bone.type)

        self.x = None
        self.y = None
        self.scale_x = None
        self.scale_y = None
        self.angle_deg = None
        self.angle = None

        self.parse(node)

    def parse(self, node):
        self.x = float(node.attrib.get('x', 0.0))
        self.y = float(node.attrib.get('y', 0.0))
        self.scale_x = float(node.attrib.get('scale_x', 1.0))
        self.scale_y = float(node.attrib.get('scale_y', 1.0))
        self.angle_deg = float(node.attrib.get('angle', 0.0))
        self.angle = self.angle_deg * math.pi / 180.0

    def __str__(self):
        return 'Bone (x: %f, y: %f, sx: %f, sy: %f, angle: %f [deg: %f])'\
                % (self.x, self.y, self.scale_x, self.scale_y, self.angle, self.angle_deg)