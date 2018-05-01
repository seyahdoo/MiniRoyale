using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.events;

public class PROPPListener : GameEventUser {

	public NetworkPropOrchestrator orchestrator;

	//PROPP -> Setup Prop for client
	public override void OnEventInvoked (object eventData)
	{
		string[] args = (string[])eventData;

		//Dispatch to orchestrator
		orchestrator.PROPP (int.Parse (args [0]), int.Parse (args [1]), float.Parse (args [2]),float.Parse(args[3]),float.Parse(args[4]));

	}


}
