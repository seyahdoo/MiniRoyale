using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.events;

public class PongoListener : GameEventUser {

	public PingoPongo pinger; 

	public override void OnEventInvoked (object eventData)
	{
		pinger.OnPongo ();
	}


}
