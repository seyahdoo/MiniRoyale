using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NetworkPropOrchestrator : MonoBehaviour {

	[SerializeField]
	private int[] propTypeIDs;
	[SerializeField]
	private GameObject[] propTypeObjects;
	private Dictionary<int, GameObject> propTypes = new Dictionary<int, GameObject>();

	void Awake(){
	
		//Propulate reference dictionary
		for (int i = 0; i < propTypeIDs.Length; i++) {
			propTypes.Add (propTypeIDs [i], propTypeObjects [i]);
		}

	}


	public Dictionary<int, Prop> props = new Dictionary<int, Prop> ();

	public void PROPP(int propID, int PropType, float posx, float posy, float rot){

		Prop p;

		if (!props.ContainsKey (propID)) {
		
			GameObject go = Instantiate (propTypes [PropType]);
			p = go.GetComponent<Prop> ();

			props.Add (propID, p);
		} else {
			p = props [propID];
		}

		p.SetPosition (posx, posy, rot);






		
	}

}
