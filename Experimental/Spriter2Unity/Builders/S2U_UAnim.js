#pragma strict

import System.IO;
import System.Text;

class S2U_UAnim extends Object
{
	private var folders : S2U_Folders;
	private var prefabGO : GameObject;

	function S2U_UAnim(folders_ : S2U_Folders)
	{
		folders = folders_;
		
	}
	
	function prepare(entity : S2U_Entity, prefab : GameObject, destDirectory : String)
	{
		prefabGO = prefab;
		var allAnim : Dictionary.<int, S2U_Animation> = entity.getAnimations();
		
		for (var tmpAnim : S2U_Animation in allAnim.Values)
		{
			var clip : AnimationClip = makeAnim(tmpAnim);
			saveClip(clip, destDirectory);
		}
	}
	
	
	private function makeAnim(anim : S2U_Animation) : AnimationClip
	{
		// Unity likes to get whole curves at a time, i like it frame at a time
		// so here's the creator that'll help me with my tasks
		var curveCreator : S2U_CurveCreator = S2U_CurveCreator();

		var mainline : S2U_Mainline = anim.getMainline();
		var mainlineKeys : List.<S2U_Key> = mainline.getSortedKeys();
		var helper : S2U_Prefab = S2U_Prefab(folders);

		for (var key : S2U_Key in mainlineKeys)
		{
			helper.fakeStart(prefabGO.name);
			helper.generateGOFromFrame(key.getRefList(), anim, key.getTime(), true);
			var helperGO : GameObject = helper.getRoot();

			addDiffToClip(curveCreator, helperGO, key.getTime());
			
			GameObject.DestroyImmediate(helperGO);
		}

		return curveCreator.getAnimation(anim.getName());
	}
	
	private function addDiffToClip(output : S2U_CurveCreator, helperGO : GameObject, time : float)
	{
		// if any game object has set isStatic this means that for the animation it should be marked
		// as active, but it's attributes ain't changing
		
		// what is to be animated: Transform (whole), SpriteRenderer color.a, SpriteRenderer sprite, GameObject active
		// active is like float, 0/1
		// except for sprite everything else is a float
		// sprite is weird, will take a moment to figure out
		var rootDict : Dictionary.<String, GameObject> = new Dictionary.<String, GameObject>();
		var helperDict : Dictionary.<String, GameObject> = new Dictionary.<String, GameObject>();
		
		splitObjectIntoDict(rootDict, prefabGO);
		splitObjectIntoDict(helperDict, helperGO);
		
		var curveCreator : S2U_CurveCreator = S2U_CurveCreator();
		
		for (var key : String in rootDict.Keys)
		{
			if (! helperDict.ContainsKey(key))
			{
				addToClip_GOActive(output, time, key, false);
				continue;
			}
			
			var go : GameObject = helperDict[key];
			addToClip_GOActive(output, time, key, true);

			if (go.isStatic)
				continue;
				
			// yay! we can add a normal keyframe!
			addToClip_Transform(output, time, key, go.transform);
			
			var spriteRenderer : SpriteRenderer = go.GetComponent(SpriteRenderer) as SpriteRenderer;
			if (spriteRenderer)
				addToClip_SpriteRenderer(output, time, key, spriteRenderer);
		}
	}
	
	private function addToClip_GOActive(outCC : S2U_CurveCreator, time : float, path : String, isActive : boolean)
	{
		var tmpCurve : AnimationCurve = outCC.getCurve(path, 'm_IsActive', GameObject);
		tmpCurve.AddKey(Keyframe(time, isActive ? 1.0f : 0.0f, Mathf.Infinity, Mathf.Infinity));
	}

	private function addToClip_Transform(outCC : S2U_CurveCreator, time : float, path : String, trans : Transform)
	{
		// positions
		var posX : AnimationCurve = outCC.getCurve(path, 'localPosition.x', Transform);
		posX.AddKey(Keyframe(time, trans.localPosition.x, Mathf.Infinity, Mathf.Infinity));
		
		var posY : AnimationCurve = outCC.getCurve(path, 'localPosition.y', Transform);
		posY.AddKey(Keyframe(time, trans.localPosition.y, Mathf.Infinity, Mathf.Infinity));

		var posZ : AnimationCurve = outCC.getCurve(path, 'localPosition.z', Transform);
		posZ.AddKey(Keyframe(time, trans.localPosition.z, Mathf.Infinity, Mathf.Infinity));

		// scales
		var scaleX : AnimationCurve = outCC.getCurve(path, 'localScale.x', Transform);
		scaleX.AddKey(Keyframe(time, trans.localScale.x, Mathf.Infinity, Mathf.Infinity));
		
		var scaleY : AnimationCurve = outCC.getCurve(path, 'localScale.y', Transform);
		scaleY.AddKey(Keyframe(time, trans.localScale.y, Mathf.Infinity, Mathf.Infinity));

		var scaleZ : AnimationCurve = outCC.getCurve(path, 'localScale.z', Transform);
		scaleZ.AddKey(Keyframe(time, trans.localScale.z, Mathf.Infinity, Mathf.Infinity));
		
		// rotation
		var rotationX : AnimationCurve = outCC.getCurve(path, 'localRotation.x', Transform);
		rotationX.AddKey(Keyframe(time, trans.localRotation.x, Mathf.Infinity, Mathf.Infinity));

		var rotationY : AnimationCurve = outCC.getCurve(path, 'localRotation.y', Transform);
		rotationY.AddKey(Keyframe(time, trans.localRotation.y, Mathf.Infinity, Mathf.Infinity));

		var rotationZ : AnimationCurve = outCC.getCurve(path, 'localRotation.z', Transform);
		rotationZ.AddKey(Keyframe(time, trans.localRotation.z, Mathf.Infinity, Mathf.Infinity));

		var rotationW : AnimationCurve = outCC.getCurve(path, 'localRotation.w', Transform);
		rotationW.AddKey(Keyframe(time, trans.localRotation.w, Mathf.Infinity, Mathf.Infinity));
	}

	private function addToClip_SpriteRenderer(outCC : S2U_CurveCreator, time : float, path : String, sr : SpriteRenderer)
	{
	}

	private function splitObjectIntoDict(dict : Dictionary.<String, GameObject>, obj : GameObject)
	{
		var objPath : String = getGOPathCut(obj);
		
		if (objPath.Length > 0)
			dict.Add(objPath, obj);
			
		for (var child : Object in obj.transform)
		{
			var childT : Transform = child as Transform;
			
			splitObjectIntoDict(dict, childT.gameObject);
		}
	}
	
	private function getGOPathCut(go : GameObject) : String
	{
		var basicPath : String = S2U_Prefab.getGOPath(go);
		// cut first element, this is the "root" game object, useless for us
		
		var firstSlash : int = basicPath.IndexOf('/');
		if (firstSlash == -1)
			return "";
			
		return basicPath.Substring(firstSlash + 1);
	}
	
	private function saveClip(anim : AnimationClip, destDir : String)
	{
		var outPath : String = Path.Combine(destDir, anim.name + '.anim');
		AssetDatabase.CreateAsset(anim, outPath);
		fixAnimation(outPath);
	}
	
	private function fixAnimation(outPath : String)
	{
		// this is some sic joke.

		// you CAN'T set Legacy mode for animation and it HAVE TO be legacy
		// for mechanim to work properly for node/sprite based objects.
		// just spent like 3h looking for a proper solution. there seems to be none.
		
		// this seems to change importing type for animations, but works only for models
		// (assetImporter as ModelImporter).animationType = ModelImporterAnimationType.Legacy;
		// AssetDatabase.ImportAsset(outPath, ImportAssetOptions.ForceUpdate);
		
		// taking internal parameter by reflection doesn't work either - non-public member doesn't show
		// typeof(AnimationClip).GetProperties(BindingFlags.NonPublic) have 0 elements
		
		// i'd love to use memory mapped files but they're not part of the unity implementation...
		// it is assumed that the file is in text mode.
		// current solution
		
		var baseString : String = "m_AnimationType: ";
		var testStringToFind : String = baseString + "1";
		
		var binData : byte[] = File.ReadAllBytes(outPath);
		var data : String = Encoding.UTF8.GetString(binData);
		
		if (data.IndexOf(testStringToFind) != -1)
		{
			// input file is in text mode
//			Debug.Log("Found marker - text mode assumed");
			data = data.Replace(testStringToFind, baseString + "2");
			File.WriteAllText(outPath, data);
		}
		else
		{
			// input must be in binary mode.
			Debug.Log("Marker for fixing not found. Assets are serialized in binary mode. Change mode to text and reimport again.");
			
			// fix for binary format goes here
			
//			File.WriteAllBytes(outPath, binData);
		}

	}
};
