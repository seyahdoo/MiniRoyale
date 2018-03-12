#include "PlayerInformation.h"

PlayerInformation::PlayerInformation(const string &sourceAddress, const unsigned short &sourcePort, const int &playerId){
	this->sourceAddress = sourceAddress;
	this->sourcePort = sourcePort;
	this->playerId = playerId;
	this->isStillConnected = 1;
	this->playerPosX = 0;
	this->playerPosY = 0;
	this->playerMovementSpeed = 5000;
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
	return this->sourceAddress;
}
const unsigned short PlayerInformation::getPlayerSourcePort() const{
	return this->sourcePort;
}
void PlayerInformation::setIsStillConnected(bool isStillConnected){
	this->isStillConnected = isStillConnected;
}
bool PlayerInformation::getIsStillConnected() const{
	return this->isStillConnected;
}
const float PlayerInformation::getPlayerPosX() const {
	return this->playerPosX;
}
const float PlayerInformation::getPlayerPosY() const {
	return this->playerPosY;
}
void PlayerInformation::setPlayerPosX(float playerPosX) {
	this->playerPosX = playerPosX;
}
void PlayerInformation::setPlayerPosY(float playerPosY) {
	this->playerPosY = playerPosY;
}
const float PlayerInformation::getPlayerMovementSpeed() const {
	return this->playerMovementSpeed;
}
void PlayerInformation::setPlayerMovementSpeed(float playerMovementSpeed) {
	this->playerMovementSpeed = playerMovementSpeed;
}
Timer& PlayerInformation::getSecondsTillLastMovement() {
	return this->secondsTillLastMovement;
}