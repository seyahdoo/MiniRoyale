using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.events;

public class DELETListener : GameEventUser {

	public NetworkBulletOrchestrator bulletOrchestrator;

	public override void OnEventInvoked (object eventData)
	{

		string[] args = (string[])eventData;

		bulletOrchestrator.TryDeleteBullet (int.Parse (args [0]));

		//TODO try delete prop

	}


}
