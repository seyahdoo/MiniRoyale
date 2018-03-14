using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.events;

public class PortoListener : GameEventUser {

	public UDPConnection connection;

	//PORTO
	public override void OnEventInvoked (object eventData)
	{
		//Debug.Log ("PORTo!!!!!!!!");

		if (eventData == null) {
			Debug.Log ("PORTO event data must not be null");
			return;
		}

		if(eventData.GetType() != typeof(string[]) ){
			Debug.Log ("event data must be type of string[]");
			return;
		}

		string[] args = (string[])eventData;

		if (args.Length != 1) {
			Debug.Log ("PORTO will get 1 arguments!");
			return;
		}

		connection.ChangePort (int.Parse (args [0]));

	}

}
