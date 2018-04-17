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

		//Dont draw weapon if player is dead
		if(pawn.rival.isDead){
			pawn.weaponRenderer.enabled = false;

		}

	}

	public virtual void DeQuip(Pawn pawn){
	
	
	}


}
