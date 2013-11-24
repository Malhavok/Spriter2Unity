__author__ = 'Malhavok'

from ObjectRef import ObjectRef
from BoneRef import BoneRef
from Object import Object
from Bone import Bone
import Utils

class Key(object):
    def __init__(self, node):
        self.id = None
        self.time_ms = None
        self.time = None
        self.spin = None

        self.sub_items = {}

        self.parse(node)

    def get_id(self):
        return self.id

    def get_refs(self):
        outList = self.sub_items.get(BoneRef.type, {}).values()
        outList.extend(self.sub_items.get(ObjectRef.type, {}).values())
        return outList

    def get_bone(self):
        if Bone.type not in self.sub_items:
            return None
        return self.sub_items[Bone.type]

    def get_object(self):
        if Object.type not in self.sub_items:
            return None
        return self.sub_items[Object.type]

    def parse(self, node):
        self.id = int(node.attrib['id'])

        self.time_ms = int(node.attrib.get('time', 0))
        self.time = self.time_ms / 1000.0

        self.spin = int(node.attrib.get('spin', 1))

        for elem in node:
            if elem.tag == 'object':
                self.parse_object(elem)
            elif elem.tag == 'bone':
                self.parse_bone(elem)
            elif elem.tag == 'bone_ref':
                self.parse_bone_ref(elem)
            elif elem.tag == 'object_ref':
                self.parse_object_ref(elem)
            else:
                print 'Unknown object type under key:', elem.tag
                exit(1)

    def parse_object(self, node):
        o = Object(node)
        self.add_obj(Object.type, o)

    def parse_bone(self, node):
        b = Bone(node)
        self.add_obj(Bone.type, b)

    def parse_bone_ref(self, node):
        b = BoneRef(node)
        self.add_ref(BoneRef.type, b.get_id(), b)

    def parse_object_ref(self, node):
        o = ObjectRef(node)
        self.add_ref(ObjectRef.type, o.get_id(), o)

    def add_ref(self, group, key, value):
        if group not in self.sub_items:
            self.sub_items[group] = {}

        self.sub_items[group][key] = value

    def add_obj(self, group, obj):
        self.sub_items[group] = obj

    def __str__(self):
        outList = []

        outList.append('Key (id: %d, time: %fs, spin: %d)' % (self.id, self.time, self.spin))

        for elem in self.sub_items.values():
            if type(elem) == dict:
                for sub in elem.values():
                    outList.append(Utils.tabber(1, str(sub)))
            else:
                outList.append(Utils.tabber(1, str(elem)))

        return '\n'.join(outList)
