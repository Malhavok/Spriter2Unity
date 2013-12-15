#pragma strict


class S2U_Prefab extends Object
{
	private var folders : S2U_Folders;
	private var objectMap : Dictionary.<String, GameObject>;
	private var root : GameObject;

	private var spriteImportScale : float;

	function S2U_Prefab(folders_ : S2U_Folders)
	{
		// TODO: find a way to read this
		spriteImportScale = 0.01f;
	
		folders = folders_;
		objectMap = new Dictionary.<String, GameObject>();
	}
	
	function prepare(entity : S2U_Entity, destDirectory : String)
	{
		root = new GameObject(entity.getName());
		objectMap[""] = root;

		var allAnims : Dictionary.<int, S2U_Animation> = entity.getAnimations();
		var keyList : List.<int> = getSortedAnimIdList(allAnims);
		
		var didFirst : boolean = false;
		for (var animId : int in keyList)
		{
			var anim : S2U_Animation = allAnims[animId];
			
//			Debug.Log("Using animation " + anim.getName() + " (id: " + animId + ")");

			attachAnimationGO(anim, ! didFirst);
			
			didFirst = true;			
		}

		objectMap.Clear();
		
		saveRoot(destDirectory);
		GameObject.DestroyImmediate(root);
	}
	
	private function getSortedAnimIdList(allAnims : Dictionary.<int, S2U_Animation>) : List.<int>
	{
		// since we can't use neither Keys.ToList() no Keys.CopyTo() in any normal way...
		var outList : List.<int> = new List.<int>();
		
		for (var tmp : int in allAnims.Keys)
			outList.Add(tmp);
			
		outList.Sort();
		return outList;
	}
	
	private function attachAnimationGO(anim : S2U_Animation, goActive : boolean)
	{
		var mainline : S2U_Mainline = anim.getMainline();
		var refKeys : List.<S2U_Key> = mainline.getSortedKeys();
		
		for (var tmpKey : S2U_Key in refKeys)
		{
			var refList : List.<S2U_BoneRef> = tmpKey.getRefList();
			
//			Debug.Log("Using key frame " + tmpKey.getId());
			generateGOFromFrame(refList, anim, goActive);
		
			goActive = false;
		}
	}

	private function generateGOFromFrame(refList : List.<S2U_BoneRef>, anim : S2U_Animation, goActive : boolean)
	{
		var realScale : Vector2 = Vector2(1.0f, 1.0f);
		// these are the guys that'll be parented to root
		var firstList : List.<S2U_BoneRef> = getRefsParentedTo(refList, -1);
		
		for (var tmpObj : S2U_BoneRef in firstList)
		{
			var sprite : S2U_ObjectRef = tmpObj as S2U_ObjectRef;
			if (sprite != null)
				generateGOFromObject(sprite, "", anim, realScale, goActive);
			else
				generateGOFromBone(tmpObj, "", refList, anim, realScale, goActive);
		}
	}
	
	private function generateGOFromObject(sprite : S2U_ObjectRef, parentPath : String, anim : S2U_Animation, parentScale : Vector2, goActive : boolean) : void
	{
		// parent scale is here just to scale, nothing more will be done with it
		// also - sprites have no children, so we don't need ref list!
		// calculations of pivots have to be done here
		// this function is terrible and long
		var timeline : S2U_Timeline = anim.getTimelineById(sprite.getTimeline());
		var key : S2U_Key = timeline.getKeyById(sprite.getTimelineKey());
		var object : S2U_Object = key.getNormal() as S2U_Object;
		
		var file : S2U_File = folders.getFile(object.getFolder(), object.getFile());
		var filePath : String = folders.getPath(object.getFolder(), object.getFile());
		
		var parentGO : GameObject = objectMap[parentPath];
		var goFullPath : String = getGOPath(timeline.getName(), parentGO);

		if (objectMap.ContainsKey(goFullPath))
			return;

		var outGO : GameObject = new GameObject();
		outGO.SetActive(goActive);
		outGO.name = timeline.getName();
		outGO.transform.parent = parentGO.transform;
		// add it to GameObject map
		objectMap[goFullPath] = outGO;
		
		// preparations done, time for calculations!
		// this is more-or-less direct translation from PrefabMaker.mangle
		var sinA : float = Mathf.Sin(object.getAngleRad());
		var cosA : float = Mathf.Cos(object.getAngleRad());
		
		// first, calculate pivot position
		var pivot : Vector2 = object.getPivot();
		if (float.IsInfinity(pivot.x))
			pivot.x = file.getPivot().x;
		if (float.IsInfinity(pivot.y))
			pivot.y = file.getPivot().y;

		var pivotPix : Vector2 = Vector2(file.getSize().x * pivot.x, file.getSize().y * pivot.y);
		pivotPix = file.getSize() / 2.0f - pivotPix; // finally, we got pivot position... or do we? rotation have to be applied!
		var fullPivot : Vector2 = Vector2(); // no "rotate" method for Vector2
		fullPivot.x = pivotPix.x * cosA - pivotPix.y * sinA;
		fullPivot.y = pivotPix.x * sinA + pivotPix.y * cosA;
		
		// now - scales
		var scale : Vector2 = object.getScale(); // but it'd be way too simple, wouldn't it?
		scale.x *= parentScale.x;
		scale.y *= parentScale.y;
		
		// yupi, final part! remember there is no "import scale" here...
		outGO.transform.localPosition.x = spriteImportScale * (object.getPos().x * parentScale.x + fullPivot.x * scale.x);
		outGO.transform.localPosition.y = spriteImportScale * (object.getPos().y * parentScale.y + fullPivot.y * scale.y);
		outGO.transform.localPosition.z = -10.0f * spriteImportScale * sprite.getZIndex();
		
		outGO.transform.localScale = scale;
		outGO.transform.localScale.z = 1.0f;
		
		outGO.transform.localRotation = Quaternion.AngleAxis(object.getAngleDeg(), Vector3(0.0f, 0.0f, 1.0f));
		
		// add sprite renderer
		var spriteRenderer : SpriteRenderer = outGO.AddComponent(SpriteRenderer) as SpriteRenderer;
		spriteRenderer.color.a = object.getAlpha();
		var spriteImg : Sprite = AssetDatabase.LoadAssetAtPath(filePath, Sprite) as Sprite;
		
		if (spriteImg == null)
			Debug.LogWarning("Failed to connect node " + outGO.name + " with sprite " + filePath);
		else
			spriteRenderer.sprite = spriteImg;
	}
	
	private function generateGOFromBone(bone : S2U_BoneRef, parentPath : String, refList : List.<S2U_BoneRef>, anim : S2U_Animation, parentScale : Vector2, goActive : boolean) : void
	{
		// copy parent scale, we will change it
		// we have to get children of this node from refList
		// all transforms here are set to 1 and propagated via parentScale
		var timeline : S2U_Timeline = anim.getTimelineById(bone.getTimeline());
		var key : S2U_Key = timeline.getKeyById(bone.getTimelineKey());
		var object : S2U_Bone = key.getNormal();
		
		var parentGO : GameObject = objectMap[parentPath];
		var goFullPath : String = getGOPath(timeline.getName(), parentGO);

		if (objectMap.ContainsKey(goFullPath))
			return;

		var outGO : GameObject = new GameObject();
		outGO.SetActive(goActive);
		outGO.name = timeline.getName();
		outGO.transform.parent = parentGO.transform;
		// add it to GameObject map
		objectMap[goFullPath] = outGO;
		
		// preparations done, time for calculations!
		// this is more-or-less direct translation from PrefabMaker.mangle
		
		// this will be the new parent scale
		var scale : Vector2 = object.getScale(); // but it'd be way too simple, wouldn't it?
		scale.x *= parentScale.x;
		scale.y *= parentScale.y;
		
		// yupi, final part! remember there is no "import scale" here...
		outGO.transform.localPosition.x = spriteImportScale * object.getPos().x * parentScale.x;
		outGO.transform.localPosition.y = spriteImportScale * object.getPos().y * parentScale.y;
		outGO.transform.localPosition.z = 0.0f;

		outGO.transform.localScale = Vector3.one;

		outGO.transform.localRotation = Quaternion.AngleAxis(object.getAngleDeg(), Vector3.forward);
		
		// now - find all children!
		var children : List.<S2U_BoneRef> = getRefsParentedTo(refList, bone.getId());
		for (var tmpObj : S2U_BoneRef in children)
		{
			var sprite : S2U_ObjectRef = tmpObj as S2U_ObjectRef;
			if (sprite != null)
				generateGOFromObject(sprite, goFullPath, anim, scale, goActive);
			else
				generateGOFromBone(tmpObj, goFullPath, refList, anim, scale, goActive);
		}
	}
	
	private function getGOPath(goName : String, parent : GameObject) : String
	{
		if (parent == null)
			return goName;
	
		var parentPath : String = getGOPath(parent);
		return parentPath + '/' + goName;
	}
	
	private function getGOPath(go : GameObject) : String
	{
		if (go.transform.parent == null)
			return go.name;
			
		var pathUpToNow : String = getGOPath(go.transform.parent.gameObject);
		return pathUpToNow + '/' + go.name;
	}
	
	private function getRefsParentedTo(refList : List.<S2U_BoneRef>, parentId : int) : List.<S2U_BoneRef>
	{
		var outList : List.<S2U_BoneRef> = new List.<S2U_BoneRef>();
		
		for (var tmp : S2U_BoneRef in refList)
		{
			if (tmp.getParent() != parentId)
				continue;
			outList.Add(tmp);
		}
		
		return outList;
	}
	
	private function saveRoot(outDir : String)
	{
		var prefabPath : String = combinePrefabPath(outDir, root.name);
		
		var prefab : UnityEngine.Object = PrefabUtility.CreateEmptyPrefab(prefabPath);
		PrefabUtility.ReplacePrefab(root, prefab, ReplacePrefabOptions.ConnectToPrefab);
	}
	
	private function combinePrefabPath(path : String, name : String) : String
	{
		return Path.Combine(path, name + '.prefab');
	}
};
