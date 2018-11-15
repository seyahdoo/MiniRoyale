using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.events;

public class EXITTListener : GameEventUser {

    public NetworkBulletOrchestrator bulletOrchestrator;
    public NetworkRivalOrchestrator rivalOrchestrator;

    public NetworkPickupOrchestrator pickupOrchestrator;
    public NetworkPropOrchestrator propOrchestrator;

    public GameObject player;

	public override void OnEventInvoked (object eventData)
	{


        player.SetActive(false);
        bulletOrchestrator.Cleanup();
        rivalOrchestrator.Cleanup();
        propOrchestrator.Cleanup();
        pickupOrchestrator.Cleanup();

        //TODO Load Start Scene

	}


}
