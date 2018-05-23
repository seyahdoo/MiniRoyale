using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.events;

public class MOVEDListener : GameEventUser {

	public NetworkRivalOrchestrator orchestrator;

	int lastpkg = -1;

	//MOVED
	public override void OnEventInvoked (object eventData)
	{
		//Debug.Log ("MOVED!");

		string[] args = (string[])eventData;

		//Drop late packets
		int nowpkg = int.Parse (args [0]);
		if (lastpkg > nowpkg) {
			Debug.LogError ("Dropping Late Package!");
			return;
		} else {
			lastpkg = nowpkg;
		}

		//Dispatch to orchestrator
		orchestrator.MOVED (int.Parse (args [1]), float.Parse (args [2]), float.Parse (args [3]),float.Parse(args[4]));

	}


}
