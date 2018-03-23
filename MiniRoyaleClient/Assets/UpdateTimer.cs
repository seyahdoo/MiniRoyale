using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class UpdateTimer : MonoBehaviour {


	public void Doit(){
		doit = true;
	}
	bool doit = false;


	void Update(){
		if (doit) {
			doit = false;
			PrintLag ();
		}
	}

	#region LagModule

	[SerializeField]
	float LastPacketTime = 0f;

	[SerializeField]
	float MaxLag = float.MinValue;

	[SerializeField]
	float MinLag = float.MaxValue;

	[SerializeField]
	float Lag;

	void PrintLag(){
		float CurrentTime = Time.time;
		float Lag = CurrentTime - LastPacketTime;
		if (Lag > MaxLag)
			MaxLag = Lag;
		if (Lag < MinLag)
			MinLag = Lag;

		//print (Lag);

		LastPacketTime = CurrentTime;
	}

	#endregion


}
