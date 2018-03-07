using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.events;

public class PongListener : GameEventUser {

	public PingPong pinger; 

	public override void OnEventInvoked (object eventData)
	{
		pinger.OnPong ();
	}


}
