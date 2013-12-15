#pragma strict

import System.Xml;
import System.Collections.Generic;

class S2U_Animation extends S2U_Base
{
	static var nodeName : String = "animation";
	
	private var name : String;
	private var length : float;
	
	private var mainline : S2U_Mainline;
	private var timelines : Dictionary.<int, S2U_Timeline>;

	function S2U_Animation()
	{
		super();
		mainline = S2U_Mainline();
		timelines = new Dictionary.<int, S2U_Timeline>();
	}
	
	function getName() : String { return name; }
	function getLength() : float { return length; }
	function getMainline() : S2U_Mainline { return mainline; }
	function getTimelineById(id : int) : S2U_Timeline
	{
		if (! timelines.ContainsKey(id))
			return null;
		return timelines[id];
	}
	
	function parse(xml : XmlNode) : boolean
	{
		if (! super.parse(xml))
			return false;
	
		name = xml.Attributes['name'].Value;
		// time in seconds, SCML keeps it in milliseconds
		length = float.Parse(xml.Attributes['length'].Value) / 1000.0f;

		for (var nodeXML : Object in xml.ChildNodes)
		{
			var node : XmlNode = nodeXML as XmlNode;
			
			if (node.Name == S2U_Mainline.nodeName && ! mainline.parse(node))
			{
				Debug.LogError("Unable to continue");
			}
			else if (node.Name == S2U_Timeline.nodeName)
			{
				var timeline : S2U_Timeline = S2U_Timeline();
				
				if (! timeline.parse(node))
					continue;
					
				timelines.Add(timeline.getId(), timeline);
			}
		}

		return true;
	}
};


class S2U_Key extends S2U_Base
{
	static var nodeName : String = "key";

	private var time : float;
	private var onlyRefs : boolean;
	
	private var refList : List.<S2U_BoneRef>;
	private var normList : List.<S2U_Bone>;
	
	function S2U_Key(acceptOnlyRefs : boolean)
	{
		super();
		time = 0.0f;
		onlyRefs = acceptOnlyRefs;
		
		if (onlyRefs)
			refList = new List.<S2U_BoneRef>();
		else
			normList = new List.<S2U_Bone>();
	}
	
	function getTime() : float { return time; }
	function getRefList() : List.<S2U_BoneRef> { return refList; }
	function getNormalList() : List.<S2U_Bone> { return normList; }
	function getNormal() : S2U_Bone
	{
		if (normList.Count > 1)
			Debug.LogError("Normal list got size bigger than 1");
		return normList[0];
	}
	
	function parse(xml : XmlNode) : boolean
	{
		if (! super.parse(xml))
			return false;

		if (xml.Attributes['time'] != null)
			time = float.Parse(xml.Attributes['time'].Value) / 1000.0f;
			
		for (var nodeXML : Object in xml.ChildNodes)
		{
			var node : XmlNode = nodeXML as XmlNode;
			
			if (onlyRefs)
				parseRefs(node);
			else
				parseNormal(node);
		}
			
		return true;
	}
	
	function parseRefs(xml : XmlNode)
	{
		var tmp : S2U_BoneRef;
		if (xml.Name == S2U_BoneRef.getNodeName())
			tmp = S2U_BoneRef();
		else if (xml.Name == S2U_ObjectRef.getNodeName())
			tmp = S2U_ObjectRef();
		else
		{
			Debug.LogWarning("Non-ref object in animation key: " + xml.Name);
			return;
		}
		
		if (! tmp.parse(xml))
			return;
			
		refList.Add(tmp);
	}
	
	function parseNormal(xml : XmlNode)
	{
		var tmp : S2U_Bone;
		if (xml.Name == S2U_Bone.getNodeName())
			tmp = S2U_Bone();
		else if (xml.Name == S2U_Object.getNodeName())
			tmp = S2U_Object();
		else
		{
			Debug.LogWarning("Non-normal object in animation key: " + xml.Name);
			return;
		}
		
		if (! tmp.parse(xml))
			return;
			
		normList.Add(tmp);
	}
};


class S2U_Mainline extends Object
{
	static var nodeName : String = "mainline";

	private var keys : Dictionary.<int, S2U_Key>;

	function S2U_Mainline()
	{
		keys = new Dictionary.<int, S2U_Key>();
	}
	
	function getSortedKeys() : List.<S2U_Key>
	{
		var outList : List.<S2U_Key> = new List.<S2U_Key>();

		var keyList : List.<int> = new List.<int>();
		for (var tmpKey : int in keys.Keys)
			keyList.Add(tmpKey);
		keyList.Sort();
		
		for (var sKey : int in keyList)
			outList.Add(keys[sKey]);		

		return outList;
	}

	function parse(xml : XmlNode) : boolean
	{
		for (var nodeXML : Object in xml.ChildNodes)
		{
			var node : XmlNode = nodeXML as XmlNode;
			if (node.Name != S2U_Key.nodeName)
				continue;
				
			var key : S2U_Key = S2U_Key(true);
			if (! key.parse(node))
				continue;
				
			keys.Add(key.getId(), key);
		}
	
		return true;
	}
};


class S2U_Timeline extends S2U_Base
{
	static var nodeName : String = "timeline";

	private var name : String;
	private var keys : Dictionary.<int, S2U_Key>;
	
	function S2U_Timeline()
	{
		super();
		keys = new Dictionary.<int, S2U_Key>();
	}

	function getName() : String { return name; }
	function getKeyById(id : int) : S2U_Key
	{
		if (! keys.ContainsKey(id))
			return null;
		return keys[id];
	}

	function parse(xml : XmlNode) : boolean
	{
		if (! super.parse(xml))
			return false;

		name = xml.Attributes['name'].Value;
	
		for (var nodeXML : Object in xml.ChildNodes)
		{
			var node : XmlNode = nodeXML as XmlNode;
			if (node.Name != S2U_Key.nodeName)
				continue;
				
			var key : S2U_Key = S2U_Key(false);
			if (! key.parse(node))
				continue;
				
			keys.Add(key.getId(), key);
		}

		return true;
	}
};
