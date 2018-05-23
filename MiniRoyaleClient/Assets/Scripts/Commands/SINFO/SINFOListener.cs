using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using seyahdoo.events;
using RoboRyanTron.Unite2017.Variables;

public class SINFOListener : GameEventUser {

    [SerializeField] IntegerReference SelfPlayerID;

	//SINFO:SelfPlayerID; -> Self player Info
	public override void OnEventInvoked (object eventData)
	{
		string[] args = (string[])eventData;

        SelfPlayerID.Variable.SetValue(int.Parse(args[0]));
    }



}
