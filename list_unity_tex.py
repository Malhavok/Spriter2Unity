__author__ = 'Malhavok'

import Spriter
import Unity
import sys


def check_req_files(scmlFile):
    parser = Spriter.Parser.Parser(scmlFile)
    parser.mangle()

    fk = parser.get_file_keeper()
    return fk.get_file_list()


if len(sys.argv) < 3:
    print 'Usage:', sys.argv, '[SCML file] [Unity directory with sprites]'
    print '\tChecks whether given Unity directory contains all required files.'
    print '\tRemember that it is required to turn on Visible Meta files in unity Editor settings.'
    exit(1)

print 'Checking required resources...'
files = check_req_files(sys.argv[1])
print 'Checking provided unity folder'
metaReader = Unity.MetaReader.MetaReader(sys.argv[2])

for f in files:
    print 'Checking file', f, '--',
    wasOk, resp = metaReader.check_file(f)

    if wasOk:
        print 'OK -', resp
    else:
        print 'Warning -', resp
