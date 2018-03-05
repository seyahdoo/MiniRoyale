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
#include <iostream>          // For cout and cerr
#include <cstdlib>           // For atoi()

//const int ECHOMAX = 255;     // Longest string to echo
const int ECHOMAX = 1024;     // Longest string to echo

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
    for (;;) {  // Run forever
      // Block until receive message from a client
      recvMsgSize = sock.recvFrom(echoBuffer, ECHOMAX, sourceAddress, 
                                      sourcePort);
  
      cout << "Received packet from " << sourceAddress << ":" 
           << sourcePort << endl;
		
		
		char * packet = new char[ECHOMAX+1];
		strcpy(packet,echoBuffer);
		int subPacketSize = 0;
		char *mainMessage = strtok (packet,";");
		char *currentMessage = new char[strlen(mainMessage)];
		const char* attributeJoin = "JOIN";
		const char* attributeSay = "SAY";
		int playerID;
		char playerMessage[ECHOMAX-sizeof(int)];
			while (mainMessage!=0)
			  {
				  char *subMessage = strtok (mainMessage,":"); 
				//std::cout << p << '\n';
				cout << "mainMessage: " << mainMessage < endl;
				if( strcmp(subMessage, attributeJoin) == 0){
					subMessage = strtok (NULL,":");
					playerID = atoi(subMessage);
					cout << "subMessage(JOIN): " << subMessage < endl;
				}
				else if( strcmp(subMessage, attributeSay) == 0){
					subMessage = strtok (NULL,":");
					strcpy(playerMessage,subMessage);
					cout << "subMessage(SAY): " << subMessage < endl;
				}
				mainMessage = strtok(NULL,";");
			  }
			// gelen mesajı : göre ayır, duzgun parcaları dogru degiskenlere ata, eksana bas (client'a gerekli bilgileri geri don)
			string replyMessage = to_string(attributeSay) + ":" + to_string(playerID) + ", " + playerMessage;
			recvMsgSize = strlen(replyMessage);
			sock.sendTo(replyMessage, recvMsgSize, sourceAddress, sourcePort);
      //sock.sendTo(echoBuffer, recvMsgSize, sourceAddress, sourcePort);
	  delete[] currentMessage;
	  delete[] packet;
    }
  } catch (SocketException &e) {
    cerr << e.what() << endl;
    exit(1);
  }
  // NOT REACHED

  return 0;
}


// Ram'de iplerin kime ait olduklarını tut (ip,port,baglantı bilgisi clası) (udp classın nereden geldigini bilip, ona gore cevap ver)