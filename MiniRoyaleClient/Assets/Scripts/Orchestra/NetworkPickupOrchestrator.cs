using seyahdoo.pooling.v3;
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

    private void Awake()
    {
        Pool.CreatePool<Pickup>(pickupObject, 10, 10000);

    }

    public void PCKIN(int pickupID, int itemID, float posx, float posy, int quantity ){
			
		Pickup p;

		if (!pickups.ContainsKey (pickupID)) {

            p = Pool.Get<Pickup>();
			p.orchestrator = this;
			pickups.Add (pickupID, p);

		} else {
			p = pickups [pickupID];
		
		}


		p.SetOptions (pickupID, itemID, posx, posy, quantity);
	
	}

	public void PCKDL(int pickupID){

		if (pickups.ContainsKey (pickupID)) {

			Pickup p;
			p = pickups [pickupID];
			if (chosenPickup == p) {
				p.UnChosen();
				chosenPickup = null;

			}

            pickups.Remove(pickupID);

            Pool.Release<Pickup>(p);
				
		}
	
	}


	//TODO fix this

	public void InsideRange(Pickup p){
		nearPickups.Add (p);
	}

	public void OutsideRange(Pickup p){
		nearPickups.Remove (p);

        if(chosenPickup == p)
        {
            p.UnChosen();
            chosenPickup = null;
        }

	}

	void Update(){

		float neardist = float.PositiveInfinity;

		foreach (Pickup p in nearPickups) {
			float dist = Vector3.Distance (playerPosition.position, p.transform.position);
			if(dist < neardist){
				neardist = dist;
                if (chosenPickup)
                {
				    chosenPickup.UnChosen ();
                }
				p.Chosen ();
				chosenPickup = p;
			}

		}
		

		if (Input.GetKeyDown (KeyCode.F)) {
            if (chosenPickup)
            {
			    Debug.Log("picked up "+ chosenPickup.ToString());
			    connection.Send ("PCKUP:" + chosenPickup.PickupID + ";");
            }
		}

	}

    public void Cleanup()
    {
        Pool.ReleaseAll<Pickup>();

        pickups.Clear();
        nearPickups.Clear();
        chosenPickup = null;


    }

}
