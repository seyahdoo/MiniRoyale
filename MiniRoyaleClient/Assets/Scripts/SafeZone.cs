using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SafeZone : MonoBehaviour {

    public GameObject SafezoneObject;

    public void UpdateCirclePos(float CenterPosX, float CenterPosY, float Radius)
    {
        SafezoneObject.transform.position = new Vector2(CenterPosX, CenterPosY);
        SafezoneObject.transform.localScale = Vector2.one * Radius;
    }
	
	// Update is called once per frame
	void Update () {
	    
        
	}


}
