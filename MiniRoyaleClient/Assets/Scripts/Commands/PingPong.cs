using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.events;

public class PingPong : GameEventUser {

	public UDPConnection Connection;

	public long ping;

	public System.Diagnostics.Stopwatch stopwatch = new System.Diagnostics.Stopwatch();

	public bool doPing;
	void Update(){
		if (doPing) {
			doPing = false;
			Ping ();
		}
	}

	public override void OnEventInvoked (object eventData)
	{
		Debug.Log ("Ping Got! PONG!");
		Connection.Send ("PONG;");
	}

	void Ping(){
		stopwatch.Reset ();
		stopwatch.Start ();
		Connection.Send ("PING;");
	}

	public void OnPong(){

		stopwatch.Stop ();
		ping = stopwatch.ElapsedMilliseconds;

		Debug.Log ("Ping: "+ping);
	}

}
