using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.events;

public class SAIDListener : GameEventUser {

	public ChatSender chatSender;

	public override void OnEventInvoked (object eventData)
	{
		//Try to Get Data
		string[] args = null;
		if (eventData != null) {
			if (eventData.GetType() == typeof(string[])) {
				args = (string[])eventData;
			}
		}

		if (args.Length != 2) {
			Debug.LogError ("SAID expected 2 arguments!");
			return;
		}

		chatSender.MessageReceived (args[0],args[1]);

	}

}
