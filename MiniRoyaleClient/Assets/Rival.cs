using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Rival : MonoBehaviour {

	public int PlayerID;

	public Vector2 CurrentPosition;
	public Vector2[] OldPositions;

	public Transform myTransform;
	public GameObject myGameObject;

	void Awake(){
		myTransform = transform;
		myGameObject = gameObject;
	}


	public void setPosition(Vector2 pos){
		CurrentPosition = pos;

		//TODO interpolation

	}

}
