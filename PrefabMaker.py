__author__ = 'Malhavok'

import math
import Unity
from Unity import Consts as UC
from Spriter import Node, Sprite

class PrefabMaker(object):
    def __init__(self, metaReader = None):
        self.go_map = {}
        self.saver = Unity.PrefabSaver.PrefabSaver()
        self.metaReader = metaReader
        self.spriteAssigner = Unity.MB_AssignSprite.MB_AssignSprite()

    def get_game_object_list(self):
        return self.go_map.values()

    def get_prefab_go_list(self):
        return self.saver.object_list

    def generate_game_objects(self, entity, animId, keyFrameId, newBeDisabled = False):
        anim = entity.get_anim(animId)
        keyFrame = anim.get_key_frame(keyFrameId)

        entityNode = Node.Node()
        entityNode.name = entity.get_name()

        for elem in keyFrame.nodes:
            entityNode.add_child(elem)

        self.mangle(entityNode, None, None, newBeDisabled)

        # clearing parent, just in case someone wants to use it again
        for elem in keyFrame.nodes:
            elem.detach_from_parent()

    def make_prefab(self, entity):
        # i assume there is at least one anim and one frame
        numAnims = entity.get_num_anims()
        self.generate_game_objects(entity, 0, 0)

        for animId in xrange(numAnims):
            anim = entity.get_anim(animId)
            numFrames = anim.get_num_key_frames()

            startFrame = 1 if animId == 0 else 0

            if startFrame >= numFrames:
                continue

            for frameId in xrange(startFrame, numFrames):
                self.generate_game_objects(entity, animId, frameId, True)

        # attach sprite script to the main GO
        self.fix_sprite_assigner()
        self.go_map[None].add_component(self.spriteAssigner)

        for path in self.go_map.keys():
            self.saver.add_object(self.go_map[path], path is None)

        self.saver.save(entity.get_name())

    def fix_sprite_assigner(self):
        for go in self.go_map.values():
            sr = go.get_component_of_type(Unity.SpriteRenderer.SpriteRenderer.type)
            if sr is None:
                continue

            self.spriteAssigner.set_path_renderer(go.get_path(), sr.get_id())

        self.spriteAssigner.optimize()

    def mangle(self, node, parent, parent_node, newBeDisabled = False):
        # this is a node of some type
        # make game object out of it
        # !!!! this requires HEAVY refactoring to make it
        # !!!! easier to understand and modify
        go = Unity.GameObject.GameObject(node.get_name())
        go.set_takes_part_in_anim_calcs(node.get_active())

        sinA = math.sin(node.get_angle())
        cosA = math.cos(node.get_angle())

        x = node.get_pos_x()
        y = node.get_pos_y()
        z = 0.0

        sx = node.get_scale_x()
        sy = node.get_scale_y()

        if parent_node is not None:
            sx *= parent_node.get_scale_x()
            sy *= parent_node.get_scale_y()

        if parent is not None:
            parent.add_child(go)

        x *= (sx / node.get_scale_x())
        y *= (sy / node.get_scale_y())

        if node.__class__ == Sprite.Sprite:
            px = node.get_pivot_from_middle_pix_x() * sx
            py = node.get_pivot_from_middle_pix_y() * sy

            rotPX = px * cosA - py * sinA
            rotPY = px * sinA + py * cosA

            x += rotPX
            y += rotPY

            # this solves Z-sorting problem in a less aggressive way
            # if the value is big enough it solves z-fighting problems
            # Unity imports this as 1/100, multiplying by 10 seems fine
            # to solve f-fighting problem (and won't require moving the default camera)
            z = -float(node.get_z_index() * 10.0)

            sr = Unity.SpriteRenderer.SpriteRenderer()
            sr.set_render_group(node.get_z_index())
            sr.set_alpha(node.get_alpha())

            if self.metaReader:
                sr.set_sprite_guid(self.metaReader.get_guid(node.get_file().get_name()))

            self.spriteAssigner.add_sprite(node.get_file().get_name(), go.get_path(), sr.get_sprite_guid())

            go.add_component(sr)


        transform = go.get_component_of_type(Unity.Transform.Transform.type)
        transform.set_position(x * UC.PixelScale, y * UC.PixelScale, z * UC.PixelScale)
        transform.set_z_rot(node.get_angle())

        if node.__class__ == Sprite.Sprite:
            transform.set_scale(sx, sy, 1.0)
            #transform.set_scale(node.get_scale_x(), node.get_scale_y(), 1.0)
        else:
            transform.set_scale(1.0, 1.0, 1.0)

        node.scale_x = sx
        node.scale_y = sy

        if go.get_path() not in self.go_map:
            go.set_active(not newBeDisabled)

            # get current parent for that object and parent it
            if not (go.get_path() is None and go.get_parent_path() is None):
                self.go_map[go.get_parent_path()].add_child(go)

            self.go_map[go.get_path()] = go

        for subNode in node.get_children():
            self.mangle(subNode, go, node, newBeDisabled)

