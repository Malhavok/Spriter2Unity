Spriter2Unity
=============

Tool that converts SCML files into unity .prefab and .anim files

This is an early version and is probably NOT working well, but it'll be fixed over time. It requires python installed in your system (but no special or external library is needed). Generated prefab's and anim's are in Unity text mode, dunno yet how it'll behave in the long run.

NOTICE
======

Another major change. Whole system for calculating curves for Unity was redesigned. It may still be a bit buggy,
whenever you notice anything big - let me know, i'll try to fix it ASAP.

Each time using Spriter2Unity copy content of UnityAssets directory into your own project Asset directory.
This means, that after operation you should have [unity project]/Assets/Spriter2Unity/ directory with some
weird stuff inside.

Remember, that every time you're downloading a new version you have to export all your animations again
and you have to update your project with newest scripts from UnityAssets directory. Without this steps
nothing can work for sure.

About
=====

What it does:
- for each entity in SCML file creates a Unity prefab
- each entity got it's sprites assigned as long as you imported these sprites before conversion
- for each animation in SCML file creates a Unity animation
- sprites are changed during animations, so only 1 SpriteRenderer is used for each node in the spriter file
- animations are changing sprites via script function call, so animations are 100% retargetable

Limitations (and why):
- currently supports only Spriter b5 (because it was the "current" version when i started coding it)
- probably much more (but i didn't have time to test it enough)

Why this way:
- you get a Unity prefab, which behaves exactly like the ones created normally
- you get animations and can use them with Unity Animators (state machine)
- you get animations and thus you can modify them in Unity, e.g.: adding script events to different parts of animations

Roadmap:
- making sure it works properly for everything in b5
- adding some stuff from b6 when available (hit-boxes, spawn-points) (but i WON'T add mesh deformation)
- making it more user-friendly

What works:
- was able to export test character from Spriter free Asset pack with it
- a sample character (terrible! made it myself) as an example
- pickups from Spriter essential art pack
- character maps / retargetable animations (you can replace whole / part of the character at runtime)

What doesn't work:
- object-refs with some abs positions/pivots/scales etc - didn't see a reason so far to use them...

Note:
- copy content of UnityAssets to your Assets directory
- set pivot in Unity to Center (the default one). All pivot calculations are taken care of internally
- import all Sprites BEFORE even calling convert
- you HAVE TO set Editor option for metafiles to "visible" (you'd like that for any version control anyway)
- requires python 2.7, doesn't work with python 3.0
- (deprecated, but still nice) before using you may want to watch this: http://www.youtube.com/watch?v=pZK86lQU8ME (thanks to Edgar from www.brashmonkey.com for this video)

Current usage (from command line):

python list_tex.py [name of the SCML]
- lists all textures required for this scml file

python list_unity_tex.py [name of the SCML] [Unity directory]
- checks are all textures from Unity were exported correctly (have guid assigned already)

python convert.py [name of the SCML to covert] [Unity folder with textures that match these required]
- this converts scml file into prefab and anims
