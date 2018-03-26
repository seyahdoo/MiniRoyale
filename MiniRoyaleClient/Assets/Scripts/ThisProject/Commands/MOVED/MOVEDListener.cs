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

		//Argument check
		if (eventData == null) {
			Debug.Log ("MOVED event data must not be null");
			return;
		}

		if(eventData.GetType() != typeof(string[]) ){
			Debug.Log ("event data must be type of string[]");
			return;
		}

		string[] args = (string[])eventData;

		if (args.Length != 5) {
			Debug.Log ("MOVED will get 5 arguments!");
			return;
		}
		////////////////


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
