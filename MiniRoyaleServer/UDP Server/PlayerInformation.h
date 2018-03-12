#ifndef __PLAYERINFORMATION_INCLUDED__
#define __PLAYERINFORMATION_INCLUDED__

#include <vector>
#include "Timer.h"
#include <iostream>
using namespace std;

class PlayerInformation{
public:
	PlayerInformation(const string &sourceAddress, const unsigned short &sourcePort, const int &playerId);
	~PlayerInformation();
	const int getPlayerIdByAdress(const string &sourceAddress, const unsigned short &sourcePort) const;
	const string getPlayerSourceAddress() const;
	const unsigned short getPlayerSourcePort() const;
	void setIsStillConnected(bool isStillConnected);
	bool getIsStillConnected() const;
	const float getPlayerPosX() const;
	const float getPlayerPosY() const;
	void setPlayerPosX(float playerPosX);
	void setPlayerPosY(float playerPosY);
	const float getPlayerMovementSpeed() const;
	void setPlayerMovementSpeed(float playerMovementSpeed);
	Timer& getSecondsTillLastMovement();
private:
	float playerPosX, playerPosY;
	float playerMovementSpeed;
	string sourceAddress;             // Address of datagram source
    unsigned short sourcePort;        // Port of datagram source
	int playerId;					  // Unique ID of a player/client
	bool isStillConnected;
	Timer secondsTillLastMovement;
};

#endif
