using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.events;

public class PCKINListener : GameEventUser {

	public NetworkPickupOrchestrator orchestrator;

	//PCKIN
	public override void OnEventInvoked (object eventData)
	{
		
		string[] args = (string[])eventData;


		//Dispatch to orchestrator
		orchestrator.PCKIN (int.Parse (args [0]), int.Parse (args [1]), float.Parse (args [2]), float.Parse (args [3]),int.Parse(args[4]));

	}


}
