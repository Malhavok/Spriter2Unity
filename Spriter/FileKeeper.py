__author__ = 'Malhavok'

class FileKeeper(object):
    def __init__(self, folderDict):
        self.folders = folderDict

    def get_file(self, folderId, fileId):
        if folderId not in self.folders:
            return None

        return self.folders[folderId].get_file(fileId)

    def get_file_list(self):
        outList = []

        for folder in self.folders.values():
            outList.extend(folder.get_file_list())

        return outList