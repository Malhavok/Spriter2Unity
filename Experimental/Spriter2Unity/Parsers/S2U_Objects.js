#pragma strict

import System.Xml;


class S2U_ObjectRef extends S2U_BoneRef
{
	static function getNodeName() : String { return "object_ref"; }

	private var zIndex : int;

	function S2U_ObjectRef()
	{
		super();
		zIndex = -1;
	}
	
	function getZIndex() : int { return zIndex; }
	
	function parse(xml : XmlNode) : boolean
	{
		if (! super.parse(xml))
			return false;
	
		zIndex = int.Parse(xml.Attributes['z_index'].Value);
	
		return true;
	}
};


class S2U_Object extends S2U_Bone
{
	static function getNodeName() : String { return "object"; }

	private var folderId : int;
	private var fileId : int;
	private var pivot : Vector2;
	private var alpha : float;

	function S2U_Object()
	{
		super();
		alpha = 1.0f;
		
		pivot = Vector2();
		pivot.x = Mathf.Infinity; // means "not set"
		pivot.y = Mathf.Infinity; // means "not set"
	}
	
	function getFolder() : int { return folderId; }
	function getFile() : int { return fileId; }
	function getPivot() : Vector2 { return pivot; }
	function getAlpha() : float { return alpha; }
	
	function parse(xml : XmlNode) : boolean
	{
		if (! super.parse(xml))
			return false;
			
		folderId = int.Parse(xml.Attributes['folder'].Value);
		fileId = int.Parse(xml.Attributes['file'].Value);
		
		if (xml.Attributes['a'] != null)
			alpha = float.Parse(xml.Attributes['a'].Value);
			
		if (xml.Attributes['pivot_x'] != null)
			pivot.x = float.Parse(xml.Attributes['pivot_x'].Value);
	
		if (xml.Attributes['pivot_y'] != null)
			pivot.y = float.Parse(xml.Attributes['pivot_y'].Value);

		return true;
	}
};
