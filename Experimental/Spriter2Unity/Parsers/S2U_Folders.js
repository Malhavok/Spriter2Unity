#pragma strict

import System.IO;
import System.Xml;
import System.Collections.Generic;


class S2U_Folders extends Object
{
	private var basePath : String;
	private var folders : Dictionary.<int, S2U_Folder>;

	function S2U_Folders(xml : XmlNode)
	{
		folders = new Dictionary.<int, S2U_Folder>();
	
		for (var nodeXML : Object in xml.ChildNodes)
		{
			var node : XmlNode = nodeXML as XmlNode;
			
			if (node.Name != S2U_Folder.nodeName)
				continue;
				
			var folder : S2U_Folder = S2U_Folder();
			if (! folder.parse(node))
				continue;
				
			folders.Add(folder.getId(), folder);
		}
	}
	
	function setBasePath(bp : String) { basePath = bp; }
	
	function debugPrint()
	{
		for (var tmp : S2U_Folder in folders.Values)
		{
			tmp.debugPrint();
		}
	}
	
	function getFile(folderId : int, fileId : int) : S2U_File
	{
		if (! folders.ContainsKey(folderId))
			return null;
			
		return folders[folderId].getFile(fileId);
	}
	
	function getPath(folderId : int, fileId : int) : String
	{
		if (! folders.ContainsKey(folderId))
			return null;
			
		var file : S2U_File = folders[folderId].getFile(fileId);
		if (! file)
			return null;
			
		return Path.Combine(basePath, file.getPath());
	}
};


class S2U_Folder extends S2U_Base
{
	static var nodeName : String = "folder";

	private var files : Dictionary.<int, S2U_File>;
	
	function S2U_Folder()
	{
		super();
		files = new Dictionary.<int, S2U_File>();
	}
	
	function parse(xml : XmlNode) : boolean
	{
		if (! super.parse(xml))
			return false;
	
		for (var nodeXML : Object in xml.ChildNodes)
		{
			var node : XmlNode = nodeXML as XmlNode;
			
			if (node.Name != S2U_File.nodeName)
				continue;
				
			var file : S2U_File = S2U_File();
			if (! file.parse(node))
				continue;
				
			files.Add(file.getId(), file);
		}
		
		return true;
	}
	
	function getFile(fileId : int) : S2U_File
	{
		if (! files.ContainsKey(fileId))
			return null;
		return files[fileId];
	}
	
	function debugPrint()
	{
		Debug.Log("Folder -> id: " + getId());
		
		for (var tmp : S2U_File in files.Values)
		{
			tmp.debugPrint();
		}
	}
};


class S2U_File extends S2U_Base
{
	static var nodeName : String = "file";

	private var path : String;
	private var size : Vector2;
	private var pivot : Vector2;
	
	function S2U_File()
	{
		super();
		size = Vector2();
		pivot = Vector2();
	}

	function getPath() : String { return path; }
	function getSize() : Vector2 { return size; }
	function getPivot() : Vector2 { return pivot; }
	
	function parse(xml : XmlNode) : boolean
	{
		if (! super.parse(xml))
			return false;
	
		path = xml.Attributes['name'].Value;
		
		size.x = float.Parse(xml.Attributes['width'].Value);
		size.y = float.Parse(xml.Attributes['height'].Value);

		pivot.x = float.Parse(xml.Attributes['pivot_x'].Value);
		pivot.y = float.Parse(xml.Attributes['pivot_y'].Value);
		
		return true;
	}
	
	function debugPrint()
	{
		Debug.Log("File -> id: " + getId() + ", path: " + path + ", size (" + size.x + ", " + size.y + "), pivot (" + pivot.x + ", " + pivot.y + ")");
	}
};
