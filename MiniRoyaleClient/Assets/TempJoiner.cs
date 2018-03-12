using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using RoboRyanTron.Unite2017.Variables;

public class TempJoiner : MonoBehaviour {

	public UDPConnection connection;

	public IntegerReference PlayerID;

	public GameObject player;

	void Start(){
		//PlayerID.Variable.Value = Random.Range (int.MinValue, int.MaxValue);

		connection.Send ("JOIN:" + PlayerID.Value + ";");

		player.SetActive (true);

	}
}
