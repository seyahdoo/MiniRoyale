using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.events;

public class PingoPongo : GameEventUser {

	public UDPConnection Connection;

	public long ping;

	public System.Diagnostics.Stopwatch stopwatch = new System.Diagnostics.Stopwatch();
    
    /// <summary>
    /// this will be listened from AutoConnector
    /// </summary>
    public float lastHeardFromServer = 0f;

	public bool doPingo;
	void Update(){

		if (doPingo) {
			doPingo = false;
			SendPingo ();
		}
	}

	public override void OnEventInvoked (object eventData)
	{
        OnPingo();
	}

	public void SendPingo(){
		stopwatch.Reset ();
		stopwatch.Start ();
		Connection.Send ("PINGO;");
	}

    public void OnPingo()
    {
        //Debug.Log ("Pingo Got! PONGO!");
        Connection.Send("PONGO;");

        lastHeardFromServer = Time.time;
    }

	public void OnPongo(){

		stopwatch.Stop ();
		ping = stopwatch.ElapsedMilliseconds;
        //Debug.Log ("Pingo: "+ping);

        lastHeardFromServer = Time.time;
	}

}
