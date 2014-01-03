__author__ = 'Malhavok'

class File(object):
    def __init__(self, node):
        self.id = None
        self.name = None
        self.width = None
        self.height = None
        self.pivot_x = None
        self.pivot_y = None

        self.parse(node)

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def parse(self, node):
        self.id = int(node.attrib['id'])
        self.name = node.attrib['name']
        self.width = int(node.attrib['width'])
        self.height = int(node.attrib['height'])
        self.pivot_x = float(node.attrib.get('pivot_x', 0.0))
        self.pivot_y = float(node.attrib.get('pivot_y', 0.0))

    def __str__(self):
        return 'File (id: %d, name: %s, w: %d, h: %d, px: %f, py: %f)'\
                % (self.id, self.name, self.width, self.height, self.pivot_x, self.pivot_y)