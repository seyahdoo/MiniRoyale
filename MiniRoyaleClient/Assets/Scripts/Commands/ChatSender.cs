using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ChatSender : MonoBehaviour {

	public UDPConnection udp;

	public string tosend;
	public bool send = false;
	public bool join = false;

	int id;

	void Awake(){
		id = Random.Range (int.MinValue, int.MaxValue);
	}

	void Update(){
		if (send) {
			send = false;
			udp.Send ("SAYY:" + tosend +";");
		}

		if (join) {
			join = false;
			udp.Send("JOIN:"+id+";");
		}

	}

	public void MessageReceived(string playerId,string message){
		
		Debug.Log (playerId + ": " + message);


	}





}
