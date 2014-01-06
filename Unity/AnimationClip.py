__author__ = 'Malhavok'

import math
import codecs

from CurveCalc import CurveCalc
from CurveCalcRot import CurveCalcRot
from CurveCalcInstant import CurveCalcInstant
from CurveCalcSprite import CurveCalcSprite
from Transform import Transform
from SpriteRenderer import SpriteRenderer
from GameObject import GameObject
from AnimationEvent import AnimationEvent

from MB_AssignSprite import MB_AssignSprite

import CurveParam
import CurveWorker
import Curves
import CurveSavers


class AnimationClip(object):
    def __init__(self, name, animTimeSec, baseGOList):
        self.name = name

        self.isLooped = True
        self.animTime = animTimeSec
        self.keyframes = {}

        # will not be touched!
        assert(len(baseGOList))
        self.baseGOList = baseGOList

        self.animationScript = self.find_animation_script()
        assert self.animationScript


    def set_looped(self, isLooped):
        self.isLooped = isLooped


    def add_key_frame(self, time, goList):
        self.keyframes[time] = goList


    def save(self):
        outName = self.name + '.anim'
        outStr = self.to_string()

        with codecs.open(outName, 'w', encoding='utf=8') as f:
            f.write(outStr)


    def find_animation_script(self):
        for go in self.baseGOList:
            script = go.get_mono_behaviour_by_guid(MB_AssignSprite.GUID)
            if not script:
                continue

            return script
        return None


    def add_final_keyframe(self):
        sortedTime = sorted(self.keyframes.keys())

        if self.isLooped:
            finalTime = sortedTime[0]
        else:
            finalTime = sortedTime[-1]

        self.keyframes[self.animTime] = self.keyframes[finalTime]


    def to_string(self):
        outList = []

        rotationCurves, editorRotData = self.calc_rotation_curves()
        positionCurves, editorPosData = self.calc_position_curves()
        scaleCurves, editorScaleData = self.calc_scale_curves()

        floatingCurves, editorFloatCurves = self.calc_active_curves()
        floatAlpha, editorFloatAlpha = self.calc_alpha_curves()

        eventCurves = self.calc_animation_events()

        outList.append('%YAML 1.1')
        outList.append('%TAG !u! tag:unity3d.com,2011:')
        outList.append('--- !u!74 &7400000')
        outList.append('AnimationClip:')
        outList.append('  m_ObjectHideFlags: 0')
        outList.append('  m_PrefabParentObject: {fileID: 0}')
        outList.append('  m_PrefabInternal: {fileID: 0}')
        outList.append('  m_Name: ' + self.name)
        outList.append('  serializedVersion: 4')
        outList.append('  m_AnimationType: 2')
        outList.append('  m_Compressed: 0')
        outList.append('  m_UseHighQualityCurve: 1')

        # place rotation curves here
        if rotationCurves is None:
            outList.append('  m_RotationCurves: []')
        else:
            outList.append('  m_RotationCurves:')
            outList.append(self.tabber(2, rotationCurves, ' '))

        outList.append('  m_CompressedRotationCurves: []')

        # place position curves here
        if positionCurves is None:
            outList.append('  m_PositionCurves: []')
        else:
            outList.append('  m_PositionCurves:')
            outList.append(self.tabber(2, positionCurves, ' '))

        # place scale curves here
        if scaleCurves is None:
            outList.append('  m_ScaleCurves: []')
        else:
            outList.append('  m_ScaleCurves:')
            outList.append(self.tabber(2, scaleCurves, ' '))

        # place floating curves here
        if floatingCurves is None and floatAlpha is None:
            outList.append('  m_FloatCurves: []')
        else:
            outList.append('  m_FloatCurves:')

            if floatingCurves is not None:
                outList.append(self.tabber(2, floatingCurves, ' '))

            if floatAlpha is not None:
                outList.append(self.tabber(2, floatAlpha, ' '))

        outList.append('  m_PPtrCurves: []')
        outList.append('  m_SampleRate: 60')
        outList.append('  m_WrapMode: 0')
        outList.append('  m_Bounds:')
        outList.append('    m_Center: {x: 0, y: 0, z: 0}')
        outList.append('    m_Extent: {x: 0, y: 0, z: 0}')
        outList.append('  m_AnimationClipSettings:')
        outList.append('    serializedVersion: 2')
        outList.append('    m_StartTime: 0')
        outList.append('    m_StopTime: ' + str(self.animTime))
        outList.append('    m_OrientationOffsetY: 0')
        outList.append('    m_Level: 0')
        outList.append('    m_CycleOffset: 0')
        outList.append('    m_LoopTime: ' + ('1' if self.isLooped else '0'))
        outList.append('    m_LoopBlend: 0')
        outList.append('    m_LoopBlendOrientation: 0')
        outList.append('    m_LoopBlendPositionY: 0')
        outList.append('    m_LoopBlendPositionXZ: 0')
        outList.append('    m_KeepOriginalOrientation: 0')
        outList.append('    m_KeepOriginalPositionY: 1')
        outList.append('    m_KeepOriginalPositionXZ: 0')
        outList.append('    m_HeightFromFeet: 0')
        outList.append('    m_Mirror: 0')

        # place editor curves here
        if editorPosData is None and editorScaleData is None and editorRotData is None and editorFloatCurves is None and editorFloatAlpha is None:
            outList.append('  m_EditorCurves: []')
        else:
            outList.append('  m_EditorCurves:')
            if editorRotData is not None:
                outList.append(self.tabber(2, editorRotData, ' '))
            if editorPosData is not None:
                outList.append(self.tabber(2, editorPosData, ' '))
            if editorScaleData is not None:
                outList.append(self.tabber(2, editorScaleData, ' '))
            if editorFloatCurves is not None:
                outList.append(self.tabber(2, editorFloatCurves, ' '))
            if editorFloatAlpha is not None:
                outList.append(self.tabber(2, editorFloatAlpha, ' '))

        # place euler editor curves here
        outList.append('  m_EulerEditorCurves: []')

        if eventCurves is None:
            outList.append('  m_Events: []')
        else:
            outList.append('  m_Events:')
            outList.append(self.tabber(2, eventCurves, ' '))

        return '\n'.join(outList)


    def calc_position_curves(self):
        if len(self.keyframes) == 0:
            return None

        xCurveParam = CurveParam.CurveParam('x', Curves.CurveLinear.CurveLinear)
        yCurveParam = CurveParam.CurveParam('y', Curves.CurveLinear.CurveLinear)
        zCurveParam = CurveParam.CurveParam('z', Curves.CurveInstant.CurveInstant)

        tsrWork = CurveWorker.CurveWorker(
            [xCurveParam, yCurveParam, zCurveParam],
            CurveSavers.TSRSaver.TSRSaver,
            Transform.type,
            'm_LocalPosition'
        )

        for t in self.keyframes.keys():
            for go in self.keyframes[t]:
                transform = go.get_component_of_type(Transform.type)
                tsrWork.add_key_frame(t, go.get_path(), 'z', transform.get_z_position())

                if not go.does_take_part_in_anim_calcs():
                    continue

                tsrWork.add_key_frame(t, go.get_path(), 'x', transform.get_x_position())
                tsrWork.add_key_frame(t, go.get_path(), 'y', transform.get_y_position())

        return tsrWork.to_string(), tsrWork.to_editor_string()


    def calc_rotation_curves(self):
        if len(self.keyframes) == 0:
            return None

        # the effect of this is creation of 3-dimensional quaternion for rotation around Z-axis
        # it's form is (0, 0, sin(angle)/2, cos(angle)/2)
        xCurveParam = CurveParam.CurveParam('x', Curves.CurveDummy.CurveDummy, curveClassCtorParams = (0.0,))
        yCurveParam = CurveParam.CurveParam('y', Curves.CurveDummy.CurveDummy, curveClassCtorParams = (0.0,))

        zCurveParam = CurveParam.CurveParam(
            'z',
            Curves.CurveLinearAngle.CurveLinearAngle,
            curveClassCtorParams = (lambda x: math.sin(x / 2.0), )
        )

        wCurveParam = CurveParam.CurveParam(
            'w',
            Curves.CurveLinearAngle.CurveLinearAngle,
            curveClassCtorParams = (lambda x: math.cos(x / 2.0), )
        )

        tsrWork = CurveWorker.CurveWorker(
            [xCurveParam, yCurveParam, zCurveParam, wCurveParam],
            CurveSavers.TSRSaver.TSRSaver,
            Transform.type,
            'm_LocalRotation',
            continuousTimeLine=True
        )

        for t in self.keyframes.keys():
            for go in self.keyframes[t]:
                transform = go.get_component_of_type(Transform.type)

                if not go.does_take_part_in_anim_calcs():
                    # tsrWork.add_time_frame(t)
                    continue

                tsrWork.add_key_frame(t, go.get_path(), 'z', transform.get_z_angle())
                tsrWork.add_key_frame(t, go.get_path(), 'w', transform.get_z_angle())

        return tsrWork.to_string(), tsrWork.to_editor_string()


    def calc_scale_curves(self):
        if len(self.keyframes) == 0:
            return None

        xCurveParam = CurveParam.CurveParam('x', Curves.CurveLinear.CurveLinear)
        yCurveParam = CurveParam.CurveParam('y', Curves.CurveLinear.CurveLinear)
        zCurveParam = CurveParam.CurveParam('z', Curves.CurveDummy.CurveDummy, curveClassCtorParams = (1.0,))

        tsrWork = CurveWorker.CurveWorker(
            [xCurveParam, yCurveParam, zCurveParam],
            CurveSavers.TSRSaver.TSRSaver,
            Transform.type,
            'm_LocalScale'
        )

        for t in self.keyframes.keys():
            for go in self.keyframes[t]:
                transform = go.get_component_of_type(Transform.type)

                if not go.does_take_part_in_anim_calcs():
                    continue

                tsrWork.add_key_frame(t, go.get_path(), 'x', transform.get_x_scale())
                tsrWork.add_key_frame(t, go.get_path(), 'y', transform.get_y_scale())

        return tsrWork.to_string(), tsrWork.to_editor_string()


    def calc_active_curves(self):
        if len(self.keyframes) == 0:
            return None

        curveParam = CurveParam.CurveParam(None, Curves.CurveInstant.CurveInstant)

        tsrWork = CurveWorker.CurveWorker(
            [curveParam],
            CurveSavers.FloatSaver.FloatSaver,
            GameObject.type,
            'm_IsActive'
        )

        for t in self.keyframes.keys():
            keyFramePaths = set()

            for go in self.keyframes[t]:
                go.set_active(True)
                keyFramePaths.add(go.get_path())
                tsrWork.add_key_frame(t, go.get_path(), None, go.is_active_as_int())

            # add all other objects in this gameobject, as disabled
            for go in self.baseGOList:
                if go.get_path() in keyFramePaths:
                    continue

                tsrWork.add_key_frame(t, go.get_path(), None, 0)

        return tsrWork.to_string(), tsrWork.to_editor_string()


    def calc_alpha_curves(self):
        if len(self.keyframes) == 0:
            return None

        curveParam = CurveParam.CurveParam('a', Curves.CurveLinear.CurveLinear)

        tsrWork = CurveWorker.CurveWorker(
            [curveParam],
            CurveSavers.FloatSaver.FloatSaver,
            SpriteRenderer.type,
            'm_Color'
        )

        for t in self.keyframes.keys():
            for go in self.keyframes[t]:
                if not go.does_take_part_in_anim_calcs():
                    continue
                sprite_renderer = go.get_component_of_type(SpriteRenderer.type)
                if sprite_renderer is None:
                    continue

                tsrWork.add_key_frame(t, go.get_path(), 'a', sprite_renderer.get_alpha())

        return tsrWork.to_string(), tsrWork.to_editor_string()


    def calc_animation_events(self):
        if len(self.keyframes) == 0:
            return None

        eventList = []

        for t in self.keyframes.keys():
            for go in self.keyframes[t]:
                if not go.does_take_part_in_anim_calcs():
                    continue
                sprite_renderer = go.get_component_of_type(SpriteRenderer.type)
                if sprite_renderer is None:
                    continue

                evt = AnimationEvent(t)
                animId = self.animationScript.get_idx_by_path_and_guid(go.get_path(), sprite_renderer.get_sprite_guid())
                if animId >= 0:
                    animMarker = '%s.%d' % (self.name, animId)
                    evt.set_str_function('S2UInternal_AssignSprite', animMarker)
                    eventList.append(evt.to_string())

        return '\n'.join(eventList)


    def tabber(self, num, text, ch = '\t'):
        split = text.splitlines()
        app = ch * num
        return app + ('\n' + app).join(split)