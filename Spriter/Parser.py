__author__ = 'Malhavok'

import xml.etree.ElementTree as ET
from Folder import Folder
from Entity import Entity
import Utils
from FileKeeper import FileKeeper

class Parser(object):
    supported_version = '1.0'

    def __init__(self, filename):
        self.filename = filename

        self.xml = ET.parse(filename)
        self.folders = {}
        self.entities = {}

    def make_error(self, msg):
        print 'ERROR:', msg
        exit(1)

    def get_file_keeper(self):
        return FileKeeper(self.folders)

    def mangle(self):
        root = self.xml.getroot()

        # check version
        if root.tag != 'spriter_data':
            self.make_error('bad tag on root')

        if root.attrib['scml_version'] != Parser.supported_version:
            self.make_error('unsupported version of Spriter - is %s, should be %s' % (root.attrib['scml_version'], Parser.supported_version))

        for elem in root:
            if elem.tag == 'folder':
                self.mangle_folder(elem)
            elif elem.tag == 'entity':
                self.mangle_entity(elem)
            else:
                self.make_error('unsupported tag: %s' % (elem.tag,))

    def prepare_entities(self):
        fk = self.get_file_keeper()

        outList = []
        for ent in self.entities.values():
            ent.set_file_keeper(fk)
            outList.append(ent)

        return outList

    def mangle_folder(self, node):
        f = Folder(node)
        self.folders[f.get_id()] = f

    def mangle_entity(self, node):
        e = Entity(node)
        self.entities[e.get_id()] = e

    def __str__(self):
        outList = []

        for elem in self.folders.values():
            outList.append(Utils.tabber(1, str(elem)))

        for elem in self.entities.values():
            outList.append(Utils.tabber(1, str(elem)))

        return '\n'.join(outList)
