__author__ = 'Malhavok'

class FileKeeper(object):
    def __init__(self, folderDict):
        self.folders = folderDict

    def get_file(self, folderId, fileId):
        if folderId not in self.folders:
            return None

        return self.folders[folderId].get_file(fileId)
