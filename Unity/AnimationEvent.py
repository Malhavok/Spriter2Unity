__author__ = 'Malhavok'

class AnimationEvent(object):
    def __init__(self, time = 0.0):
        super(self.__class__, self).__init__()

        self.floatParam = None
        self.intParam = None
        self.strParam = None
        self.functionName = None
        self.time = time

    def set_time(self, newTime):
        self.time = newTime

    def set_int_function(self, funName, intVal):
        self.functionName = funName
        self.intParam = intVal

    def set_str_function(self, funName, strVal):
        self.functionName = funName
        self.strParam = strVal

    def to_string(self):
        outList = []

        outList.append('- time: %f' % (self.time,))
        outList.append('  functionName: %s' % (self.functionName,))

        if self.strParam is None:
            outList.append('  data:')
        else:
            outList.append('  data: %s' % (self.strParam,))

        outList.append('  objectReferenceParameter: {fileID: 0}')

        if self.floatParam is None:
            outList.append('  floatParameter: 0')
        else:
            outList.append('  floatParameter: %f' % (self.floatParam,))

        if self.intParam is None:
            outList.append('  intParameter: 0')
        else:
            outList.append('  intParameter: %d' % (self.intParam,))

        outList.append('  messageOptions: 0')

        return '\n'.join(outList)
