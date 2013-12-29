__author__ = 'Malhavok'

from MonoBehaviour import MonoBehaviour
from SpriteRenderer import SpriteRenderer

class MB_AssignSprite(MonoBehaviour):
    # all GUIDs are defined purely on their position
    # inside assets folder. so if user places my script directory
    # exactly where is want, i can use my GUIDs and not bother him any more
    GUID = '99fd3c019d4a14ac88074a420bba7c77'

    class Helper:
        def __init__(self, spriteName, pathName, spriteGUID, spriteRendererID):
            self.spriteName = spriteName
            self.pathName = pathName
            self.spriteGUID = spriteGUID
            self.rendererID = spriteRendererID

        def to_string(self):
            outList = []

            outList.append('  - spriteName: %s' % (self.spriteName,))
            outList.append('    nodeName: %s' % (self.pathName,))
            outList.append('    sprite: {fileID: 21300000, guid: %s, type: 3}' % (self.spriteGUID,))
            outList.append('    rend: {fileID: %d%05d}' % (SpriteRenderer.type, self.rendererID))

            return '\n'.join(outList)

    def __init__(self):
        super(self.__class__, self).__init__(MB_AssignSprite.GUID)
        self.spriteList = []

    def add_sprite(self, spriteName, pathName, spriteGUID, spriteRendererID):
        self.spriteList.append(MB_AssignSprite.Helper(spriteName, pathName, spriteGUID, spriteRendererID))

    def to_string_params(self):
        outList = []

        # assumption is made that at least one sprite is placed here
        # but... there are no objects without at least one sprite
        # so that should not be a problem
        outList.append('  spriteList:')

        for elem in self.spriteList:
            outList.append(elem.to_string())

        return '\n'.join(outList)
