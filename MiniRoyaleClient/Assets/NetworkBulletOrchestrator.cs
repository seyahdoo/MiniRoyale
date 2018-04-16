using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NetworkBulletOrchestrator : MonoBehaviour {

	public GameObject BulletPrefab;

	public Dictionary<int,Bullet> bullets = new Dictionary<int, Bullet> ();


	//SHOTT:bullet_id,posx,posy,bullet_speed;
	public void SHOTT(int id, float posx, float posy, float angle, float speed){

		//print (id);

		if (!bullets.ContainsKey (id)) {
			GameObject bulletobj = GameObject.Instantiate (BulletPrefab); 
			Bullet b = bulletobj.GetComponent<Bullet> ();

			bullets.Add (id, b);

			b.SHOTT (posx, posy, angle, speed);

		} else {

			bullets [id].SHOTT (posx, posy, angle, speed);

		}


	}

	/// <summary>
	/// Tries the delete bullet with given id
	/// </summary>
	/// <returns><c>true</c>, if bullet was deleted, <c>false</c> if there is no bullet with given id.</returns>
	/// <param name="id">Identifier.</param>
	public bool TryDeleteBullet(int id){

		if (bullets.ContainsKey (id)) {
			Bullet b = bullets [id];
			b.Delete ();
			return true;
		
		} else {
			return false;
		}

	}


}
