__author__ = 'Malhavok'

from KeyElem import KeyElem

class ObjectRef(KeyElem):
    type = 'object-ref'

    def __init__(self, node):
        super(self.__class__, self).__init__(ObjectRef.type)

        self.id = None
        self.parent = None
        self.timeline = None
        self.key = None
        self.z_index = None

        self.parse(node)

    def get_id(self):
        return self.id

    def get_parent(self):
        return self.parent

    def parse(self, node):
        self.id = int(node.attrib['id'])

        if 'parent' in node.attrib:
            self.parent = int(node.attrib['parent'])

        self.timeline = int(node.attrib['timeline'])
        self.key = int(node.attrib['key'])
        self.z_index = int(node.attrib['z_index'])

    def __str__(self):
        parent = self.parent
        if parent is None:
            parent = '(None)'

        return 'Object-ref (id: %d, parent: %s, timeline: %d, z_index: %d)'\
                % (self.id, str(parent), self.timeline, self.z_index)