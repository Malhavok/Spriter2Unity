__author__ = 'Malhavok'

from Component import Component

class MonoBehaviour(Component):
    globalId = 0
    type = 114

    def __init__(self, GUID):
        # as it can be inherited, i have to point MonoBehaviour as the class type
        # otherwise it'd try to call MonoBehaviour super instead
        super(MonoBehaviour, self).__init__(MonoBehaviour.type, MonoBehaviour.globalId)
        MonoBehaviour.globalId += 2

        # global unique ID for script that have to be attached
        self.GUID = GUID

    def get_guid(self):
        return self.GUID

    def to_string_params(self):
        # fill this to assign values to scripts
        # each param name have to start with 2 spaces and go 2 spaces deeper
        # for sub-params
        return ''

    def to_string(self):
        outList = []

        outList.append('--- !u!%d &%d%05d' % (self.get_type(), self.get_type(), self.get_id()))
        outList.append('MonoBehaviour:')
        outList.append('  m_ObjectHideFlags: 1')
        outList.append('  m_PrefabParentObject: {fileID: 0}')
        outList.append('  m_PrefabInternal: {fileID: 100100000}')
        outList.append('  m_GameObject: {fileID: 1%05d}' % (self.gameObjectId,))
        outList.append('  m_Enabled: 1')
        outList.append('  m_EditorHideFlags: 0')
        outList.append('  m_Script: {fileID: 11500000, guid: %s, type: 3}' % (self.GUID,))
        outList.append('  m_Name:')
        outList.append('  m_EditorClassIdentifier:')

        outList.append(self.to_string_params())

        return '\n'.join(outList)