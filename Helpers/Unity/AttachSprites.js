#pragma strict

// Sprite attaching script for Spriter2Unity
// For this thing to work you have to keep all your textures in the same folder structure as when working with Spriter
// 

function Start() : void
{
	attach_sprites();
}

private function attach_sprites() : void
{
	// assuming that the top-level game object doesn't have a sprite
	attach_sprites_to_children(transform);
	
	Debug.Log("Sprite attaching finished. During play move object to project to create a new prefab, with sprites attached.");
}

private function attach_sprites_to_children(trans : Transform) : void
{
	for (var childO : Object in trans)
	{
		var childT : Transform = childO as Transform;
		// could add some safety here...
		
		try_attaching_sprites(childT.gameObject);
		
		// reccurence
		attach_sprites_to_children(childT);
	}
}

private function try_attaching_sprites(go : GameObject) : void
{
	var sr : SpriteRenderer = go.GetComponent(SpriteRenderer) as SpriteRenderer;
	if (! sr)
	{
//		Debug.Log("(" + count + ") node is not a sprite: " + go.name);
		return;
	}
	
//	Debug.Log("(" + count + ") SPRITE: " + go.name);
	// in a name, between brackets, hidden is the name of the file that should be attached
	// in that name, '/' character was replaced by '!' character, because Unity uses '/' internally
	// we have to get this filename and unparse it.
	
	var idx : int = go.name.IndexOf('(');
	var edx : int = go.name.LastIndexOf(')');
	
	if (idx == -1 || edx == -1)
	{
		Debug.LogError("Game object name doesn't contain filename. It seems it was modified externally.");
		return;
	}
	
	var fName : String = go.name.Substring(idx + 1, edx - idx - 1).Replace('!', '/');

	// remove extension at the end
	var dotIdx : int = fName.IndexOf('.');
	if (dotIdx != -1)
	{
		fName = fName.Substring(0, dotIdx);
	}
	
//	Debug.Log("go name: " + go.name + " -> filename: '" + fName + "'");
	var sprite : Sprite = Resources.Load(fName, Sprite) as Sprite;
	if (! sprite)
	{
		Debug.LogError("Cannot find a sprite for object " + go.name + " (requested filename " + fName + " under Resources folder)");
		return;
	}
	
	sr.sprite = sprite;
}
