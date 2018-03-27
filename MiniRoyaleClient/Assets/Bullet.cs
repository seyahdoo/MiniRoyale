using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Bullet : MonoBehaviour {

	[SerializeField]
	private Rigidbody2D rb;

	public void SHOTT(float posx, float posy, float angle, float speed){

		transform.position = new Vector2 (posx, posy);
		rb.velocity = new Vector2 (
			Mathf.Cos (Mathf.Deg2Rad * angle),
			Mathf.Sin (Mathf.Deg2Rad * angle)) 
			* speed
			;



	}






}
