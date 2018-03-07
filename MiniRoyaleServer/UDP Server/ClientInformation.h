#ifndef __PLAYERINFORMATION_INCLUDED__
#define __PLAYERINFORMATION_INCLUDED__

class PlayerInformation{
public:
	PlayerInformation(const string &sourceAddress, const unsigned short &sourcePort, const int &playerId) throw();
	~PlayerInformation() throw();
	const int getPlayerId() const;
	const string getPlayerSourceAddress() const;
	const unsigned short getSourcePort() const;

private:
	string sourceAddress;             // Address of datagram source
    unsigned short sourcePort;        // Port of datagram source
	int playerId;					  // Unique ID of a player/client
};

#endif