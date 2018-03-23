using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Rival : MonoBehaviour {

	public int PlayerID;

	public Pawn pawn;

	public Vector2 NewPosition;
	public float NewPositionTime;
	public Vector2 OldPosition;
	public float OldPositionTime;

	public Transform myTransform;
	public GameObject myGameObject;

	bool positionJustUpdated = false;


	void Awake(){
		myTransform = transform;
		myGameObject = gameObject;
	}


	public void setPosition(Vector2 pos){
		OldPosition = NewPosition;
		OldPositionTime = NewPositionTime;

		NewPosition = pos;

		positionJustUpdated = true;
	}

	public void Interpolate(float currentTime){

		if (positionJustUpdated) {
			positionJustUpdated = false;
			NewPositionTime = Time.time;
		}

		Vector2 pos = Vector2.Lerp (
			              OldPosition, NewPosition,
			              (currentTime - NewPositionTime) / (NewPositionTime - OldPositionTime)
		              );

		myTransform.position = pos;

	}

}
