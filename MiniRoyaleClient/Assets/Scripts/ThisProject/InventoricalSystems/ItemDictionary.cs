using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ItemDictionary : MonoBehaviour {

	public Item[] registeredItems;

	Dictionary<int, Item> itemDictionary = new Dictionary<int, Item>();


	void Awake(){

		foreach (var item in registeredItems) {
			itemDictionary.Add (item.typeId, item);
		}

	}


	public Item GetItem(int id){
	
		if (!itemDictionary.ContainsKey (id)) {
			Debug.LogError ("ERROR: cannot find specified item in dictionary.");
			return null;
		}

		return itemDictionary [id];
	}


}
