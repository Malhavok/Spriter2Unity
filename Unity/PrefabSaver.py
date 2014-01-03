__author__ = 'Malhavok'

import codecs

class PrefabSaver(object):
    def __init__(self):
        self.object_list = []
        self.rootGO = -1

    def add_object(self, newGO, isRoot = False):
        self.object_list.append(newGO)
        if isRoot:
            self.rootGO = newGO.get_id()

    def get_prefab_info(self):
        if self.rootGO < 0:
            print 'ERROR: Unable to generate PREFAB header - no object marked as root'
            exit(1)

        outList = []

        outList.append('--- !u!1001 &100100000')
        outList.append('Prefab:')
        outList.append('  m_ObjectHideFlags: 1')
        outList.append('  serializedVersion: 2')
        outList.append('  m_Modification:')
        outList.append('    m_TransformParent: {fileID: 0}')
        outList.append('    m_Modifications: []')
        outList.append('    m_RemovedComponents: []')
        outList.append('  m_ParentPrefab: {fileID: 0}')
        outList.append('  m_RootGameObject: {fileID: 1%05d}' % (self.rootGO,))
        outList.append('  m_IsPrefabParent: 1')
        outList.append('  m_IsExploded: 1')

        return '\n'.join(outList)

    def to_string(self):
        componentMap = self.mangle()

        outList = []

        outList.append('%YAML 1.1')
        outList.append('%TAG !u! tag:unity3d.com,2011:')

        keys = componentMap.keys()
        for k in sorted(keys):
            cmp_list = componentMap[k]

            for elem in cmp_list:
                outList.append(elem.to_string())

        outList.append(self.get_prefab_info())

        return '\n'.join(outList)

    def save(self, filename):
        fullFilename = filename + '.prefab'

        with codecs.open(fullFilename, 'w', encoding='utf-8') as f:
            data = self.to_string()
            f.write(data)

    def mangle(self):
        outMap = {}

        for go in self.object_list:
            self.append_to_map(outMap, 1, go)

            for cmp in go.get_components():
                self.append_to_map(outMap, cmp.get_type(), cmp)

        return outMap

    def append_to_map(self, inOutMap, key, val):
        if key not in inOutMap:
            inOutMap[key] = []

        inOutMap[key].append(val)