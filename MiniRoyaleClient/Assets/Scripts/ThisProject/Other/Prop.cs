using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Prop : MonoBehaviour {

	Transform my_transform;

	void Awake(){
		my_transform = transform;
	}

	public void SetPosition(float posx, float posy, float rot){

		my_transform.position = new Vector3 (posx, posy, 0f);
		my_transform.localEulerAngles = new Vector3 (0f, 0f, rot);

	}


}
