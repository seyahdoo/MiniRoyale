/*
 *   C++ sockets on Unix and Windows
 *   Copyright (C) 2002
 *
 *   This program is free software; you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation; either version 2 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program; if not, write to the Free Software
 *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

#include "PracticalSocket.h" // For UDPSocket and SocketException
#include "PlayerInformation.h"	
#include "Timer.h"

#include <iostream>          // For cout and cerr
#include <cstdlib>           // For atoi()

 //const int ECHOMAX = 255;     // Longest string to echo
const int ECHOMAX = 256;     // Longest string to echo

int main(int argc, char *argv[]) {

	if (argc != 2) {                  // Test for correct number of parameters
		cerr << "Usage: " << argv[0] << " <Server Port>" << endl;
		exit(1);
	}

	unsigned short echoServPort = atoi(argv[1]);     // First arg:  local port

	try {
		UDPSocket sock(echoServPort);

		char echoBuffer[ECHOMAX];         // Buffer for echo string
		int recvMsgSize;                  // Size of received message
		string sourceAddress;             // Address of datagram source
		unsigned short sourcePort;        // Port of datagram source

		vector<PlayerInformation*> players;
		Timer clockCounter;
		int requestType;
		for (;;) {  // Run forever
		  // Block until receive message from a client

			recvMsgSize = sock.recvFrom(echoBuffer, ECHOMAX, sourceAddress, sourcePort);
			requestType = sock.getRequestType(echoBuffer, sourceAddress, sourcePort, players);
			switch (requestType) {
			case -4:
				cout << "CurrentMovementMagnitude is higher that maxmimumPossibleMovementMagnitude, failed to update movement request from address: " << sourceAddress << ":" << sourcePort << endl << endl;
				break;
			case -3:
				cout << "Failed to find the playerID that has came from address: " << sourceAddress << ":" << sourcePort << endl << endl;
				break;
			case -2:
				cout << "There are no playerId for given address parameters" << endl << endl;
				break;
			case -1:
				cout << "players.size() returns 0" << endl << endl;
				break;
			case 1:
				cout << "Successful JOIN by " << sourceAddress << ":" << sourcePort << endl << endl;
				break;
			case 2:
				cout << "Player with address " << sourceAddress << ":" << sourcePort << " has succesfully send a message" << endl << endl;
				break;
			case 3:
				cout << "Succesfully sent PING requests to players " << endl << endl;
				break;
			case 4:
				cout << "Succesfully get PONG from address: " << sourceAddress << ":" << sourcePort << endl << endl;
				break;
			case 5:
				cout << "Succesfully moved player from address: " << sourceAddress << ":" << sourcePort << endl << endl;
				break;
			}
			//cout << "Received packet from " << sourceAddress << ":" << sourcePort << endl;
			//sock.sendTo(echoBuffer, recvMsgSize, sourceAddress, sourcePort);


		}
		/*if (clockCounter.seconds_elapsed() >= 5) {
			if (players.size() > 0) {
				char ping[6] = "PING;";
				requestType = sock.getRequestType(ping, sourceAddress, sourcePort, players);

			}
			/*
			if(players.size() > 0){
			int playerIndexFromVector;
			for(playerIndexFromVector = 0; playerIndexFromVector < players.size(); playerIndexFromVector++){
			if(!players[playerIndexFromVector]->getIsStillConnected()){

			}
			}

			char ping[6] = "PING;";
			requestType = sock.getRequestType(ping, sourceAddress, sourcePort, players);
			}
			clockCounter.reset();
		}*/
	}
	catch (SocketException &e) {
		cerr << e.what() << endl;
		exit(1);
	}
	// NOT REACHED

	return 0;
}



// Kendimi ping yap, pong don 
// requestType fonksiyonu yap, butun request tiplerini farklı modüllere yaz
// multithread yap
