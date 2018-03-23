using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using MFatihMAR.EasySockets;
using System.Net;


public class UDPConnection : MonoBehaviour {

	//holds ip and port data of server
	public ConnectionSettings settings;

	//connection manager object
	UdpPeer connection = new UdpPeer ();

	//Ip and port information of server (can change dynamically) 
	IPEndPoint ServerEndPoint;

	void Awake(){

		//Set Server ip port
		ServerEndPoint = new IPEndPoint (IPAddress.Parse (settings.serverAdress), settings.port);

		//Start to listen server
		connection.Start (new IPEndPoint (IPAddress.Any, 0));

	}

	void OnEnable(){
		//data events
		connection.OnData += Connection_OnData;
	}
		
	void OnDisable(){
		//data events
		connection.OnData -= Connection_OnData;
	}

	/// <summary>
	/// Changes the port of server connection.
	/// </summary>
	/// <param name="port">Port.</param>
	public void ChangePort(int port){
		ServerEndPoint.Port = port;
	}

	/// <summary>
	/// Send the specified message to server endpoint via UDP.
	/// </summary>
	/// <param name="message">Message.</param>
	public void Send(string message)
	{
		//Debug.Log ("UDP:Sending:" + message);

		//Encode data as UTF8
		byte[] data = System.Text.Encoding.UTF8.GetBytes(message);

		//Send to server through connection manager
		connection.Send (ServerEndPoint, data);
	}

	/// <summary>
	/// When a Data received from client Port
	/// </summary>
	/// <param name="remoteIPEP">Server IP</param>
	/// <param name="data">DATA as bytes</param>
	void Connection_OnData (System.Net.IPEndPoint remoteIPEP, byte[] data)
	{
		//Decode data as UTF8
		string message = System.Text.Encoding.UTF8.GetString(data);

		//Invoke message received
		MessageReceived (message);
	}

	/// <summary>
	/// Message event as decoded string
	/// </summary>
	/// <param name="message">Decoded message</param>
	public void MessageReceived(string message)
	{
		//Debug.Log ("UDP:Received:"+message);

		//Message Received event for listeners
		if(MessageReceivedEvent != null)
			MessageReceivedEvent.Invoke (message);
	}

	//Message Received Event
	public delegate void MessageReceivedDelegate(string message);
	public event MessageReceivedDelegate MessageReceivedEvent;


}
