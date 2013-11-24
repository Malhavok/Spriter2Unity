Spriter2Unity
=============

Tool that converts SCML files into unity .prefab and .anim files

This is a VERY early version and is probably NOT working well, but it'll be fixed over time. It requires python installed in your system (but no special or external library is needed). Generated prefab's and anim's are in Unity text mode, dunno yet how it'll behave in the long run.

What it does:
- for each entity in SCML file creates a Unity prefab
- for each animation in SCML file creates a Unity animation

Limitations (and why):
- it doesn't assign any sprites, only creates nodes with SpriteRenderer (1. Unity uses guid's to assign them and i know no way of obtaining these; 2. this way you can place all elements on as many/little atlases as you want and still use it)
- currently supports only Spriter b5 (because it was the "current" version when i started coding it)
- doesn't change sprites like Spriter does (for each file a new Unity Node is generated, and is disabled / enabled whenever needed)
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
- i was able to export test character from Spriter Asset pack with it
- i support a sample character (terrible! made it myself) as an example

What doesn't work:
- for some reason pickups ain't working... yet!

Current usage (from command line):

python main.py [name of the SCML to covert]
