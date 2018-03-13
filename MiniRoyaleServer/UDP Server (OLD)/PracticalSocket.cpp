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

#include "PracticalSocket.h"


#ifdef WIN32
#include <winsock.h>         // For socket(), connect(), send(), and recv()
typedef int socklen_t;
typedef char raw_type;       // Type used for raw data on this platform
#else
#include <sys/types.h>       // For data types
#include <sys/socket.h>      // For socket(), connect(), send(), and recv()
#include <netdb.h>           // For gethostbyname()
#include <arpa/inet.h>       // For inet_addr()
#include <unistd.h>          // For close()
#include <netinet/in.h>      // For sockaddr_in
typedef void raw_type;       // Type used for raw data on this platform
#endif

#include <errno.h>             // For errno

using namespace std;

#ifdef WIN32
static bool initialized = false;
#endif

// SocketException Code

SocketException::SocketException(const string &message, bool inclSysMsg)
throw() : userMessage(message) {
	if (inclSysMsg) {
		userMessage.append(": ");
		userMessage.append(strerror(errno));
	}
}

SocketException::~SocketException() throw() {
}

const char *SocketException::what() const throw() {
	return userMessage.c_str();
}

// Function to fill in address structure given an address and port
static void fillAddr(const string &address, unsigned short port,
	sockaddr_in &addr) {
	memset(&addr, 0, sizeof(addr));  // Zero out address structure
	addr.sin_family = AF_INET;       // Internet address

	hostent *host;  // Resolve name
	if ((host = gethostbyname(address.c_str())) == NULL) {
		// strerror() will not work for gethostbyname() and hstrerror() 
		// is supposedly obsolete
		throw SocketException("Failed to resolve name (gethostbyname())");
	}
	addr.sin_addr.s_addr = *((unsigned long *)host->h_addr_list[0]);

	addr.sin_port = htons(port);     // Assign port in network byte order
}

// Socket Code

Socket::Socket(int type, int protocol) throw(SocketException) {
#ifdef WIN32
	if (!initialized) {
		WORD wVersionRequested;
		WSADATA wsaData;

		wVersionRequested = MAKEWORD(2, 0);              // Request WinSock v2.0
		if (WSAStartup(wVersionRequested, &wsaData) != 0) {  // Load WinSock DLL
			throw SocketException("Unable to load WinSock DLL");
		}
		initialized = true;
	}
#endif

	// Make a new socket
	if ((sockDesc = socket(PF_INET, type, protocol)) < 0) {
		throw SocketException("Socket creation failed (socket())", true);
	}
}

Socket::Socket(int sockDesc) {
	this->sockDesc = sockDesc;
}

Socket::~Socket() {
#ifdef WIN32
	::closesocket(sockDesc);
#else
	::close(sockDesc);
#endif
	sockDesc = -1;
}

string Socket::getLocalAddress() throw(SocketException) {
	sockaddr_in addr;
	unsigned int addr_len = sizeof(addr);

	if (getsockname(sockDesc, (sockaddr *)&addr, (socklen_t *)&addr_len) < 0) {
		throw SocketException("Fetch of local address failed (getsockname())", true);
	}
	return inet_ntoa(addr.sin_addr);
}

unsigned short Socket::getLocalPort() throw(SocketException) {
	sockaddr_in addr;
	unsigned int addr_len = sizeof(addr);

	if (getsockname(sockDesc, (sockaddr *)&addr, (socklen_t *)&addr_len) < 0) {
		throw SocketException("Fetch of local port failed (getsockname())", true);
	}
	return ntohs(addr.sin_port);
}

void Socket::setLocalPort(unsigned short localPort) throw(SocketException) {
	// Bind the socket to its port
	sockaddr_in localAddr;
	memset(&localAddr, 0, sizeof(localAddr));
	localAddr.sin_family = AF_INET;
	localAddr.sin_addr.s_addr = htonl(INADDR_ANY);
	localAddr.sin_port = htons(localPort);

	if (bind(sockDesc, (sockaddr *)&localAddr, sizeof(sockaddr_in)) < 0) {
		throw SocketException("Set of local port failed (bind())", true);
	}
}

void Socket::setLocalAddressAndPort(const string &localAddress,
	unsigned short localPort) throw(SocketException) {
	// Get the address of the requested host
	sockaddr_in localAddr;
	fillAddr(localAddress, localPort, localAddr);

	if (bind(sockDesc, (sockaddr *)&localAddr, sizeof(sockaddr_in)) < 0) {
		throw SocketException("Set of local address and port failed (bind())", true);
	}
}

void Socket::cleanUp() throw(SocketException) {
#ifdef WIN32
	if (WSACleanup() != 0) {
		throw SocketException("WSACleanup() failed");
	}
#endif
}

unsigned short Socket::resolveService(const string &service,
	const string &protocol) {
	struct servent *serv;        /* Structure containing service information */

	if ((serv = getservbyname(service.c_str(), protocol.c_str())) == NULL)
		return atoi(service.c_str());  /* Service is port number */
	else
		return ntohs(serv->s_port);    /* Found port (network byte order) by name */
}

// CommunicatingSocket Code

CommunicatingSocket::CommunicatingSocket(int type, int protocol)
throw(SocketException) : Socket(type, protocol) {
}

CommunicatingSocket::CommunicatingSocket(int newConnSD) : Socket(newConnSD) {
}

void CommunicatingSocket::connect(const string &foreignAddress,
	unsigned short foreignPort) throw(SocketException) {
	// Get the address of the requested host
	sockaddr_in destAddr;
	fillAddr(foreignAddress, foreignPort, destAddr);

	// Try to connect to the given port
	if (::connect(sockDesc, (sockaddr *)&destAddr, sizeof(destAddr)) < 0) {
		throw SocketException("Connect failed (connect())", true);
	}
}

void CommunicatingSocket::send(const void *buffer, int bufferLen)
throw(SocketException) {
	if (::send(sockDesc, (raw_type *)buffer, bufferLen, 0) < 0) {
		throw SocketException("Send failed (send())", true);
	}
}

int CommunicatingSocket::recv(void *buffer, int bufferLen)
throw(SocketException) {
	int rtn;
	if ((rtn = ::recv(sockDesc, (raw_type *)buffer, bufferLen, 0)) < 0) {
		throw SocketException("Received failed (recv())", true);
	}

	return rtn;
}

string CommunicatingSocket::getForeignAddress()
throw(SocketException) {
	sockaddr_in addr;
	unsigned int addr_len = sizeof(addr);

	if (getpeername(sockDesc, (sockaddr *)&addr, (socklen_t *)&addr_len) < 0) {
		throw SocketException("Fetch of foreign address failed (getpeername())", true);
	}
	return inet_ntoa(addr.sin_addr);
}

unsigned short CommunicatingSocket::getForeignPort() throw(SocketException) {
	sockaddr_in addr;
	unsigned int addr_len = sizeof(addr);

	if (getpeername(sockDesc, (sockaddr *)&addr, (socklen_t *)&addr_len) < 0) {
		throw SocketException("Fetch of foreign port failed (getpeername())", true);
	}
	return ntohs(addr.sin_port);
}

// TCPSocket Code

TCPSocket::TCPSocket()
throw(SocketException) : CommunicatingSocket(SOCK_STREAM,
	IPPROTO_TCP) {
}

TCPSocket::TCPSocket(const string &foreignAddress, unsigned short foreignPort)
throw(SocketException) : CommunicatingSocket(SOCK_STREAM, IPPROTO_TCP) {
	connect(foreignAddress, foreignPort);
}

TCPSocket::TCPSocket(int newConnSD) : CommunicatingSocket(newConnSD) {
}

// TCPServerSocket Code

TCPServerSocket::TCPServerSocket(unsigned short localPort, int queueLen)
throw(SocketException) : Socket(SOCK_STREAM, IPPROTO_TCP) {
	setLocalPort(localPort);
	setListen(queueLen);
}

TCPServerSocket::TCPServerSocket(const string &localAddress,
	unsigned short localPort, int queueLen)
	throw(SocketException) : Socket(SOCK_STREAM, IPPROTO_TCP) {
	setLocalAddressAndPort(localAddress, localPort);
	setListen(queueLen);
}

TCPSocket *TCPServerSocket::accept() throw(SocketException) {
	int newConnSD;
	if ((newConnSD = ::accept(sockDesc, NULL, 0)) < 0) {
		throw SocketException("Accept failed (accept())", true);
	}

	return new TCPSocket(newConnSD);
}

void TCPServerSocket::setListen(int queueLen) throw(SocketException) {
	if (listen(sockDesc, queueLen) < 0) {
		throw SocketException("Set listening socket failed (listen())", true);
	}
}

// UDPSocket Code

UDPSocket::UDPSocket() throw(SocketException) : CommunicatingSocket(SOCK_DGRAM,
	IPPROTO_UDP) {
	setBroadcast();
}

UDPSocket::UDPSocket(unsigned short localPort)  throw(SocketException) :
	CommunicatingSocket(SOCK_DGRAM, IPPROTO_UDP) {
	setLocalPort(localPort);
	setBroadcast();
}

UDPSocket::UDPSocket(const string &localAddress, unsigned short localPort)
throw(SocketException) : CommunicatingSocket(SOCK_DGRAM, IPPROTO_UDP) {
	setLocalAddressAndPort(localAddress, localPort);
	setBroadcast();
}

void UDPSocket::setBroadcast() {
	// If this fails, we'll hear about it when we try to send.  This will allow 
	// system that cannot broadcast to continue if they don't plan to broadcast
	int broadcastPermission = 1;
	setsockopt(sockDesc, SOL_SOCKET, SO_BROADCAST,
		(raw_type *)&broadcastPermission, sizeof(broadcastPermission));
}

void UDPSocket::disconnect() throw(SocketException) {
	sockaddr_in nullAddr;
	memset(&nullAddr, 0, sizeof(nullAddr));
	nullAddr.sin_family = AF_UNSPEC;

	// Try to disconnect
	if (::connect(sockDesc, (sockaddr *)&nullAddr, sizeof(nullAddr)) < 0) {
#ifdef WIN32
		if (errno != WSAEAFNOSUPPORT) {
#else
		if (errno != EAFNOSUPPORT) {
#endif
			throw SocketException("Disconnect failed (connect())", true);
		}
	}
}

void UDPSocket::sendTo(const void *buffer, int bufferLen,
	const string &foreignAddress, unsigned short foreignPort)
	throw(SocketException) {
	sockaddr_in destAddr;
	fillAddr(foreignAddress, foreignPort, destAddr);

	// Write out the whole buffer as a single message.
	if (sendto(sockDesc, (raw_type *)buffer, bufferLen, 0,
		(sockaddr *)&destAddr, sizeof(destAddr)) != bufferLen) {
		throw SocketException("Send failed (sendto())", true);
	}
}

int UDPSocket::recvFrom(void *buffer, int bufferLen, string &sourceAddress,
	unsigned short &sourcePort) throw(SocketException) {
	sockaddr_in clntAddr;
	socklen_t addrLen = sizeof(clntAddr);
	int rtn;
	// if (true) receives message and stores it to buffer
	if ((rtn = recvfrom(sockDesc, (raw_type *)buffer, bufferLen, 0,
		(sockaddr *)&clntAddr, (socklen_t *)&addrLen)) < 0) {
		throw SocketException("Receive failed (recvfrom())", true);
	}
	sourceAddress = inet_ntoa(clntAddr.sin_addr);	// Get IPv4 address and append it to string format
	sourcePort = ntohs(clntAddr.sin_port);

	return rtn;
}

void UDPSocket::setMulticastTTL(unsigned char multicastTTL) throw(SocketException) {
	if (setsockopt(sockDesc, IPPROTO_IP, IP_MULTICAST_TTL,
		(raw_type *)&multicastTTL, sizeof(multicastTTL)) < 0) {
		throw SocketException("Multicast TTL set failed (setsockopt())", true);
	}
}

void UDPSocket::joinGroup(const string &multicastGroup) throw(SocketException) {
	struct ip_mreq multicastRequest;

	multicastRequest.imr_multiaddr.s_addr = inet_addr(multicastGroup.c_str());
	multicastRequest.imr_interface.s_addr = htonl(INADDR_ANY);
	if (setsockopt(sockDesc, IPPROTO_IP, IP_ADD_MEMBERSHIP,
		(raw_type *)&multicastRequest,
		sizeof(multicastRequest)) < 0) {
		throw SocketException("Multicast group join failed (setsockopt())", true);
	}
}

void UDPSocket::leaveGroup(const string &multicastGroup) throw(SocketException) {
	struct ip_mreq multicastRequest;

	multicastRequest.imr_multiaddr.s_addr = inet_addr(multicastGroup.c_str());
	multicastRequest.imr_interface.s_addr = htonl(INADDR_ANY);
	if (setsockopt(sockDesc, IPPROTO_IP, IP_DROP_MEMBERSHIP,
		(raw_type *)&multicastRequest,
		sizeof(multicastRequest)) < 0) {
		throw SocketException("Multicast group leave failed (setsockopt())", true);
	}
}

/**
*	Request types are explained below:
*	1 -> "JOIN" type request, to handle this we need to create an object for PlayerInformation class
*	2 -> "SAY" type request, to handle this we need to return the message contained in the packet to clients
*	in the format of "SAID:[playerId], [message]
*	3 -> "PING" request check whether the players are still connected to server or not with certain time intervals
*	4 -> "LEAVE/DELETE" type request, we need to delete the object with corresponding playerId
*/
int UDPSocket::getRequestType(char* buffer, const string &sourceAddress, const unsigned short &sourcePort, vector<PlayerInformation*>& players) {
	const char* requestTypeJoin = "JOIN";
	const char* requestTypeSayy = "SAYY";
	const char* requestTypePing = "PING";
	const char* requestTypePong = "PONG";
	const char* requestTypeDrop = "DROP";
	const char* requestTypeMove = "MOVE";



	//char *message = new char[256];
	//strcpy(message, buffer);
	//message = strtok(message,";");
	//cout << message << endl;

	char *token = buffer;
	//strcpy(token, buffer);	
	token = strtok(token, ";");
	//cout << token << endl;

	token = strtok(token, ":");
	//cout << token << endl;
	int requestType;

	// If JOIN request has come
	if (strcmp(token, requestTypeJoin) == 0) {
		token = strtok(NULL, ":");

		if (handleRequestTypeJoin(token, sourceAddress, sourcePort, players)) {
			// Succesfully created an onject of PlayerInformation
			requestType = 1;
		}
		else {
			// Failed to create a PlayerInformation object
			requestType = -3;
		}

		//cout << token << endl;

	}
	// If SAY request has come
	else if (strcmp(token, requestTypeSayy) == 0) {
		token = strtok(NULL, ":");
		requestType = handleRequestTypeSayy(token, sourceAddress, sourcePort, players);
	}
	else if (strcmp(token, requestTypePing) == 0) {
		requestType = handleRequestTypePing(token, sourceAddress, sourcePort, players);
	}
	else if (strcmp(token, requestTypePong) == 0) {

		token = strtok(NULL, ":");
		requestType = handleRequestTypePong(token, sourceAddress, sourcePort, players);


		// Work this area

		/*

		if (players.size() > 0) {
			int playerIndexFromVector;
			for (playerIndexFromVector = 0; playerIndexFromVector < players.size(); playerIndexFromVector++) {
				players[playerIndexFromVector]->setIsStillConnected(true);
			}
		}
		else {
			requestType = -3;
		}*/

	}
	//cout << "Before delete" << endl;
	//delete [] message;
	//cout << "After delete 1" << endl;

	//delete [] token;
	//cout << "After delete 2" << endl;

	// MOVE:PlayerID,posx,posy;
	else if (strcmp(token, requestTypeMove) == 0) {
		token = strtok(NULL, ":");
		requestType = handleRequestTypeMove(token, sourceAddress, sourcePort, players);
	}


	return requestType;
}

bool UDPSocket::handleRequestTypeJoin(char* buffer, const string &sourceAddress, const unsigned short &sourcePort, vector<PlayerInformation*>& players) {

	PlayerInformation *newPlayer;
	newPlayer = new PlayerInformation(sourceAddress, sourcePort, atoi(buffer));
	players.push_back(newPlayer);

	if (players.back()->getPlayerIdByAdress(sourceAddress, sourcePort) != atoi(buffer)) {
		return false;
	}

	return true;
}


// Should also take playerID as reference in case of players are joining from same ip
int UDPSocket::handleRequestTypeSayy(char* buffer, const string &sourceAddress, const unsigned short &sourcePort, vector<PlayerInformation*>& players) {
	if (players.size() > 0) {
		char replyToPlayer[256] = {};
		strcpy(replyToPlayer, "SAID:");

		int playerIndexFromVector = 0;
		while (playerIndexFromVector < players.size() && players[playerIndexFromVector]->getPlayerIdByAdress(sourceAddress, sourcePort) == -1) {
			++playerIndexFromVector;
		}

		if (playerIndexFromVector >= players.size())
		{
			return -2;

		}
		else {

			int playerId = players[playerIndexFromVector]->getPlayerIdByAdress(sourceAddress, sourcePort);

			string s = to_string(playerId);
			vector<char> v(s.begin(), s.end());
			v.push_back('\0'); // Make sure we are null-terminated
			char* c = &v[0];

			strcat(replyToPlayer, c);
			strcat(replyToPlayer, ", ");
			strcat(replyToPlayer, buffer);
			strcat(replyToPlayer, ";");

			int sizeOfMessage = (strlen(replyToPlayer) * sizeof(char));
			cout << replyToPlayer << endl;
			sendTo(replyToPlayer, sizeOfMessage, sourceAddress, sourcePort);
			return 2;
		}
	}
	else {
		return -1;
	}
}

int UDPSocket::handleRequestTypePing(char* buffer, const string &sourceAddress, const unsigned short &sourcePort, vector<PlayerInformation*>& players) {
	if (players.size() > 0) {
		int playerIndexFromVector;
		char replyToPlayer[256] = {};
		for (playerIndexFromVector = 0; playerIndexFromVector < players.size(); playerIndexFromVector++) {
			strcpy(replyToPlayer, "PING");
			strcat(replyToPlayer, ";");

			int sizeOfMessage = (strlen(replyToPlayer) * sizeof(char));
			sendTo(replyToPlayer, sizeOfMessage, players[playerIndexFromVector]->getPlayerSourceAddress(), players[playerIndexFromVector]->getPlayerSourcePort());
			players[playerIndexFromVector]->setIsStillConnected(false);
		}
		return 3;
	}
	else {
		return -1;
	}
}

int UDPSocket::handleRequestTypePong(char* buffer, const string &sourceAddress, const unsigned short &sourcePort, vector<PlayerInformation*>& players) {
	if (players.size() > 0) {
		int playerIndexFromVector = 0;

		while (players.at(playerIndexFromVector)->getPlayerIdByAdress(sourceAddress, sourcePort) != atoi(buffer)) {
			++playerIndexFromVector;
		}

		if (playerIndexFromVector >= players.size()) {
			return -3;
		}
		players[playerIndexFromVector]->setIsStillConnected(true);

		return 4;
	}
	else {
		return -1;
	}
}

// MOVD:PlayerID,posx,posy;
int UDPSocket::handleRequestTypeMove(char* buffer, const string &sourceAddress, const unsigned short &sourcePort, vector<PlayerInformation*>& players) {
	char replyToPlayer[256] = {};
	strcpy(replyToPlayer, "MOVD:");

	bool isMovementSuccesful = false;

	buffer = strtok(buffer, ",");
	int playerIdFromBuffer = atoi(buffer);

	buffer = strtok(NULL, ",");
	//float playerPosXFromBuffer = ((int)(atof(buffer)*100.0 + 0.5F)) / 100.0F;
	float playerPosXFromBuffer = atof(buffer);
	buffer = strtok(NULL, ",");
	//float playerPosYFromBuffer = ((int)(atof(buffer)*100.0 + 0.5F)) / 100.0F;
	float playerPosYFromBuffer = atof(buffer);
	int playerIndexFromVector = 0;
	while (playerIndexFromVector < players.size() && players[playerIndexFromVector]->getPlayerIdByAdress(sourceAddress, sourcePort) == -1 && players[playerIndexFromVector]->getPlayerIdByAdress(sourceAddress, sourcePort) == playerIdFromBuffer) {
		++playerIndexFromVector;
	}

	if (playerIndexFromVector >= players.size())
	{
		return -2;
	}
	cout << "PlayerPosX before Update: " << players[playerIndexFromVector]->getPlayerPosX() << endl;
	cout << "PlayerPosY before Update: " << players[playerIndexFromVector]->getPlayerPosY() << endl;

	cout << "Time Before :" << players[playerIndexFromVector]->getSecondsTillLastMovement().seconds_elapsed() << endl;
	float maximumPossibleMovement = (players[playerIndexFromVector]->getPlayerMovementSpeed() * players[playerIndexFromVector]->getSecondsTillLastMovement().seconds_elapsed());
	players[playerIndexFromVector]->getSecondsTillLastMovement().reset();
	//cout << "Maximum possible movement value: " << maximumPossibleMovement << endl;
	cout << "Time After :" << players[playerIndexFromVector]->getSecondsTillLastMovement().seconds_elapsed() << endl;

	float currentMovement = (fabs(players[playerIndexFromVector]->getPlayerPosX() - playerPosXFromBuffer) * fabs(players[playerIndexFromVector]->getPlayerPosY() - playerPosYFromBuffer));
	//cout << "Current movement value: " << currentMovement << endl;

	players[playerIndexFromVector]->setPlayerPosX(playerPosXFromBuffer);
	players[playerIndexFromVector]->setPlayerPosY(playerPosYFromBuffer);
	isMovementSuccesful = true;
	/*if (maximumPossibleMovement >= currentMovement) {
		players[playerIndexFromVector]->setPlayerPosX(playerPosXFromBuffer);
		players[playerIndexFromVector]->setPlayerPosY(playerPosYFromBuffer);
		isMovementSuccesful = true;
	}*/

	string s = to_string(playerIdFromBuffer);
	//cout << "PlayerId (String): " << s << endl;
	vector<char> v(s.begin(), s.end());
	v.push_back('\0'); // Make sure we are null-terminated
	char* c = &v[0];

	strcat(replyToPlayer, c);
	strcat(replyToPlayer, ",");
	v.clear();


	//s = to_string(((int)(players[playerIndexFromVector]->getPlayerPosX()*100.0 + 0.5F)) / 100.0F);
	s = to_string(players[playerIndexFromVector]->getPlayerPosX());
	//cout << "playerPosX (String): " << s << endl;

	vector<char> x(s.begin(), s.end());
	x.push_back('\0'); // Make sure we are null-terminated

	/*
	copy(s.begin(), s.end(), std::back_inserter(v));
	v.push_back('\0'); // Make sure we are null-terminated
	*/
	c = &x[0];
	//cout << "PlayerPosX after Update: " << c << endl;

	strcat(replyToPlayer, c);
	strcat(replyToPlayer, ",");
	x.clear();


	//s = to_string(((int)(players[playerIndexFromVector]->getPlayerPosY()*100.0 + 0.5F)) / 100.0F);
	s = to_string(players[playerIndexFromVector]->getPlayerPosY());
	//cout << "playerPosX (String): " << s << endl;

	vector<char> z(s.begin(), s.end());
	z.push_back('\0'); // Make sure we are null-terminated
	/*
	copy(s.begin(), s.end(), std::back_inserter(v));
	v.push_back('\0'); // Make sure we are null-terminated
	*/
	c = &z[0];

	//cout << "PlayerPosY after Update: " << c << endl;


	strcat(replyToPlayer, c);
	strcat(replyToPlayer, ";");
	z.clear();


	int sizeOfMessage = (strlen(replyToPlayer) * sizeof(char));
	cout << replyToPlayer << endl;

	sendTo(replyToPlayer, sizeOfMessage, sourceAddress, sourcePort);


	if (isMovementSuccesful) {
		return 5;
	}
	else {
		return -4;
	}
}

// Saniyede constant olarak 64 time frame at
// Tick sayisini float tut
// Players must see each others
// her bir tick'te ping gönder, (saniyede bir falan)