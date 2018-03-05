using System;
using System.Collections.Generic;
using System.Runtime.Serialization;
using UnityEngine;
using UnityEngine.UI;
using System.Net;
using System.Net.Sockets;


public class UDPConnection : MonoBehaviour
{
	#region Data
	public ConnectionSettings settings;

	/// <summary>
	/// IP for clients to connect to. Null if you are the server.
	/// </summary>
	public IPAddress serverIp;

	IPEndPoint serverEndPoint;

	UdpClient connection;
	#endregion

	#region Unity Events
	public void Awake()
	{
		serverIp = IPAddress.Parse (settings.serverAdress);
		serverEndPoint = new IPEndPoint (serverIp, settings.port);

		connection = new UdpClient (settings.port);
		connection.BeginReceive(OnReceive, null);
	}

	private void OnApplicationQuit()
	{
		connection.Close();
	}
	#endregion

	#region API
	public void Send(string message)
	{
		byte[] data = System.Text.Encoding.UTF8.GetBytes(message);
		connection.Send(data, data.Length, serverEndPoint);
	}

	void OnReceive(IAsyncResult ar)
	{
		try
		{
			IPEndPoint ipEndpoint = null;
			byte[] data = connection.EndReceive(ar, ref ipEndpoint);

			string message = System.Text.Encoding.UTF8.GetString(data);

			MessageReceived(message);
		}
		catch(SocketException e)
		{
			// This happens when a client disconnects, as we fail to send to that port.
			Debug.Log ("catch!");

		}finally{
			Debug.Log ("Contunie Receiving");
			connection.BeginReceive(OnReceive, null);
		
		}

	}

	internal void Send(string message, IPEndPoint ipEndpoint)
	{
		byte[] data = System.Text.Encoding.UTF8.GetBytes(message);
		connection.Send(data, data.Length, ipEndpoint);
	}

	public void MessageReceived(string message)
	{
		//Debug.Log (message);

		if(MessageReceivedEvent != null)
			MessageReceivedEvent.Invoke (message);
	
	}

	public delegate void MessageReceivedDelegate(string message);
	public event MessageReceivedDelegate MessageReceivedEvent;

	#endregion
}

