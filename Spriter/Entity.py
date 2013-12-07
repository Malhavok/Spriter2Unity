__author__ = 'Malhavok'

from Animation import Animation
import Utils

class Entity(object):
    def __init__(self, node):
        self.id = None
        self.name = None

        self.animations = {}

        self.fileKeeper = None

        self.parse(node)


    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_anim(self, idx):
        if idx not in self.animations:
            return None

        return self.animations[idx]

    def get_num_anims(self):
        return len(self.animations)


    def set_file_keeper(self, fk):
        self.fileKeeper = fk

        for anim in self.animations.values():
            anim.set_file_keeper(fk)

    def parse(self, node):
        self.id = int(node.attrib['id'])
        self.name = node.attrib['name']

        for elem in node:
            if elem.tag != 'animation':
                continue

            a = Animation(elem)
            self.animations[a.get_id()] = a

    def __str__(self):
        outList = []

        outList.append('Entity (id: %d, name: %s)' % (self.id, self.name))

        for elem in self.animations.values():
            outList.append(Utils.tabber(1, str(elem)))

        return '\n'.join(outList)