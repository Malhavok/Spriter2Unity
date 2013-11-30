__author__ = 'Malhavok'

import Utils
from BoneRef import BoneRef
from Bone import Bone


class Node(object):
    def __init__(self):
        self.name = '(None)'

        self.x = 0.0
        self.y = 0.0
        self.angle = 0.0

        self.scale_x = 1.0
        self.scale_y = 1.0

        self.bone = None
        self.boneRef = None

        self.parent = None
        self.children = []

    def add_child(self, othNode):
        othNode.parent = self
        self.children.append(othNode)

    def detach_from_parent(self):
        self.parent = None

    def get_name(self):
        return self.name

    def get_bone_id(self):
        if self.boneRef is None:
            return None
        return self.boneRef.id

    def get_pos(self):
        return self.x, self.y

    def get_pos_x(self):
        return self.x

    def get_pos_y(self):
        return self.y

    def get_scale(self):
        return self.scale_x, self.scale_y

    def get_scale_x(self):
        return self.scale_x

    def get_scale_y(self):
        return self.scale_y

    def get_angle(self):
        return self.angle

    def get_parent(self):
        return self.parent

    def get_children(self):
        return self.children

    def build(self, boneRef, timeline):
        # does the magic
        # retrieves proper BONE from timeline
        # and fills internal data with it
        if boneRef.get_type() != BoneRef.type:
            Utils.print_error('node didnt get boneref', [boneRef, timeline])

        self.boneRef = boneRef
        timeIdx = boneRef.timeline
        timeKey = boneRef.key

        if timeIdx not in timeline:
            Utils.print_error('cant build node with given data', [boneRef, timeline])

        timeElem = timeline[timeIdx]
        self.name = timeElem.name

        if timeKey not in timeElem.keys:
            Utils.print_error('cant build node with given data', [boneRef, timeline, timeElem])

        finalKey = timeElem.keys[timeKey]
        bone = finalKey.get_bone()

        if bone is None:
            Utils.print_error('cant build node - there is no bone in key', [boneRef, timeline, timeElem, finalKey])

        if bone.get_type() != Bone.type:
            Utils.print_error('Bone is not a bone', [boneRef, timeline, timeElem, finalKey, bone])

        # fill using data from bone!
        self.x = bone.x
        self.y = bone.y
        self.scale_x = bone.scale_x
        self.scale_y = bone.scale_y
        self.angle = bone.angle

        self.bone = bone

        return finalKey.time


    def __str__(self):
        outList = []

        outList.append('Node (name: %s, x: %f, y: %f, sx: %f, sy: %f, angle: %f)' %\
                       (self.name, self.x, self.y, self.scale_x, self.scale_y, self.angle))

        if self.bone is None:
            outList.append('\tBone: (None)')
        else:
            outList.append('\tBone:')
            outList.append(Utils.tabber(2, str(self.bone)))

        if self.parent is None:
            outList.append('\tParent: (None)')
        else:
            outList.append('\tParent: (Exists)')
#            outList.append(Utils.tabber(2, str(self.parent)))

        if len(self.children) == 0:
            outList.append('\tChildren: (None)')
        else:
            outList.append('\tChildren:')
            for child in self.children:
                outList.append(Utils.tabber(2, str(child)))

        return '\n'.join(outList)
