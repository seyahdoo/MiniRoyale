using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using RoboRyanTron.Unite2017.Variables;

[RequireComponent(typeof(Rigidbody2D))]
public class Player : MonoBehaviour {

	public UDPConnection connection;

	public IntegerReference PlayerID;

	public FloatReference Speed;
	public FloatReference TickPerSecond;

	private Transform myTransform;
	private Rigidbody2D body;

	//Initialize
	void Awake(){
		myTransform = transform;
		body = GetComponent<Rigidbody2D> ();
	}

	//TICK EVENT
	void OnEnable(){
		InvokeRepeating ("Tick", 0, 1f/TickPerSecond.Value);
	}
	void OnDisable(){
		CancelInvoke ("Tick");
	}

	public Vector2 direction;

	//Update will determine player position
	void Update(){
		direction.x = Input.GetAxis ("Horizontal");
		direction.y = Input.GetAxis ("Vertical");
		direction *= Speed.Value;

		body.velocity = direction;
	}

	//Send Server events
	void Tick(){
		//We will send current position to server every tick
		connection.Send("MOVE:"+PlayerID.Value+","+myTransform.position.x+","+myTransform.position.y+";");

	}


}
