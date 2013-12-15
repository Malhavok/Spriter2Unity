#pragma strict

import System.Xml;
import System.IO;

class S2U_Importer extends AssetPostprocessor
{
	private static var outputPath : String = "Assets/S2UOutput";

	static function OnPostprocessAllAssets(
			importedAssets : String[],
			deletedAssets : String[],
			movedAssets : String[],
			movedFromAssetPaths : String[])
	{
		// TODO: make sure that all other NEEDED paths are handled as well
		// eg, when moving SCML we may want to reimport it just to change all sprites attached
		for (var str : String in importedAssets)
		{
			if (! str.EndsWith('.scml'))
				continue;
				
			ImportSCML(str);
		}
	}
	
	
	static function ImportSCML(path : String)
	{
		var basePath : String = Path.GetDirectoryName(path);
		var pureFilename : String = Path.GetFileNameWithoutExtension(path);
		var outputDir : String = Path.Combine(S2U_Importer.outputPath, pureFilename);
		
		createDirectories(outputDir);
		
		var inFile : FileStream = FileStream(path, FileMode.Open, FileAccess.Read);
		if (! inFile)
		{
			Debug.LogError("Unable to open FileStream for path " + path);
			return;
		}
		
		var xmlReader : XmlReader = XmlTextReader.Create(inFile);
		if (! xmlReader)
		{
			Debug.LogError("Unable to create XmlReader for path " + path);
			return;
		}
		
		var rootNode : XmlNode = getSpriterRoot(xmlReader);
		if (! rootNode)
			return;
				
		var folders : S2U_Folders = S2U_Folders(rootNode);
		folders.setBasePath(basePath);
		
		var entities : S2U_Entities = S2U_Entities(rootNode);
		entities.build(folders, outputDir);
	}
	

	static private function getSpriterRoot(reader : XmlReader)
	{
		var doc : XmlDocument = new XmlDocument();
		
		while (true)
		{
			var rootNode : XmlNode = doc.ReadNode(reader);
			if (! rootNode)
				break;
			
//			Debug.Log(rootNode.Name);
			if (rootNode.Name == "spriter_data")
				return rootNode;
		}
		
		Debug.LogError("Invalid SCML file - there is no spriter_data");
		return null;
	}
	
	static private function createDirectories(finalDir : String)
	{
		var folderNames : String[] = finalDir.Split(Path.DirectorySeparatorChar);
		if (folderNames.Length == 0)
		{
			Debug.LogError("Unable to create directories for non-directory like string: " + finalDir);
			return;
		}
		
		var pathSoFar : String = folderNames[0];
		for (var idx : int = 1; idx < folderNames.Length; ++idx)
		{
			var newFullPath : String = Path.Combine(pathSoFar, folderNames[idx]);
			if (! Directory.Exists(newFullPath))
				AssetDatabase.CreateFolder(pathSoFar, folderNames[idx]);
			pathSoFar = newFullPath;
		}
	}
};
