__author__ = 'Malhavok'

from File import File
import Utils

class Folder(object):
    def __init__(self, node):
        self.id = 0
        self.files = {}

        self.parse(node)

    def get_id(self):
        return self.id

    def get_file(self, fileId):
        if fileId not in self.files:
            return None

        return self.files[fileId]

    def get_file_list(self):
        outList = []

        for f in self.files.values():
            outList.append(f.get_name())

        return outList

    def parse(self, node):
        self.id = int(node.attrib['id'])

        for sub in node:
            f = File(sub)
            self.files[f.get_id()] = f

    def __str__(self):
        outList = []

        outList.append('Folder (id: %d)' % (self.id,))

        for elem in self.files.values():
            outList.append(Utils.tabber(1, str(elem)))

        return '\n'.join(outList)