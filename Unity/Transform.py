__author__ = 'Malhavok'

from Component import Component
import math

class Transform(Component):
    globalId = 0
    type = 4

    def __init__(self):
        super(self.__class__, self).__init__(Transform.type, Transform.globalId)
        Transform.globalId += 2

        self.position = (0, 0, 0)
        self.rotation = (0, 0, 0, 1)
        self.scale = (1, 1, 1)

        self.angle = 0.0

        self.children = []
        self.father = None

    def add_child(self, othTransform):
        if othTransform.get_id() in self.children:
            return False

        othTransform.father = self.get_id()
        self.children.append(othTransform.get_id())
        return True

    def set_position(self, x, y, z):
        self.position = (x, y, z)

    def get_position(self):
        return self.position

    def get_x_position(self):
        return self.position[0]

    def get_y_position(self):
        return self.position[1]

    def get_z_position(self):
        return self.position[2]

    def set_z_rot(self, angleRad):
        self.angle = angleRad
        self.rotation = (0.0, 0.0, math.sin(angleRad / 2.0), math.cos(angleRad / 2.0))

    def get_z_angle(self):
        return self.angle

    def get_rotation(self):
        return self.rotation

    def set_scale(self, x, y, z):
        self.scale = (x, y, z)

    def get_scale(self):
        return self.scale

    def get_x_scale(self):
        return self.scale[0]

    def get_y_scale(self):
        return self.scale[1]

    def get_z_scale(self):
        return self.scale[2]

    def to_string(self):
        outList = []

        outList.append('--- !u!4 &4%05d' % (self.id,))
        outList.append('Transform:')
        outList.append('  m_ObjectHideFlags: 1')
        outList.append('  m_PrefabParentObject: {fileID: 0}')
        outList.append('  m_PrefabInternal: {fileID: 100100000}')
        outList.append('  m_GameObject: {fileID: 1%05d}' % (self.gameObjectId,))
        outList.append('  m_LocalRotation: {x: %f, y: %f, z: %f, w: %f}' % (self.rotation[0], self.rotation[1], self.rotation[2], self.rotation[3]))
        outList.append('  m_LocalPosition: {x: %f, y: %f, z: %f}' % (self.position[0], self.position[1], self.position[2]))
        outList.append('  m_LocalScale: {x: %f, y: %f, z: %f}' % (self.scale[0], self.scale[1], self.scale[2]))

        if len(self.children) == 0:
            outList.append('  m_Children: []')
        else:
            outList.append('  m_Children:')
            for child in self.children:
                outList.append('  - {fileID: 4%05d}' % (child,))

        if self.father is None:
            outList.append('  m_Father: {fileID: 0}')
        else:
            outList.append('  m_Father: {fileID: 4%05d}' % (self.father,))

        return '\n'.join(outList)
