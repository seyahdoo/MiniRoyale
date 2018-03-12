using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.events;

public class NetworkRivalOrchestrator : MonoBehaviour {

	public Dictionary<int,Rival> rivals;

	public GameObject rivalPrefab;

	public Stack<Rival> rivalPool;

	public Stack<GameObject> EnableQueue;

	public int rivalStartpoolCount = 10;

	void Awake(){
		rivals = new Dictionary<int, Rival> ();
		rivalPool = new Stack<Rival> ();

		for (int i = 0; i < rivalStartpoolCount; i++) {
			CreateRival ();
		}

		EnableQueue = new Stack<GameObject> ();
	}

	void CreateRival(){
	
		GameObject rivalobj = Instantiate (rivalPrefab);
		Rival rival = rivalobj.GetComponent<Rival> ();
		rivalobj.SetActive (false);

		rivalPool.Push (rival);
	}



	void Update(){
		
		while (EnableQueue.Count > 0) {
			EnableQueue.Pop ().SetActive (true);
		}

		foreach (Rival rival in rivals.Values) {
			rival.myTransform.position = rival.CurrentPosition; 
		}

	}

	public void MOVD(int playerID,float posx,float posy){
		//Debug.Log ("Orchestrator: MOVD");

		Rival rival;
		//Find rival from dictionary
		if (rivals.ContainsKey (playerID)) {
			//Debug.Log("Orchestrator: Found Rival in dictionary");
			rival = rivals [playerID];
		} else {
			//TODO: POOL THIS!
			//Create Rival
			Debug.Log("Orchestrator: getting Rival from pool");
			if (rivalPool.Count <= 0) {
				//TODO
				//Debug.LogError ("DEAL WITH THIS!!!");
			}

			rival = rivalPool.Pop ();
			rival.PlayerID = playerID;

			EnableQueue.Push (rival.myGameObject);

			rivals.Add (playerID, rival);
		}

		rival.setPosition (new Vector2(posx,posy));
	}


}
