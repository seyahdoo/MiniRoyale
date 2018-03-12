using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.events;

public class MOVDListener : GameEventUser {

	public NetworkRivalOrchestrator orchestrator;

	//MOVD
	public override void OnEventInvoked (object eventData)
	{

		if (eventData == null) {
			Debug.Log ("MOVD event data must not be null");
			return;
		}

		if(eventData.GetType() != typeof(string[]) ){
			Debug.Log ("event data must be type of string[]");
			return;
		}

		string[] args = (string[])eventData;

		if (args.Length != 3) {
			Debug.Log ("MOVD will get 3 arguments!");
			return;
		}


		orchestrator.MOVD (int.Parse (args [0]), float.Parse (args [1]), float.Parse (args [2]));


	}


}
