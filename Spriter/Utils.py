__author__ = 'Malhavok'

def tabber(num, text, ch = '\t'):
    split = text.splitlines()
    app = ch * num
    return app + ('\n' + app).join(split)


def print_error(msg, objs):
    print 'ERROR:', msg

    for o in objs:
        print '----', o.__class__, '----'
        print o

    exit(1)