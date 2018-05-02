﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NetworkItemOrchestrator : MonoBehaviour {


	public UDPConnection connection;

	public NetworkRivalOrchestrator rivalOrchestrator;


	public void RequestItemInfo(int playerID){

		//Debug.Log (connection.ServerEndPoint.Address+":"+connection.ServerEndPoint.Port + ">" +"Requesting item info");

		connection.Send ("PIREQ:" + playerID + ";");

	}




	public void PINFO(int playerId, string playerName, List<UniqueItem> items){

		Rival rival = rivalOrchestrator.GetRival (playerId);

		foreach (var item in items) {
			//Debug.Log ("Trying to equip:"+item.item.itemName);

			rival.pawn.EquipThreadSafe (item);
		}

	
	}



}
