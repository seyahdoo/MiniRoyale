using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.events;

public class KILEDListener : GameEventUser {

	public NetworkRivalOrchestrator orchestrator;

	//KILED
	public override void OnEventInvoked (object eventData)
	{
		string[] args = (string[])eventData;

		//Dispatch to orchestrator
		orchestrator.KILED (int.Parse (args [0]));

	}



}
