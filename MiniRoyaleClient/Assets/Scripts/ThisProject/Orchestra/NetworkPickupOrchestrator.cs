using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NetworkPickupOrchestrator : MonoBehaviour {

	public UDPConnection connection;

	class pickupInfo {
		
	}

	public Dictionary<int, Pickup> pickups = new Dictionary<int, Pickup> ();

	public GameObject pickupObject;


	public List<Pickup> nearPickups = new List<Pickup> ();
	public Pickup chosenPickup;
	public Transform playerPosition;



	public void PCKIN(int pickupID, int itemID, float posx, float posy, int quantity ){
			
		Pickup p;

		if (!pickups.ContainsKey (pickupID)) {
			//create pickup
			GameObject go = Instantiate (pickupObject);
			p = go.GetComponent<Pickup> ();
			p.orchestrator = this;
			pickups.Add (pickupID, p);

		} else {
			p = pickups [pickupID];
		
		}


		p.SetOptions (pickupID, itemID, posx, posy, quantity);
	
	}

	public void PCKDL(int pickupID){

		if (pickups.ContainsKey (pickupID)) {
			//Debug.Log ("Will delete");
			Pickup p;
			p = pickups [pickupID];
			if (chosenPickup == p) {
				p.UnChosen();
				chosenPickup = null;

			}

			Destroy (p.gameObject);
				
		}
	
	}


	//TODO fix this

	public void InsideRange(Pickup p){
		if (nearPickups.Count <= 0) {
			chosenPickup = p;
			p.Chosen ();
		}
		nearPickups.Add (p);
	}

	public void OutsideRange(Pickup p){
		nearPickups.Remove (p);
		//BUG HERE Probaby
		if (chosenPickup == p) {
			chosenPickup.UnChosen ();
			chosenPickup = null;
		}
	}

	void Update(){

		if (nearPickups.Count >= 2) {
			float neardist = float.PositiveInfinity;

			foreach (Pickup p in nearPickups) {
				float dist = Vector3.Distance (playerPosition.position, p.transform.position);
				if(dist < neardist){
					neardist = dist;
					chosenPickup.UnChosen ();
					p.Chosen ();
					chosenPickup = p;
				}

			}
		
		}

		if (Input.GetKeyDown (KeyCode.F)) {
			Debug.Log("picked up "+ chosenPickup.ToString());
			connection.Send ("PCKUP:" + chosenPickup.PickupID + "," + chosenPickup.Quantity + ";");
		}

	}

}
