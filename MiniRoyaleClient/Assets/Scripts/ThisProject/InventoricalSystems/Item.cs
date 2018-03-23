using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Item : ScriptableObject {


	public int typeId;

	public string itemName;

	public string description;

	//Weapons
	//Throwables
	//Skins

	public virtual void Use(){

		///Send SHOOT if weapon

	}

	public virtual void Equip(Pawn pawn){

		///Maybe Change Body color?

	}

	public virtual void DeQuip(Pawn pawn){
	
	
	}


}
