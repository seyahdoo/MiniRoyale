using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NetworkBulletOrchestrator : MonoBehaviour {

	public GameObject BulletPrefab;



	//SHOTT:bullet_id,posx,posy,bullet_speed;
	public void SHOTT(int id, float posx, float posy, float angle, float speed){


		GameObject bulletobj = GameObject.Instantiate (BulletPrefab); 

		Bullet b = bulletobj.GetComponent<Bullet> ();

		b.SHOTT (posx, posy, angle, speed);



	}



	void Update(){




	}


}
