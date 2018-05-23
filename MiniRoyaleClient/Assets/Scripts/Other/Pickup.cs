using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Pickup : MonoBehaviour {

	public NetworkPickupOrchestrator orchestrator;
	public GameObject chosenObj;

	public int PickupID;
	public int TypeID;
	public int Quantity;

	void OnTriggerEnter2D(Collider2D other)
	{
		orchestrator.InsideRange (this);


	}

	void OnTriggerExit2D(Collider2D other)
	{
		orchestrator.OutsideRange (this);


	}

	public void Chosen(){
		
		chosenObj.SetActive (true);
	}

	public void UnChosen(){
	
		chosenObj.SetActive (false);
	
	}

	public void SetOptions(int pickupID, int typeID, float posx, float posy, int quantity){

		this.PickupID = pickupID;
		this.TypeID = typeID;
		this.Quantity = quantity;

		transform.position = new Vector2 (posx, posy);
	
	}

}
