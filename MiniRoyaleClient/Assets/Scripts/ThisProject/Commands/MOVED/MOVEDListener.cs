using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.events;

public class MOVEDListener : GameEventUser {

	public NetworkRivalOrchestrator orchestrator;

	int lastpkg;

	//MOVED
	public override void OnEventInvoked (object eventData)
	{
		//Debug.Log ("MOVED!");

		if (eventData == null) {
			Debug.Log ("MOVED event data must not be null");
			return;
		}

		if(eventData.GetType() != typeof(string[]) ){
			Debug.Log ("event data must be type of string[]");
			return;
		}

		string[] args = (string[])eventData;

		if (args.Length != 4) {
			Debug.Log ("MOVED will get 4 arguments!");
			return;
		}

		int nowpkg = int.Parse (args [1]);

		if (lastpkg > nowpkg) {
			return;
		}

		orchestrator.MOVED (int.Parse (args [1]), float.Parse (args [2]), float.Parse (args [3]));


	}


}
