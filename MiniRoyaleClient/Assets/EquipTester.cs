using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EquipTester : MonoBehaviour {


	public bool equipItem;
	public bool deQuipItem;

	public Pawn pawn;
	public Item item;

	void Update(){
		if (equipItem) {
			equipItem = false;
			EquipItem ();
		}

		if (deQuipItem) {
			deQuipItem = false;
			DeQuipItem ();
		}



	}

	public void EquipItem(){
		pawn.EquipThreadSafe (new UniqueItem(Random.Range(0,10000),item));
	}

	public void DeQuipItem(){
	
		//pawn.Equip (new UniqueItem(Random.Range(0,10000),item));

	}


}
