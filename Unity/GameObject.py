__author__ = 'Malhavok'

from Transform import Transform

class GameObject(object):
    globalId = 0
    type = 1

    def __init__(self, name = 'obj'):
        self.id = GameObject.globalId
        GameObject.globalId += 2

        self.name = name
        self.isActive = True
        self.components = []

        self.path = None

        self.add_component(Transform())

    def set_active(self, isActive):
        self.isActive = isActive

    def is_active(self):
        return self.isActive

    def is_active_as_int(self):
        return 1 if self.isActive else 0

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_path(self):
        return self.path

    def get_parent_path(self):
        if self.path is None:
            return None

        edx = self.path.rfind('/')
        if edx == -1:
            return None

        return self.path[:edx]

    def add_child(self, newGO):
        # the base game object is the one animations are attached to
        # so he can't show up in these paths
        myTransform = self.get_component_of_type(Transform.type)
        childTransform = newGO.get_component_of_type(Transform.type)

        if myTransform is None or childTransform is None:
            print 'ERROR: game object has no transform'
            exit(1)

        if not myTransform.add_child(childTransform):
            return

        if self.get_path() is None:
            newGO.path = newGO.get_name()
        else:
            newGO.path = self.get_path() + '/' + newGO.get_name()


    def add_component(self, newComponent):
        newComponent.set_game_object(self.id)
        self.components.append(newComponent)

    def get_components(self):
        return self.components

    def get_component_of_type(self, type):
        for cmp in self.components:
            if cmp.get_type() == type:
                return cmp
        return None

    def to_string(self):
        # this was taken from one of the unity prefabs
        outList = []

        outList.append('--- !u!1 &1%05d' % (self.id,))
        outList.append('GameObject:')
        outList.append('  m_ObjectHideFlags: 0')
        outList.append('  m_PrefabParentObject: {fileID: 0}')
        outList.append('  m_PrefabInternal: {fileID: 100100000}')
        outList.append('  serializedVersion: 4')

        # this is the tricky part, as empty lists in YAML are written differently
        # BUT! all objects in Unity have to have AT LEAST transform, so i'm not worrying about it here
        outList.append('  m_Component:')
        for cmp in self.components:
            outList.append('  ' + cmp.get_mark_string())

        outList.append('  m_Layer: 0')
        outList.append('  m_Name: ' + self.name)
        outList.append('  m_TagString: Untagged')
        outList.append('  m_Icon: {fileID: 0}')
        outList.append('  m_NavMeshLayer: 0')
        outList.append('  m_StaticEditorFlags: 0')
        outList.append('  m_IsActive: ' + str('1' if self.isActive else '0'))

        return '\n'.join(outList)
