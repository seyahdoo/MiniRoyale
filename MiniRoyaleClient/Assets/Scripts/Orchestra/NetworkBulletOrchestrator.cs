using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.pooling.v3;

public class NetworkBulletOrchestrator : MonoBehaviour {

	public GameObject BulletPrefab;

	public Dictionary<int,Bullet> bullets = new Dictionary<int, Bullet> ();

    private void Awake()
    {
        Pool.CreatePool<Bullet>(BulletPrefab, 10, 10000);
    }

    //SHOTT:bullet_id,posx,posy,bullet_speed;
    public void SHOTT(int id, float posx, float posy, float angle, float speed){

		if (!bullets.ContainsKey (id)) {

            Bullet b = Pool.Get<Bullet>();

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

            Pool.Release<Bullet>(b);
            bullets.Remove(id);

			return true;

        } else {
			return false;
		}

	}


    /// <summary>
    /// Cleanup gamescene from bullets after game finishes
    /// </summary>
    public void Cleanup()
    {
        Pool.ReleaseAll<Bullet>();

        bullets.Clear();

    }

}
