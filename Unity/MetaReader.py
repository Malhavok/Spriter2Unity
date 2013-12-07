__author__ = 'Malhavok'

import os

class MetaReader(object):
    def __init__(self, unityDir):
        self.guids = {}
        self.unityDir = unityDir

    def check_file(self, filename):
        fullPath = os.path.join(self.unityDir, filename)
        # we're looking for meta file
        if not fullPath.endswith('.meta'):
            fullPath = '%s.meta' % fullPath

        if not os.path.exists(fullPath):
            return False, 'Path "%s" doesnt exist' % (fullPath,)

        if not os.path.isfile(fullPath):
            return False, 'Path "%s" is not a file' % (fullPath,)

        # reading just 4kb, safety switch for some screwed up cases. i haven't seen unity meta for file above
        # 1kb but i need like 2 or 3 lines from it.
        with open(fullPath, 'r') as f:
            data = f.read(4096).splitlines()

        # i could use here json parser to do this, but i don't want any external dependencies
        # for most ppl installing python is more than bad and forcing them to install anything more - impossible
        # but, with a fat assumption, we can go with that
        GUID_MARKER = 'guid: '
        for line in data:
            if not line.startswith(GUID_MARKER):
                continue

            guid = line[len(GUID_MARKER):]
            self.guids[filename] = guid
            return True, 'GUID found: "%s"' % (guid,)

        # return from inside for loop