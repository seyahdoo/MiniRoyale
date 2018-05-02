using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CommandDispatcher : MonoBehaviour {

	public UDPConnection Connection;
	public List<ServerCommandHandler> CommandHandlers;

	public UpdateTimer timer;

	#region dispatch Module

	void OnEnable(){
		Connection.MessageReceivedEvent += Connection_MessageReceivedEvent;
	}

	void OnDisable(){
		Connection.MessageReceivedEvent -= Connection_MessageReceivedEvent;
	}

	readonly char[] commandSplitter = {';'};

	void Connection_MessageReceivedEvent (string message){
		//Debug.Log ("Dispatching: " + message);

		//Lag Debugging
		//timer.Doit();

		string[] splitted = message.Split (commandSplitter, System.StringSplitOptions.RemoveEmptyEntries);

		foreach (string command in splitted) {

			//Debug.Log ("CommandDispatcher:" + command);

			foreach (ServerCommandHandler commandHandler in CommandHandlers) {

				if (command.Substring(0,5) == (commandHandler.CommandCode)) {

					//Debug.Log ("Parsing for: " + commandHandler.CommandCode +". Thee: "+ command);

					if (commandHandler.ArgumentCount > 0) {

						string[] args = 
							//strip "COMMAND:" in "CMND:xx,yy,tt"
							command.Substring (6)

							//split args
								.Split (',');

						TriggerQueueElement tqe = new TriggerQueueElement (commandHandler, args);

						lock (triggerQueueLock) {
							//Queue the command
							triggerQueue.Enqueue (tqe);
						}

					} else {

						TriggerQueueElement tqe = new TriggerQueueElement (commandHandler, null);

						lock (triggerQueueLock) {
							//Queue the command
							triggerQueue.Enqueue (tqe);
						}

					}

				}

			}

		}

	}

	#endregion

	#region TriggerQueue
	private class TriggerQueueElement{
		public ServerCommandHandler handler;
		public string[] args;

		public TriggerQueueElement(ServerCommandHandler handler, string[] args){
			this.handler = handler;
			this.args = args;
		}

		public void Trigger(){
			handler.TriggerCommand (args);
		}
	}

	Queue<TriggerQueueElement> triggerQueue = new Queue<TriggerQueueElement>();
	private Object triggerQueueLock = new Object();

	void Update(){

		lock (triggerQueueLock) {
			
			while (triggerQueue.Count > 0) {
				triggerQueue.Dequeue ().Trigger ();
			}

		}

	}
	#endregion


}