__author__ = 'Malhavok'

from MonoBehaviour import MonoBehaviour
from SpriteRenderer import SpriteRenderer

class MB_AssignSprite(MonoBehaviour):
    # all GUIDs are defined purely on their position
    # inside assets folder. so if user places my script directory
    # exactly where is want, i can use my GUIDs and not bother him any more
    GUID = '99fd3c019d4a14ac88074a420bba7c77'

    class Helper:
        def __init__(self, spriteName, pathName, spriteGUID):
            self.spriteName = spriteName
            self.pathName = pathName
            self.spriteGUID = spriteGUID
            self.rendererID = None

        def assign_renderer(self, rendererID):
            self.rendererID = rendererID

        def get_path(self):
            return self.pathName

        def get_sprite_guid(self):
            return self.spriteGUID

        def __eq__(self, other):
            if self.spriteName != other.spriteName:
                return False
            if self.pathName != other.pathName:
                return False
            if self.spriteGUID != other.spriteGUID:
                return False
            if self.rendererID != other.rendererID:
                return False

            return True

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

    def add_sprite(self, spriteName, pathName, spriteGUID):
        self.spriteList.append(MB_AssignSprite.Helper(spriteName, pathName, spriteGUID))

    def get_idx_by_path_and_guid(self, pathName, spriteGUID):
        for idx in xrange(len(self.spriteList)):
            if self.spriteList[idx].get_path() != pathName:
                continue

            if self.spriteList[idx].get_sprite_guid() != spriteGUID:
                continue

            return idx
        return -1

    def set_path_renderer(self, pathName, rendererID):
        for elem in self.spriteList:
            if elem.get_path() != pathName:
                continue

            elem.assign_renderer(rendererID)

    def optimize(self):
        # remove duplicated entries
        outList = []

        # simple O(n^2) search
        for elem in self.spriteList:
            isSame = False

            for tmpElem in outList:
                if elem == tmpElem:
                    isSame = True
                    break

            if isSame:
                continue

            outList.append(elem)

        self.spriteList = outList

    def to_string_params(self):
        outList = []

        # assumption is made that at least one sprite is placed here
        # but... there are no objects without at least one sprite
        # so that should not be a problem
        outList.append('  spriteList:')

        for elem in self.spriteList:
            outList.append(elem.to_string())

        return '\n'.join(outList)
