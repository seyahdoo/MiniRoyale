using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Rival : MonoBehaviour {

	public int PlayerID;

	public Pawn pawn;

	public float NewPositionTime;
	public float OldPositionTime;

	public Vector2 NewPosition;
	public Vector2 OldPosition;

	public float NewRotation;
	public float OldRotation;

	public Transform myTransform;
	public GameObject myGameObject;

	bool positionJustUpdated = false;

	public Sprite DeadSprite;

	public bool isDead = false;

	void Awake(){
		myTransform = transform;
		myGameObject = gameObject;
	}


	public void setPosition(Vector2 pos,float rot){
		OldPosition = NewPosition;
		OldPositionTime = NewPositionTime;
		NewPosition = pos;

		OldRotation = (NewRotation + 360) % 360;

		//Debug.Log ("Modded OldRotation:" + NewRotation +","+ OldRotation);

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



		//TODO Fix 1 to 359 interpolation bug
		if(NewRotation - OldRotation > 185){
			NewRotation -= 360;
		}

		if(OldRotation - NewRotation > 185){
			NewRotation += 360;
		}

		float rot = Mathf.Lerp (
			            OldRotation, NewRotation,
			            (currentTime - NewPositionTime) / (NewPositionTime - OldPositionTime)
		            );

		myTransform.position = pos;
		myTransform.localEulerAngles = new Vector3 (0f, 0f, rot);
		//Debug.Log (rot);
	}

	public void Killed ()
	{

		//Debug.Log ("im dead");
		isDead = true;

		pawn.bodyRenderer.sprite = DeadSprite;
		pawn.weaponRenderer.sprite = null;

	}




}
