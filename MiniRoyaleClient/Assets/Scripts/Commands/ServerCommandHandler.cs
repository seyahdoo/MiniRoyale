using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.events;

[CreateAssetMenu]
public class ServerCommandHandler : ScriptableObject {

	public string CommandCode;
	public int ArgumentCount = 0;

	public GameEvent Event;

	public void TriggerCommand(string[] args){
		if (ArgumentCount == 0) {
			Event.Raise (null);
			return;
		}

		if (args == null) {
			Debug.LogError ("Error: No arguments given when expected "+ArgumentCount+" number of arguments!");
			return;
		}
			
		if (args.Length != ArgumentCount) {
			Debug.LogError ("Error: Argument count mismatch on command "+CommandCode+"! Expecting: "+ArgumentCount+" Received: "+args.Length+"!");
			return;
		}

		Event.Raise (args);
	}

}
