using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.events;

public class KILEDListener : GameEventUser {


	[SerializeField] private NetworkRivalOrchestrator orchestrator;
	[SerializeField] private KillFeedUI killFeed;



	//KILED
	public override void OnEventInvoked (object eventData)
	{
		string[] args = (string[])eventData;

		//Dispatch to orchestrator
		orchestrator.KILED (int.Parse (args [0]));
		killFeed.KILED (args [1], args [3], args [4]);
	}



}
