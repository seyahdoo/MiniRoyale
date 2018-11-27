using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.events;

public class EXITTListener : GameEventUser {

    public UDPConnection connection;

    public NetworkBulletOrchestrator bulletOrchestrator;
    public NetworkRivalOrchestrator rivalOrchestrator;

    public NetworkPickupOrchestrator pickupOrchestrator;
    public NetworkPropOrchestrator propOrchestrator;

    public GameObject player;

    public AutoConnector autoConnector;

	public override void OnEventInvoked (object eventData)
	{
        ExitGame();
	}

    public void ExitGame()
    {

        connection.Send("EXITT;");

        player.SetActive(false);

        connection.ResetAdress();

        bulletOrchestrator.Cleanup();
        rivalOrchestrator.Cleanup();
        propOrchestrator.Cleanup();
        pickupOrchestrator.Cleanup();

        autoConnector.isInGame = false;

    }


}
