using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.events;

public class PCKDLListener : GameEventUser {

	public NetworkPickupOrchestrator orchestrator;

	//PCKDL
	public override void OnEventInvoked (object eventData)
	{
		
		string[] args = (string[])eventData;


		//Dispatch to orchestrator
		orchestrator.PCKDL (int.Parse (args [0]));

	}


}
