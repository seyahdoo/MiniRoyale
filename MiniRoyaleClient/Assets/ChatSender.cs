using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ChatSender : MonoBehaviour {

	public UDPConnection udp;

	public string tosend;
	public bool send = false;
	public bool hello = false;

	int id;

	void OnEnable(){
		udp.MessageReceivedEvent += MessageReceived;
	}

	void OnDisable(){
		udp.MessageReceivedEvent -= MessageReceived;
	}

	void Awake(){
		id = Random.Range (int.MinValue, int.MaxValue);
	}

	void Update(){
		if (send) {
			send = false;
			//udp.Send (tosend);
			udp.Send ("SAY:" + tosend +";");
		}

		if (hello) {
			hello = false;
			udp.Send("JOIN:"+id+";");
		}



	}

	void MessageReceived(string message){
		string[] splitted = message.Split (';');

		foreach (string command in splitted) {

			if (command.StartsWith ("SAID:")) {
				string[] args = command.Split (':', ',');
				Debug.Log (args [0]);
				Debug.Log (args [1]);
				Debug.Log (args [2]);
				Debug.Log (args [3]);

				//command = command.Substring (a, command.Length - b);

			}


		}


	}





}
