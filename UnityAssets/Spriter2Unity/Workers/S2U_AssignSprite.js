#pragma strict

import System.IO;


/// \brief interface for chaning whole sprite list
///
/// ! WARNING
/// Internally uses Resources.Load, so you have to take care
/// of unloading useless resources yourself
///
/// Using this method you can point a folder within
/// some Resources directory to change all sprites
/// of this model with sprites from a given folder.
/// Missing sprites are replaced with null (empty, invisible sprites)
///
/// Example:
/// - you got directory "Assets/Resources/Textures/Skin1" and "Assets/Resources/Textures/Skin2"
/// - what you want to pass to this function is either "Textures/Skin1" or "Textures/Skin2"
///
/// \param[in] folderName		name of the directory to use sprites from
///								(have to be inside Resources directory)
///
function replaceFullWithFolder(folderName : String) : void
{
	replacePartWithFolder(folderName, null);
}

/// \brief interface for chaning part of a sprite list
///
/// ! WARNING
/// Internally uses Resources.Load, so you have to take care
/// of unloading useless resources yourself
///
/// Using this method you can point a folder within
/// some Resources directory to change some sprites
/// of this model with sprites from a given folder.
/// Missing sprites are replaced with null (empty, invisible sprites)
///
/// Example:
/// - you got directory "Assets/Resources/Textures/Skin1" and "Assets/Resources/Textures/Skin2"
/// - what you want to pass to this function is either "Textures/Skin1" or "Textures/Skin2"
///
/// Sprites to be replaced are picked via prefix of filename from Spriter.
/// So, if all your arms are placed in "arms" directory, you can replace all
/// of them using prefix "arms".
///
/// \param[in] folderName		name of the directory to use sprites from
///								(have to be inside Resources directory)
///
/// \param[in] prefixSpriteName	prefix for replacing only some sprites. It's matched
///								against file name from spriter (with directory, e.g.:
///								arms/left_arm.png will be matched to prefix "arms")
///
function replacePartWithFolder(folderName : String, prefixSpriteName : String) : void
{
	for (var elem : S2U_SpriteInfo in spriteList)
	{
		if (prefixSpriteName != null && ! elem.getSpriteName().StartsWith(prefixSpriteName))
			continue;
	
		var assetPathFull : String = Path.Combine(folderName, elem.getSpriteName());
		var dirName : String = Path.GetDirectoryName(assetPathFull);
		var fileNameNoExt : String = Path.GetFileNameWithoutExtension(assetPathFull);
		var assetPath : String = Path.Combine(dirName, fileNameNoExt);
		assetPath = pathToAssetPath(assetPath);
		
		var newSprite : Sprite = Resources.Load(assetPath, Sprite) as Sprite;
		
		elem.setSprite(newSprite);
	}
}


////////////////////////////////////////////////////////////////////////
/// THINGS THAT SHOULD BE PRIVATE BUT CAN'T BE PRIVATE
///
/// If you read anything below this point, you're asking
/// for programming troubles.
///

/// \brief changes windows path to unix path
///
/// This step is requires as Resources.Load requires / and wont work with \
///
private function pathToAssetPath(inFolder : String) : String
{
	return inFolder.Replace('\\', '/');
}

/// \brief internal data structure
///
/// Sadly, it have to be exposed, so i can fill everything when preparing prefabs
/// Consider it private for all purposes, do not touch it directly etc
/// as it may change without notice.
///
/// Used to store information about renderers and sprites that have to be assigned
/// to them. This allows custom character maps / retargettable animations.
///
class S2U_SpriteInfo
{
	var spriteName : String;
	var nodeName : String;

	var sprite : Sprite;

	// sadly, i cannot hide it as it's value will be lost
	var rend : SpriteRenderer;
	
	function getSpriteName() : String { return spriteName; }

	function setSprite(newSprite : Sprite) { sprite = newSprite; }
	
	function assign() : void
	{
		rend.sprite = sprite;
	}
}

/// \brief list of all sprites that can be "called" and changed
///
/// For all purposes consider this list PRIVATE and do NO assumptions about it
/// I'd love to moke it private but i can't if i want to fill it during prefab generation
///
var spriteList : S2U_SpriteInfo[];

/// \brief Function that changes sprites
///
/// This function is called in every generated animation. It changes sprites
/// to the one pointed by animation. All calls to this method are internal
/// and this method shouldn't be touched.
///
function S2UInternal_AssignSprite(idx : int) : void
{
	spriteList[idx].assign();
}
