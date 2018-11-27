using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AutoConnector : MonoBehaviour {

    /// <summary>
    /// FoundListener and EXITTListener
    /// will change this
    /// </summary>
    public bool isInGame = false;

    public float lastTryTime = -100f;
    public float tryInterval = 10f;

    [SerializeField] UDPConnection connection;

    [SerializeField] PingoPongo pingo;

    [SerializeField] EXITTListener exittListener;


    float pingTimeout = 9f;
    float pingInterval = 3f;

    void Update () {

        if (!isInGame)
        {
            if((Time.time-lastTryTime) > tryInterval)
            {
                connection.ResetAdress();
                connection.Send("MATCH;");
                lastTryTime = Time.time;
            }
        }
        else
        {

            if (Time.time - pingo.lastHeardFromServer > pingInterval)
            {
                if (Time.time - pingo.lastHeardFromServer > pingTimeout)
                {
                    exittListener.ExitGame();
                }
                else
                {
                    pingo.SendPingo();
                }
            }

                

        }

	}
}
