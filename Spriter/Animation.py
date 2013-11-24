__author__ = 'Malhavok'

from Timeline import Timeline
from Key import Key
import Utils
from KeyFrame import KeyFrame

class Animation(object):
    def __init__(self, node):
        self.id = None
        self.name = None
        self.length_ms = None
        self.length = None

        self.mainline = {}
        self.timeline = {}

        self.fileKeeper = None

        self.parse(node)


    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_time(self):
        ## time in seconds
        return self.length

    def get_key_frame(self, idx):
        if idx not in self.mainline:
            return None

        return KeyFrame(self.mainline[idx], self.timeline, self.fileKeeper)

    def get_num_key_frames(self):
        return len(self.mainline)


    def set_file_keeper(self, fk):
        self.fileKeeper = fk

    def parse(self, node):
        self.id = int(node.attrib['id'])
        self.name = node.attrib['name']
        self.length_ms = float(node.attrib['length'])
        self.length = self.length_ms / 1000.0

        for elem in node:
            if elem.tag == 'mainline':
                self.parse_mainline(elem)
            elif elem.tag == 'timeline':
                t = Timeline(elem)
                self.timeline[t.get_id()] = t

    def parse_mainline(self, node):
        for elem in node:
            k = Key(elem)
            self.mainline[k.get_id()] = k


    def __str__(self):
        outList = []
        outList.append('Animation (id: %d, name: %s, length: %fs)' % (self.id, self.name, self.length))

        for elem in self.mainline.values():
            outList.append(Utils.tabber(1, str(elem)))

        for elem in self.timeline.values():
            outList.append(Utils.tabber(1, str(elem)))

        return '\n'.join(outList)