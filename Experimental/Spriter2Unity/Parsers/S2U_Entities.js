#pragma strict


import System.Xml;
import System.Collections.Generic;


class S2U_Entities extends Object
{
	private var entities : List.<S2U_Entity>;

	function S2U_Entities(xml : XmlNode)
	{
		entities = new List.<S2U_Entity>();

		for (var nodeXML : Object in xml.ChildNodes)
		{
			var node : XmlNode = nodeXML as XmlNode;
			
			if (node.Name != S2U_Entity.nodeName)
				continue;
				
			var entity : S2U_Entity = S2U_Entity();
			if (! entity.parse(node))
				continue;
			
			entities.Add(entity);
		}
	}

	function build(folders : S2U_Folders, outputDir : String)
	{
		var prefabBuilder : S2U_Prefab = S2U_Prefab(folders);
	
		for (var entity : S2U_Entity in entities)
		{
			prefabBuilder.prepare(entity, outputDir);
		}
	}
};


class S2U_Base extends Object
{
	private var id : int;
	
	function S2U_Base()
	{
		id = -1; // invalid
	}
	
	function parse(xml : XmlNode) : boolean
	{
		id = int.Parse(xml.Attributes['id'].Value);
		return true;
	}
	
	function getId() : int { return id; }
	protected function setId(newId : int) { id = newId; }
};


class S2U_Entity extends S2U_Base
{
	static var nodeName : String = "entity";

	private var name : String;
	private var animations : Dictionary.<int, S2U_Animation>;

	function S2U_Entity()
	{
		super();
		animations = new Dictionary.<int, S2U_Animation>();
	}
	
	function getAnimations() : Dictionary.<int, S2U_Animation> { return animations; }
	
	function parse(xml : XmlNode) : boolean
	{
		if (! super.parse(xml))
			return false;
	
		name = xml.Attributes['name'].Value;
		
		for (var nodeXML : Object in xml.ChildNodes)
		{
			var node : XmlNode = nodeXML as XmlNode;
			
			if (node.Name != S2U_Animation.nodeName)
				continue;

			var anim : S2U_Animation = S2U_Animation();
			if (! anim.parse(node))
				continue;
				
			animations.Add(anim.getId(), anim);
		}
		
		return true;
	}
	
	function getName() : String { return name; }
};
