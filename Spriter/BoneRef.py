__author__ = 'Malhavok'

from KeyElem import KeyElem

class BoneRef(KeyElem):
    type = 'bone-ref'

    def __init__(self, node):
        super(self.__class__, self).__init__(BoneRef.type)

        self.id = None
        self.parent = None
        self.timeline = None
        self.key = None

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

    def __str__(self):
        parent = self.parent
        if parent is None:
            parent = '(None)'

        return 'Bone-ref (id: %d, parent: %s, timeline: %d, key: %d)'\
                % (self.id, str(parent), self.timeline, self.key)