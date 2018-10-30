using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.events;
using System;
using RoboRyanTron.Unite2017.Variables;
using seyahdoo.pooling.v3;

public class NetworkRivalOrchestrator : MonoBehaviour {

	private Dictionary<int,Rival> rivals;

	[SerializeField]
	private GameObject rivalPrefab;

	[SerializeField]
	private int rivalStartpoolCount = 10;

    [SerializeField] IntegerReference SelfPlayerID;
    [SerializeField] Player player;

    void Awake(){
		rivals = new Dictionary<int, Rival> ();

        Pool.CreatePool<Rival>(rivalPrefab, rivalStartpoolCount, 1000);

	}

    void RelaseAllRivals()
    {

        Pool.ReleaseAll<Rival>();

        rivals.Clear();

    }


	void Update(){
		
		float time = Time.time;

		foreach (Rival rival in rivals.Values) {
			rival.Interpolate (time);
		}

	}

	private Rival CreateRival(int playerID){
		Rival r;

        r = Pool.Get<Rival>();
		r.PlayerID = playerID;
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

    public Pawn GetPawn(int playerID) {
        Pawn pawn;

        if (playerID == SelfPlayerID.Value)
        {
            Debug.Log("Self Pawn Get!" + playerID +":"+ SelfPlayerID.Value);
            pawn = player.pawn;
        }
        else
        {
            pawn = GetRival(playerID).pawn;
        }

        return pawn;
    }

	public void PINFO(int playerId, string playerName, bool isDead){

        Pawn pawn = GetPawn(playerId);

        pawn.PlayerName = playerName;

		if (isDead) {
			pawn.Killed ();
		}

	}

	public void MOVED(int playerID,float posx,float posy,float rot){

        //dont move yourself
        if (playerID == player.GetPlayerID()) {
            return;
        }

		Rival rival = GetRival (playerID);

        rival.SetPosition (new Vector2(posx,posy),rot);

	}

	public void KILED(int playerID){

		Pawn pawn = GetPawn (playerID);

        pawn.Killed ();

	}

    public void Cleanup()
    {

        RelaseAllRivals();

    }


}
