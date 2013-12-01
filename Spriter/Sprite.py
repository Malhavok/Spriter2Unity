__author__ = 'Malhavok'

from Node import Node
import Utils
from Object import Object
from ObjectRef import ObjectRef

class Sprite(Node):
    def __init__(self, fk):
        super(self.__class__, self).__init__()

        self.fileKeeper = fk
        self.file = None

        self.pivot_x = 0.0
        self.pivot_y = 1.0

        self.alpha = 1.0
        self.z_index = 0

        self.objRef = None
        self.obj = None


    def get_z_index(self):
        return self.z_index

    def get_alpha(self):
        return self.alpha

    def get_pivot(self):
        return self.pivot_x, self.pivot_y

    def get_pivot_from_middle_pix_x(self):
        if file is None:
            return None
        midX = self.file.width / 2.0
        pivX = self.file.width * self.pivot_x
        return midX - pivX

    def get_pivot_from_middle_pix_y(self):
        if file is None:
            return None
        midY = self.file.height / 2.0
        pivY = self.file.height * self.pivot_y
        return midY - pivY

    def build(self, objectRef, timeline):
        # same as Node, but with object
        if objectRef.get_type() != ObjectRef.type:
            Utils.print_error('node didnt get objectref', [objectRef, timeline])

        self.objRef = objectRef
        self.z_index = objectRef.z_index
        timeIdx = objectRef.timeline
        timeKey = objectRef.key

        if timeIdx not in timeline:
            Utils.print_error('cant build node with given data', [objectRef, timeline])

        timeElem = timeline[timeIdx]
        self.name = timeElem.name

        if timeKey not in timeElem.keys:
            Utils.print_error('cant build node with given data', [objectRef, timeline, timeElem])

        finalKey = timeElem.keys[timeKey]
        obj = finalKey.get_object()

        if obj is None:
            Utils.print_error('cant build node - there is no object in key', [objectRef, timeline, timeElem, finalKey])

        if obj.get_type() != Object.type:
            Utils.print_error('Bone is not a bone', [objectRef, timeline, timeElem, finalKey, obj])

        # fill using data from object!
        self.file = self.fileKeeper.get_file(obj.folder, obj.file)

        self.name = self.name + '_(' + self.file.name.replace('/', '!') + ')'

        self.x = obj.x
        self.y = obj.y
        self.scale_x = obj.scale_x
        self.scale_y = obj.scale_y
        self.angle = obj.angle

        self.pivot_x = obj.pivot_x if obj.pivot_x is not None else self.file.pivot_x
        self.pivot_y = obj.pivot_y if obj.pivot_y is not None else self.file.pivot_y
        self.alpha = obj.alpha

        self.obj = obj

        return finalKey.time


    def __str__(self):
        outList = []

        fileName = '(None)' if self.file is None else self.file.name
        outList.append('Sprite (px: %f, py: %f, file: %s)' %\
                        (self.pivot_x, self.pivot_y, fileName))

        if self.obj is None:
            outList.append('\tObject: (None)')
        else:
            outList.append('\tObject:')
            outList.append(Utils.tabber(2, str(self.obj)))

        outList.append(Utils.tabber(1, super(self.__class__, self).__str__()))

        return '\n'.join(outList)
