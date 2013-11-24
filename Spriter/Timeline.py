__author__ = 'Malhavok'

from Key import Key
import Utils

class Timeline(object):
    def __init__(self, node):
        self.id = None
        self.name = None

        self.keys = {}

        self.parse(node)

    def get_id(self):
        return self.id

    def parse(self, node):
        self.id = int(node.attrib['id'])
        self.name = node.attrib['name']

        for elem in node:
            k = Key(elem)
            self.keys[k.get_id()] = k

    def __str__(self):
        outList = []

        outList.append('Timeline (id: %d, name: %s)' % (self.id, self.name))

        for elem in self.keys.values():
            outList.append(Utils.tabber(1, str(elem)))

        return '\n'.join(outList)