using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.events;

public class PingoPongo : GameEventUser {

	public UDPConnection Connection;

	public long ping;

	public System.Diagnostics.Stopwatch stopwatch = new System.Diagnostics.Stopwatch();

	public bool doPingo;
	void Update(){
		if (doPingo) {
			doPingo = false;
			Pingo ();
		}
	}

	public override void OnEventInvoked (object eventData)
	{
		//Debug.Log ("Pingo Got! PONGO!");
		Connection.Send ("PONGO;");
	}

	void Pingo(){
		stopwatch.Reset ();
		stopwatch.Start ();
		Connection.Send ("PINGO;");
	}

	public void OnPongo(){

		stopwatch.Stop ();
		ping = stopwatch.ElapsedMilliseconds;

		//Debug.Log ("Pingo: "+ping);
	}

}
