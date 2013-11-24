__author__ = 'Malhavok'

class Component(object):
    def __init__(self, TYPE, ID):
        self.type = TYPE
        self.id = ID
        self.gameObjectId = 0

    def get_type(self):
        return self.type

    def get_id(self):
        return self.id

    def set_game_object(self, objectId):
        self.gameObjectId = objectId

    def get_mark_string(self):
        return '- %d: {fileID: %d%05d}' % (self.type, self.type, self.id)
