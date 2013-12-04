__author__ = 'Malhavok'

from Component import Component

class SpriteRenderer(Component):
    globalId = 0
    type = 212

    def __init__(self):
        super(self.__class__, self).__init__(SpriteRenderer.type, SpriteRenderer.globalId)
        SpriteRenderer.globalId += 2

        self.render_group = 0
        self.alpha = 1.0

    def set_render_group(self, rg):
        self.render_group = rg

    def set_alpha(self, newVal):
        self.alpha = newVal

    def get_alpha(self):
        return self.alpha

    def to_string(self):
        outList = []

        outList.append('--- !u!%d &%d%05d' % (self.get_type(), self.get_type(), self.get_id()))
        outList.append('SpriteRenderer:')
        outList.append('  m_ObjectHideFlags: 1')
        outList.append('  m_PrefabParentObject: {fileID: 0}')
        outList.append('  m_PrefabInternal: {fileID: 100100000}')
        outList.append('  m_GameObject: {fileID: 1%05d}' % (self.gameObjectId,))
        outList.append('  m_Enabled: 1')
        outList.append('  m_CastShadows: 0')
        outList.append('  m_ReceiveShadows: 0')
        outList.append('  m_LightmapIndex: 255')
        outList.append('  m_LightmapTilingOffset: {x: 1, y: 1, z: 0, w: 0}')
        outList.append('  m_Materials:')
        # now some magical mumbo-jumbo value, Sprite-default material it should be
        outList.append('  - {fileID: 10754, guid: 0000000000000000e000000000000000, type: 0}')
        outList.append('  m_SubsetIndices:') # i found it empty in a test prefab
        outList.append('  m_StaticBatchRoot: {fileID: 0}')
        outList.append('  m_UseLightProbes: 0')
        outList.append('  m_LightProbeAnchor: {fileID: 0}')
        outList.append('  m_ScaleInLightmap: 1')
        outList.append('  m_SortingLayer: 0')
        outList.append('  m_SortingOrder: %d' % (self.render_group,))
        outList.append('  m_SortingLayerID: 0')
        outList.append('  m_Sprite: {fileID: 0}')
        outList.append('  m_Color: {r: 1, g: 1, b: 1, a: 1}')

        return '\n'.join(outList)
