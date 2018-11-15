using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.events;

public class CRCLEListener : GameEventUser {

    public SafeZone zone;

	public override void OnEventInvoked (object eventData)
	{

        string[] args = (string[])eventData;

        zone.UpdateCirclePos(
            float.Parse(args[0]), 
            float.Parse(args[1]), 
            float.Parse(args[2]));

	}


}
