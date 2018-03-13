using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CommandDispatcher : MonoBehaviour {

	public UDPConnection Connection;
	public List<ServerCommandHandler> CommandHandlers;


	void OnEnable(){
		Connection.MessageReceivedEvent += Connection_MessageReceivedEvent;
	}

	void OnDisable(){
		Connection.MessageReceivedEvent -= Connection_MessageReceivedEvent;
	}

	readonly char[] commandSplitter = {';'};

	void Connection_MessageReceivedEvent (string message)
	{
		//Debug.Log ("Dispatching: " + message);

		string[] splitted = message.Split (commandSplitter, System.StringSplitOptions.RemoveEmptyEntries);

		foreach (string command in splitted) {

			//Debug.Log ("Command: " + command +".");

			foreach (ServerCommandHandler commandHandler in CommandHandlers) {

				if (command.Substring(0,4) == (commandHandler.CommandCode)) {

					//Debug.Log ("Parsing for: " + commandHandler.CommandCode +". Thee: "+ command);

					if (commandHandler.ArgumentCount > 0) {

						string[] args = 
							//strip "COMMAND:" in "CMND:xx,yy,tt"
							command.Substring (5)

							//split args
								.Split (',');

						//Debug.Log ("Triggering with args " + commandHandler);
						//trigger the command
						commandHandler.TriggerCommand (args);
					} else {

						//Debug.Log ("Triggering " + commandHandler);
						//trigger the command
						commandHandler.TriggerCommand (null);
					}

				}
			}

		}

	}



}