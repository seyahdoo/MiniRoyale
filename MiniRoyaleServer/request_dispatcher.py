

def RequestDispatcher(buffer):
    print("UDP: received:"+text)
        
    commands = text.split(';')
      
    for cmd in commands:
        if(cmd[0:5] == "MOVER"):
            args = cmd[6:]
            args = args.split(',')
            #print(str(args))
            # if last packet number is > args[0] return
            self.player.Move(args[1],args[2])
            
        if(cmd[0:5] == "PONGO"):
            
            