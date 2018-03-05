using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ChatSender : MonoBehaviour {

	public UDPConnection udp;

	public string tosend;
	public bool send = false;


	void Update(){
		if (send) {
			send = false;
			udp.Send (tosend);
		}
	
	}


}
