using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.events;
using System;

public class NetworkRivalOrchestrator : MonoBehaviour {

	private Dictionary<int,Rival> rivals;

	[SerializeField]
	private GameObject rivalPrefab;

	private Stack<Rival> rivalPool;

	private Stack<GameObject> EnableQueue;

	[SerializeField]
	private int rivalStartpoolCount = 10;

	void Awake(){
		rivals = new Dictionary<int, Rival> ();
		rivalPool = new Stack<Rival> ();

		for (int i = 0; i < rivalStartpoolCount; i++) {
			GrowRivalPool ();
		}

		EnableQueue = new Stack<GameObject> ();
	}

	void GrowRivalPool(){
	
		GameObject rivalobj = Instantiate (rivalPrefab);
		Rival rival = rivalobj.GetComponent<Rival> ();
		rivalobj.SetActive (false);

		rivalPool.Push (rival);
	}


	void Update(){
		
		while (EnableQueue.Count > 0) {
			EnableQueue.Pop ().SetActive (true);
		}

		float time = Time.time;

		foreach (Rival rival in rivals.Values) {
			rival.Interpolate (time);
		}

	}

	private Rival CreateRival(int playerID){
		Rival r;

		//TODO: POOL THIS!
		//Create Rival
		if (rivalPool.Count <= 0) {
			//TODO
			Debug.LogError ("DEAL WITH THIS!!!");
		}

		r = rivalPool.Pop ();
		r.PlayerID = playerID;

		//TODO
		EnableQueue.Push (r.myGameObject);

		rivals.Add (playerID, r);

		//Request player Info (like what he wears)
		itemOrchestrator.RequestItemInfo (playerID);

		return r;
	}

	public NetworkItemOrchestrator itemOrchestrator;

	public Rival GetRival(int playerID){

		//Debug.LogError ("NetworkItemOrchestrator:GetRival:" + playerID);

		Rival rival;
		//Find rival from dictionary
		if (rivals.ContainsKey (playerID)) {
			//Debug.Log("Orchestrator: Found Rival in dictionary");
			rival = rivals [playerID];
		} else {
			rival = CreateRival (playerID);
		}

		return rival;
	}
		

	public void PINFO(int playerId, string playerName, bool isDead){

		Rival rival = GetRival (playerId);

		rival.PlayerName = playerName;

		if (isDead) {
			rival.Killed ();
		}

	}

	public void MOVED(int playerID,float posx,float posy,float rot){
		//Debug.LogWarning ("Orchestrator: MOVED");

		Rival rival = GetRival (playerID);

		rival.setPosition (new Vector2(posx,posy),rot);
	}

	public void KILED(int playerID){
	

		Rival rival = GetRival (playerID);

		rival.Killed ();

	}

}
