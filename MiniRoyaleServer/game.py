
import threading



class Game():
    
    def __init__(self):
        print("initiating game")
        
        self.tickrate = 16
        
        self.players_lock = threading.Lock()
        self.players = {}
        
        self.props = {}
        
        self.bullets = {}
        
        print("initiated game")
        
        


def GameStart():
    global game_instance
    game_instance = Game()
    

game_instance = None

