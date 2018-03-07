#ifndef __PLAYERINFORMATION_INCLUDED__
#define __PLAYERINFORMATION_INCLUDED__

#include <vector>
#include <iostream>
using namespace std;

class PlayerInformation{
public:
	PlayerInformation(const string &sourceAddress, const unsigned short &sourcePort, const int &playerId);
	~PlayerInformation();
	const int getPlayerIdByAdress(const string &sourceAddress, const unsigned short &sourcePort) const;
	const string getPlayerSourceAddress() const;
	const unsigned short getPlayerSourcePort() const;

private:
	string sourceAddress;             // Address of datagram source
    unsigned short sourcePort;        // Port of datagram source
	int playerId;					  // Unique ID of a player/client
};

#endif




//////////	sourceAddress bilgisini Stringe cevirmeye calis