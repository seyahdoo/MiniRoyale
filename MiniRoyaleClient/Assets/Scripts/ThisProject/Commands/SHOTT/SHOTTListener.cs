using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.events;

public class SHOTTListener : GameEventUser {

	public NetworkBulletOrchestrator orchestrator;


	//SHOTT
	public override void OnEventInvoked (object eventData)
	{
		//Debug.Log ("SHOTT!");

		//Argument check
		if (eventData == null) {
			Debug.Log ("SHOTT event data must not be null");
			return;
		}

		if(eventData.GetType() != typeof(string[]) ){
			Debug.Log ("event data must be type of string[]");
			return;
		}

		string[] args = (string[])eventData;

		if (args.Length != 5) {
			Debug.Log ("SHOTT will get 5 arguments!");
			return;
		}
		////////////////


		//Dispatch to orchestrator
		orchestrator.SHOTT (int.Parse (args [0]), float.Parse (args [1]), float.Parse (args [2]),float.Parse(args[3]),float.Parse(args[4]));


	}
}
