__author__ = 'Malhavok'

import Unity
import Spriter
from PrefabMaker import PrefabMaker

import sys


def export_to_unity(scmlFile):
    print 'Exporting', scmlFile
    parser = Spriter.Parser.Parser(scmlFile)
    parser.mangle()

    entities = parser.prepare_entities()

    for entity in entities:
        pm = PrefabMaker()
        pm.make_prefab(entity)

        numAnim = entity.get_num_anims()
        for animId in xrange(numAnim):
            anim = entity.get_anim(animId)
            num_frames = anim.get_num_key_frames()

            ac = Unity.AnimationClip.AnimationClip(anim.get_name(), anim.get_time(), pm.get_prefab_go_list())

            for idx in xrange(num_frames):
                kf = anim.get_key_frame(idx)

                tmpPM = PrefabMaker()
                tmpPM.generate_game_objects(entity, animId, idx)

                ac.add_key_frame(kf.get_time(), tmpPM.get_game_object_list())

            ac.save()


#export_to_unity('support_files/Crabby1.scml')
export_to_unity('support_files/s_chara.scml')

#if len(sys.argv) < 2:
#    print 'Usage:', sys.argv, '[SCML file]'
#    print '\tConverts SCML file into prefab and animations'
#    exit(1)
#
#export_to_unity(sys.argv[1])