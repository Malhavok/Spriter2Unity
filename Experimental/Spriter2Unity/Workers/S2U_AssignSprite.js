#pragma strict

class S2U_SpriteInfo
{
	var spriteName : String;
	var nodeName : String;

	var sprite : Sprite;

	// sadly, i cannot hide it as it's value will be lost
	var rend : SpriteRenderer;
	
	function assign() : void
	{
		rend.sprite = sprite;
	}
}

// neither i can hide this, do not modify this manually, please
var spriteList : S2U_SpriteInfo[];


function AssignSprite(idx : int) : void
{
	spriteList[idx].assign();
}
