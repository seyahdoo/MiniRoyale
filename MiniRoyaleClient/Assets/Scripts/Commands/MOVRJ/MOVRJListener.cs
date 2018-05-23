using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.events;

public class MOVRJListener : GameEventUser {

	[SerializeField] Player player;

	//movement rejected, teleport back!
	public override void OnEventInvoked (object eventData)
	{

		string[] args = (string[])eventData;

		player.SetPosition (float.Parse (args [0]), float.Parse (args [1]));

	}


}
