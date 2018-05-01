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

	private Transform my_transform;
	private Rigidbody2D body;

	public Camera cam;

	public GameObject crosshair;

	public bool shootCommand = false;

	//Initialize
	void Awake(){
		my_transform = transform;
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
		//body.AddForce(direction);

		Vector2 mousePos = Input.mousePosition;
		Vector3 look = cam.ScreenToWorldPoint(new Vector3(mousePos.x, mousePos.y, 10));

		my_transform.right = look - my_transform.position;

		crosshair.transform.position = look;

		if (Input.GetButtonDown ("Fire1")) {
			shootCommand = true;
		}

	}

	int pkgid = 0;

	//Send Server events
	void Tick(){
		//We will send current position to server every tick
		pkgid++;

		string tosend = "MOVER:" 
			+ pkgid + "," 
			+ my_transform.position.x + "," 
			+ my_transform.position.y + "," 
			+ my_transform.localEulerAngles.z + ";";
		
		if (shootCommand) {
			shootCommand = false;
			tosend += "SHOOT;";
		}

		//Debug.Log (tosend);
		connection.Send(tosend);

	}


}
