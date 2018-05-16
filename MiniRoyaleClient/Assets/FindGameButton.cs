using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class FindGameButton : MonoBehaviour {

	[SerializeField] UDPConnection connection;

	[SerializeField] Button button;

	public void ButtonPressed(){
		connection.ResetAdress ();
		connection.Send ("MATCH;");
		Invoke ("ReenableButton", 5f);
	}

	void ReenableButton(){
		button.interactable = true;
	}

}
