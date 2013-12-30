__author__ = 'Malhavok'

from Node import Node
from Sprite import Sprite
from BoneRef import BoneRef
from ObjectRef import ObjectRef

import Utils
import math


class KeyFrame(object):
    def __init__(self, key, timeline, fileKeeper):
        self.key = key
        self.timeline = timeline
        self.fileKeeper = fileKeeper

        tmpNode = Node()
        self.parse_key(tmpNode)
        self.nodes = tmpNode.children

        for node in self.nodes:
            node.detach_from_parent()


    def get_time(self):
        return self.key.time

    def parse_key(self, node):
        # in self.key there should be only ref nodes
        # the point is at start to create all nodes that have NO parent
        starter = self.get_from_key_with_parent(node.get_bone_id())

        if len(starter) == 0:
            print 'WARNING: found a bone with no children attached:', node.get_name(), 'id:', node.get_bone_id()
#            Utils.print_error('There are no nodes with this node as parent', [node, self.key, self.timeline])

        for st in starter:
            obj = None
            if st.get_type() == BoneRef.type:
                obj = Node()
            elif st.get_type() == ObjectRef.type:
                obj = Sprite(self.fileKeeper)

            if obj is None:
                Utils.print_error('Unable to generate node nor sprite from', [obj, self.key, self.timeline])

            objTime = obj.build(st, self.timeline)

            if math.fabs(self.key.time - objTime) > 1e-4:
                obj.set_active(False)

            node.add_child(obj)

            newPath = obj.get_bone_id()
            if newPath is not None:
                self.parse_key(obj)


    def get_from_key_with_parent(self, parent):
        outList = []

        allItems = self.key.get_refs()
        if not len(allItems):
            Utils.print_error('no references from a key', [self.key, self.timeline, self.nodes])

        for item in allItems:
            if item.get_parent() == parent:
                outList.append(item)

        return outList


    def __str__(self):
        outList = []

        outList.append('KeyFrame:')

        outList.append('Nodes:')
        for node in self.nodes:
            outList.append(Utils.tabber(1, str(node)))

        return '\n'.join(outList)