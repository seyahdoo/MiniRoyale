using seyahdoo.pooling.v3;
using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NetworkPropOrchestrator : MonoBehaviour {

    public GameObject circlePropPrefab;
    public GameObject squarePropPrefab;

	void Awake(){

        Pool.CreatePool<CircleProp>(circlePropPrefab, 100, 1000);
        Pool.CreatePool<SquareProp>(squarePropPrefab, 100, 1000);

    }


	public Dictionary<int, Prop> props = new Dictionary<int, Prop> ();

	public void PROPP(int propID, int PropType, float posx, float posy, float rot){

		Prop p;

		if (!props.ContainsKey (propID)) {

            switch (PropType)
            {
                case 7001:
                    p = Pool.Get<CircleProp>();
                    break;
                case 7002:
                    p = Pool.Get<SquareProp>();
                    break;
                default:
                    p = Pool.Get<SquareProp>();
                    break;
            }

			props.Add (propID, p);
		} else {
			p = props [propID];
		}

		p.SetPosition (posx, posy, rot);

		
	}

    internal void Cleanup()
    {
        Pool.ReleaseAll<SquareProp>();
        Pool.ReleaseAll<CircleProp>();

        props.Clear();
    }
}
