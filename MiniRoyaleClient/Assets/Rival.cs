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

	public float NewRotation;
	public float OldRotation;

	public Transform myTransform;
	public GameObject myGameObject;

	bool positionJustUpdated = false;

	public Sprite DeadSprite;

	void Awake(){
		myTransform = transform;
		myGameObject = gameObject;
	}


	public void setPosition(Vector2 pos,float rot){
		OldPosition = NewPosition;
		OldPositionTime = NewPositionTime;
		NewPosition = pos;


		OldRotation = NewRotation;
		NewRotation = rot;


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

		float rot = Mathf.Lerp (
			            OldRotation, NewRotation,
			            (currentTime - NewPositionTime) / (NewPositionTime - OldPositionTime)
		            );

		myTransform.position = pos;
		myTransform.localEulerAngles = new Vector3 (0f, 0f, rot);

	}

	public void Killed ()
	{

		Debug.Log ("im dead");

		pawn.bodyRenderer.sprite = DeadSprite;
		pawn.weaponRenderer.sprite = null;

	}




}
