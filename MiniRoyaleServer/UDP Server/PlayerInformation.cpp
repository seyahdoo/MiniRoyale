#include "PlayerInformation.h"

PlayerInformation::PlayerInformation(const string &sourceAddress, const unsigned short &sourcePort, const int &playerId){
	this->sourceAddress = sourceAddress;
	this->sourcePort = sourcePort;
	this->playerId = playerId;
	std::cout << "Succesfully created player/client with id: " <<  playerId << ". With the address of: " << sourceAddress << ":" << sourcePort << endl;
}
PlayerInformation::~PlayerInformation(){
	std::cout << "Succesfully terminated player/client with id: " <<  playerId << ". With the address of: " << sourceAddress << ":" << sourcePort << endl;
}
const int PlayerInformation::getPlayerIdByAdress(const string &sourceAddress, const unsigned short &sourcePort) const{
	if(this->sourceAddress == sourceAddress && this->sourcePort == sourcePort){
		return playerId;
	}
	else{
		return -1;
	}
}
const string PlayerInformation::getPlayerSourceAddress() const{
	return sourceAddress;
}
const unsigned short PlayerInformation::getPlayerSourcePort() const{
	return sourcePort;
}