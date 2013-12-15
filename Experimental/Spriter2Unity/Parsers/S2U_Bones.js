#pragma strict

import System.Xml;


class S2U_BoneRef extends S2U_Base
{
	static function getNodeName() : String { return "bone_ref"; }

	private var parent : int;
	private var timeline : int;
	private var timelineKey : int;

	function S2U_BoneRef()
	{
		super();
		parent = -1; // -1 means no parent
	}
	
	function parse(xml : XmlNode) : boolean
	{
		if (! super.parse(xml))
			return false;
	
		if (xml.Attributes['parent'] != null)
			parent = int.Parse(xml.Attributes['parent'].Value);

		timeline = int.Parse(xml.Attributes['timeline'].Value);
		timelineKey = int.Parse(xml.Attributes['key'].Value);
		
		return true;
	}
	
	function getParent() : int { return parent; }
	function getTimeline() : int { return timeline; }
	function getTimelineKey() : int { return timelineKey; }
};


class S2U_Bone extends Object
{
	static function getNodeName() : String { return "bone"; }
	
	private var pos : Vector2;
	private var scale : Vector2;
	private var angleDeg : float;

	function S2U_Bone()
	{
		pos = Vector2(0.0f, 0.0f);
		scale = Vector2(1.0f, 1.0f);
		angleDeg = 0.0f;
	}
	
	function getPos() : Vector2 { return pos; }
	function getScale() : Vector2 { return scale; }
	function getAngleDeg() : float { return angleDeg; }
	function getAngleRad() : float { return Mathf.Deg2Rad * getAngleDeg(); }
	
	function parse(xml : XmlNode) : boolean
	{
		if (xml.Attributes['x'] != null)
			pos.x = float.Parse(xml.Attributes['x'].Value);
			
		if (xml.Attributes['y'] != null)
			pos.y = float.Parse(xml.Attributes['y'].Value);
			
		if (xml.Attributes['angle'] != null)
			angleDeg = float.Parse(xml.Attributes['angle'].Value);
			
		if (xml.Attributes['scale_x'] != null)
			scale.x = float.Parse(xml.Attributes['scale_x'].Value);
			
		if (xml.Attributes['scale_y'] != null)
			scale.y = float.Parse(xml.Attributes['scale_y'].Value);
	
		return true;
	}
};
