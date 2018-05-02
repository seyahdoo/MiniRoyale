using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.events;

public class PINFOListener : GameEventUser {

	public NetworkItemOrchestrator itemOrchestrator;
	public NetworkRivalOrchestrator rivalOrchestrator;

	public ItemDictionary itemDictionary;

	//PINFO
	public override void OnEventInvoked (object eventData)
	{

		string[] args = (string[])eventData;
	
		rivalOrchestrator.PINFO (int.Parse (args [0]), args [1], bool.Parse (args [3]));


		List<UniqueItem> items = ParseItemList (args [2]);

		itemOrchestrator.PINFO (
			int.Parse (args [0]),
			args [1],
			items
		);

	}

	public List<UniqueItem> ParseItemList(string s){

		//Debug.Log ("Unique Item Parsing: " + s);

		List<UniqueItem> uitems = new List<UniqueItem>();

		s = s.Trim ('[', ']');
		//Debug.Log (s);
		string[] itemlist = s.Split ('.');
		foreach (var iteminfo in itemlist) {
			//Debug.Log (iteminfo);

			string[] itemstring =	iteminfo.Split ('+');
			//Debug.Log (itemstring[0]+","+itemstring[1]);

			//Debug.Log (int.Parse (itemstring [0]));
			//Debug.Log (int.Parse (itemstring [1]));
			//Debug.Log(itemDictionary.GetItem (int.Parse (itemstring [1])).itemName);
				
			UniqueItem uitem = new UniqueItem (
				                   int.Parse (itemstring [0]),
				                   itemDictionary.GetItem (int.Parse (itemstring [1]))
			                   ); 
			//Debug.Log ("Parsed:" + uitem.item.itemName);
			uitems.Add (uitem);
		}

		//Debug.Log ("items:"+uitems);

		return uitems;
	}

}
