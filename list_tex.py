__author__ = 'Malhavok'

import Spriter
import sys


def check_req_files(scmlFile):
    parser = Spriter.Parser.Parser(scmlFile)
    parser.mangle()

    fk = parser.get_file_keeper()
    return fk.get_file_list()


if len(sys.argv) < 2:
    print 'Usage:', sys.argv, '[SCML file]'
    print '\tLists all textures used in scml file.'
    exit(1)

print 'Checking required resources...'
files = check_req_files(sys.argv[1])
print '\n'.join(files)
