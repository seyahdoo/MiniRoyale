using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NetworkItemOrchestrator : MonoBehaviour {


	public UDPConnection connection;

	public NetworkRivalOrchestrator rivalOrchestrator;


	public void RequestItemInfo(int playerID){
	
		connection.Send ("PIREQ:" + playerID + ";");

	}




	public void PINFO(int playerId, string playerName, List<UniqueItem> items){

		//Debug.Log ("PINFO!");


		Rival rival = rivalOrchestrator.GetRival (playerId);


		foreach (var item in items) {
			//Debug.Log ("Trying to equip:"+item.item.itemName);

			rival.pawn.EquipThreadSafe (item);
		}

	
	}



}
