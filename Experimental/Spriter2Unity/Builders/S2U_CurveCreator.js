#pragma strict

import System.Collections.Generic;
import System;

// this class is FUGLY
// TODO: make it nicer to look at
class S2U_CurveCreator extends Object
{
	private var paths : Dictionary.<String, Properties>;

	function S2U_CurveCreator()
	{
		paths = new Dictionary.<String, Properties>();
	}
	
	function getCurve(path : String, property : String, type : Type) : AnimationCurve
	{
		if (! paths.ContainsKey(path))
			paths.Add(path, Properties());
			
		return paths[path].getCurve(property, type);
	}

	function getAnimation(animName : String) : AnimationClip
	{
		var outAnim : AnimationClip = AnimationClip();
		outAnim.name = animName;
		
		// ugly as hell
		for (var key1 : String in paths.Keys)
		{
			var props : Dictionary.<String, Properties.Holder> = paths[key1].getProperties();
			
			for (var key2 : String in props.Keys)
			{
				var holder : Properties.Holder = props[key2];
				outAnim.SetCurve(key1, holder.type, key2, holder.curve);
			}
		}
		
		return outAnim;
	}


	private class Properties
	{
		class Holder
		{
			var curve : AnimationCurve;
			var type : Type;
		}	

		private var props : Dictionary.<String, Holder>;
		
		function Properties()
		{
			props = new Dictionary.<String, Holder>();
		}
		
		function getCurve(property : String, type : Type) : AnimationCurve
		{
			if (! props.ContainsKey(property))
			{
				var holder : Holder = Holder();
				holder.curve = AnimationCurve();
				holder.type = type;
				props.Add(property, holder);
			}
				
			return props[property].curve;
		}
		
		function getProperties() : Dictionary.<String, Holder> { return props; }
	};	
};
