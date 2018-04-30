using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using RoboRyanTron.Unite2017.Variables;

public class TempJoiner : MonoBehaviour {

	public UDPConnection connection;

	public IntegerReference PlayerID;

	public GameObject player;

	void Start(){
		//Give Random PlayerID
		PlayerID.Variable.SetValue(Random.Range (int.MinValue, int.MaxValue));

		connection.Send ("CNNRQ;");


		player.SetActive (true);

	}
}
