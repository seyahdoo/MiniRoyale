using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.events;

public class FOUNDListener : GameEventUser {

	[SerializeField] UDPConnection connection;
	[SerializeField] GameObject playerObject;

	public override void OnEventInvoked (object eventData)
	{

		string[] args = (string[])eventData;

		Debug.Log (args [0] + ":" + args [1]);

		connection.ChangeAdress (args [0]);
		connection.ChangePort (int.Parse(args [1]));

		connection.Send ("CNNRQ;");

		playerObject.SetActive (true);


	}


}
