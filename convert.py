__author__ = 'Malhavok'

import Unity
import Spriter
from PrefabMaker import PrefabMaker

import sys


def export_to_unity(scmlFile, unityDir):
    print 'Exporting', scmlFile
    parser = Spriter.Parser.Parser(scmlFile)
    parser.mangle()

    # prepare meta reader
    mr = Unity.MetaReader.MetaReader(unityDir)
    files = parser.get_file_keeper().get_file_list()
    for f in files:
        wasOK, reason = mr.check_file(f)
        if not wasOK:
            print 'Warning -', reason

    # prepare entities
    entities = parser.prepare_entities()

    # do all entities
    for entity in entities:
        pm = PrefabMaker(mr)
        pm.make_prefab(entity)

        numAnim = entity.get_num_anims()
        for animId in xrange(numAnim):
            anim = entity.get_anim(animId)
            num_frames = anim.get_num_key_frames()

            ac = Unity.AnimationClip.AnimationClip(anim.get_name(), anim.get_time(), pm.get_prefab_go_list())

            for idx in xrange(num_frames):
                kf = anim.get_key_frame(idx)

                tmpPM = PrefabMaker(mr)
                tmpPM.generate_game_objects(entity, animId, idx)

                ac.add_key_frame(kf.get_time(), tmpPM.get_game_object_list())

            ac.save()


if len(sys.argv) < 3:
    print 'Usage:', sys.argv, '[SCML file] [Unity directory with textures]'
    print '\tConverts SCML file into prefab and animations'
    print '\tUses textures from given directory to properly assign sprites to nodes'
    exit(1)

export_to_unity(sys.argv[1], sys.argv[2])
