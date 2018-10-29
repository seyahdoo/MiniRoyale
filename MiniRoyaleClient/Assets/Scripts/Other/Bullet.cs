using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.pooling.v3;

public class Bullet : MonoBehaviour, IPoolable {

	[SerializeField]
	private Rigidbody2D rb;

	public void SHOTT(float posx, float posy, float angle, float speed){

		transform.position = new Vector2 (posx, posy);
		/*
		rb.velocity = new Vector2 (
			Mathf.Cos (Mathf.Deg2Rad * angle),
			Mathf.Sin (Mathf.Deg2Rad * angle)) 
			* speed
			;

		*/

	}

    public void OnPoolInstantiate()
    {
    }

    public void OnPoolRelease()
    {
        rb.velocity = Vector3.zero;
    }

    public void OnPoolGet()
    {
    }
}
