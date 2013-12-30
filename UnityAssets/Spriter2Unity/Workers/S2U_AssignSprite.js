#pragma strict

import System.IO;
import System.Text.RegularExpressions;

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

/// \brief internal data structure
///
/// This one parses incomming animation marker
/// in form "string.number" into animation name
/// and animation index.
///
/// sadly, it seems that unity doesn't support
/// compiled regexs so it can be slower than
/// it should :/
///
class S2U_MarkerReader extends Object
{
	static private var regex : Regex;

	private var animName : String;
	private var animIdx : int;
	
	function S2U_MarkerReader(marker : String)
	{
		if (! regex)
		{
			// sadly, in unity, regex cannot be "compiled"
			regex = Regex("^(.*)\\.(\\d+)$");
		}
	
		var regexRes : String[] = regex.Split(marker);
		
		if (regexRes.Length != 4)
			Debug.LogError("Wrong length of the marker regex split: " + regexRes.Length);
			
		animName = regexRes[1];
		// this will throw an exception on error
		animIdx = int.Parse(regexRes[2]);
	}
	
	function getAnimName() : String { return animName; }
	function getAnimIdx() : int { return animIdx; }
}

/// \brief internal data structure
///
/// IF you're using animator (and you know you should)
/// this checks whether animation events during transitions
/// are comming ONLY from the "next" animation and not
/// the current one
///
/// There is a lot of assumptions in here:
/// - layer that is checked for transitions and animations
///   is only one, defined by layerToCheck variable
/// - it also assumes that name of the layerToCheck doesn't
///   change during runtime and is cached on first "check"
/// - assumes that this site:
///   http://docs.unity3d.com/Documentation/ScriptReference/AnimatorStateInfo.IsName.html
///   is up to date (and it seems so)
///
/// Whenever there is transition a check is made for each marker
/// if the marker doesn't belong to the "next" animation, it is
/// skipped, so it doesn't change sprites. In most other cases
/// it should fail-fast and allow sprite changing.
///
/// sidenote: i'm kinda worried about performance of this one :/
///           it may get messy with ~300 sprites on the screen at once
///           and that's not an unreasonable number :/
///
class S2U_TransitionChecker extends Object
{
	private var layerToCheck : int = 0;
	private var baseGO : GameObject;

	private var hasAnimator : boolean = true;
	private var animator : Animator = null;
	private var layerName : String;

	function S2U_TransitionChecker(go : GameObject)
	{
		baseGO = go;
	}
	
	function check(markerReader : S2U_MarkerReader) : boolean
	{
		if (! hasAnimator)
			return true;
			
		if (animator == null && ! prepareAnimator())
			return true;
	
		if (! animator.IsInTransition(layerToCheck))
			return true;
	
		var nextState : AnimatorStateInfo = animator.GetNextAnimatorStateInfo(0);
		var animStateName : String = layerName + "." + markerReader.getAnimName();
		
		if (! nextState.IsName(animStateName))
			return false;

		return true;
	}
	
	private function prepareAnimator() : boolean
	{
		animator = baseGO.GetComponent(Animator) as Animator;
		hasAnimator = animator != null;

		if (! hasAnimator)
			return false;
	
		// cached for checks
		layerName = animator.GetLayerName(layerToCheck);
	
		return true;
	}
}

/// \brief list of all sprites that can be "called" and changed
///
/// For all purposes consider this list PRIVATE and do NO assumptions about it
/// I'd love to moke it private but i can't if i want to fill it during prefab generation
///
var spriteList : S2U_SpriteInfo[];

/// \brief instance used to check whether animation event should be accepted
///
private var transitionChecker : S2U_TransitionChecker;


/// \brief initializer
///
/// Prepares data structure used to control transition animation events
///
function Start()
{
	transitionChecker = S2U_TransitionChecker(gameObject);
}

/// \brief Function that changes sprites
///
/// This function is called in every generated animation. It changes sprites
/// to the one pointed by animation. All calls to this method are internal
/// and this method shouldn't be touched.
///
function S2UInternal_AssignSprite(marker : String) : void
{
	var markerReader : S2U_MarkerReader = S2U_MarkerReader(marker);
	if (! transitionChecker.check(markerReader))
		return;

	spriteList[markerReader.getAnimIdx()].assign();
}
