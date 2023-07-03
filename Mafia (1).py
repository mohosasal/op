class MafiaGame:
    def __init__(self):
        self.GameRunning = False
        self.Players = {}

    def GetWinner(self):
        mafiaCount, citizenCount = 0, 0
        for rule in self.Players.values():
            if isinstance(rule, Mafia) and rule.Alive: mafiaCount += 1
            if isinstance(rule, Citizen) and rule.Alive: citizenCount += 1

        if mafiaCount == citizenCount:
            self.GameRunning = False
            return 'mafia'
        if mafiaCount == 0:
            self.GameRunning = False
            return 'citizens'
        
        return None
    
    def GetRuleInstance(self, name):
        for rule in self.Players.values():
            if rule.__class__.__name__ == name:
                return rule

    def isAlive(self, name):
        for rule in self.Players.values():
            if rule.__class__.__name__ == name:
                return rule.Alive
    
    def CountAlives(self):
        alives = 0
        for rule in self.Players.values():
            if rule.Alive: alives += 1
        return alives

    def CreateInstance(self, ruleName : str):
        if ruleName == 'simplecitizen':
            return SimpleCitizen(self)
        if ruleName == 'sniper':
            return Sniper(self)
        if ruleName == 'natasha':
            return Natasha(self)
        if ruleName == 'doctor':
            return Doctor(self)
        if ruleName == 'simplemafia':
            return SimpleMafia(self)
        if ruleName == 'godfather' or ruleName == 'gadfather':
            return Gadfather(self)
        if ruleName == 'detective':
            return Detective(self)

    def CreateNewGame(self, playerMap : str):
        self.GameRunning = True
        pmap = playerMap.replace(':', ' ').split()

        for i in range(0, len(pmap), 2):
            self.Players[pmap[i]] = self.CreateInstance(pmap[i + 1])
        
        return 'new game started successfully!'
    
    def AddPlayer(self, playerName):
        if playerName in self.Players.keys():
            return 'player with this name already exists'
        else:
            self.Players[playerName] = None
            return 'new player created successfully!'
        
    def LaunchVote(self, votes : str):
        vmap = votes.replace(':', '').split()
        vmap = vmap[1::2]
        votesCount = [(x, vmap.count(x)) for x in set(vmap)]
        maxVote = max(votesCount, key=lambda itm: itm[1])
        if maxVote[1] >= self.CountAlives() // 2:
            self.Players[maxVote[0]].Alive = False
            return f'player {maxVote[0]} killed by election'
        else:
            return 'No players were killed at this election' 
        
    
    


class Mafia:
    def __init__(self, game : MafiaGame):
        self.Alive = True
        self.Muted = False
        self.Guard = False
        self.Game = game

class Gadfather(Mafia):
    def __init__(self, game : MafiaGame):
        super().__init__(game)
        self.FirstRuleRequest = True
    
    def Kill(self, playerName):
        if self.Alive:
            self.Game.Players[playerName].Alive = False
            return 'Gadfather: Done!'
        else:
            return 'Gadfather: Gadfather were killed before.'

class Natasha(Mafia):
    def __init__(self, game : MafiaGame):
        super().__init__(game)
    def Mute(self, playerName):
        if self.Alive:
            self.Game.Players[playerName].Muted = True
            return 'Natasha: Done!'
        else:
            return 'Natasha: Natasha were killed before.'


class SimpleMafia(Mafia):
    def __init__(self, game : MafiaGame):
        super().__init__(game)
    def Kill(self, playerName):
        if self.Game.isAlive('Gadfather'):
            return 'Mafia: Gadfather is alive'
        else:
            self.Game.Players[playerName].Alive = False
            return 'Mafia: Done!'



class Citizen:
    def __init__(self, game : MafiaGame):
        self.Alive = True
        self.Muted = False
        self.Guard = False
        self.Game = game

class SimpleCitizen(Citizen):
    def __init__(self, game : MafiaGame):
        super().__init__(game)

class Doctor(Citizen):
    def __init__(self, game : MafiaGame):
        super().__init__(game)
    def Revive(self, playerName):
        if self.Alive:
            self.Game.Players[playerName].Alive = True
            self.Game.Players[playerName].Guard = True
            return 'Doctor: Done!'
        else:
            return 'Doctor: Doctor were killed before.'

class Detective(Citizen):
    def __init__(self, game : MafiaGame):
        super().__init__(game)
    def RequestRule(self, playerName):
        if self.Alive:
            rule = self.Game.Players[playerName]
            if isinstance(rule, Mafia) : return 'Mafia'
            if isinstance(rule, Citizen): return 'Citizen'
            return 'Negative'

class Sniper(Citizen):
    def __init__(self, game : MafiaGame):
        super().__init__(game)
        self.Bullets = 2
    
    def Kill(self, playerName):
        if self.Bullets == 0:
            return 'Sniper: The sniper has run out of bullets.'
        if self.Alive:
            if self.Game.Players[playerName].Guard == False:
                self.Game.Players[playerName].Alive = False
                return 'Sniper: Done!'
        else:
            return 'Sniper: Sniper were killed before.'


game = MafiaGame()

while True:
    command = input().lower()
    if command == 'exit': break

    cmd = command.split()

    if cmd[0] == 'new_player':
        name = cmd[1]
        result = game.AddPlayer(name)
        print(result)
    
    elif cmd[0] == 'new_game':
        command = command.replace('new_game ', '')
        result = game.CreateNewGame(command)
        print(result)

    elif cmd[0] == 'vote:':
        command = command.replace('vote: ', '')
        result = game.LaunchVote(command)
        print(result)

    elif cmd[0] == 'gadfather:' and cmd[1] == 'kill':
        player = game.GetRuleInstance('Gadfather')
        player.Kill(cmd[2])

    elif cmd[0] == 'mafia:' and cmd[1] == 'kill':
        player = game.GetRuleInstance('SimpleMafia')
        player.Kill(cmd[2])
        
    elif cmd[0] == 'natasha:' and cmd[1] == 'get':
        player = game.GetRuleInstance('Natasha')
        player.Mute(cmd[2])

    elif cmd[0] == 'doctor:' and cmd[1] == 'make':
        player = game.GetRuleInstance('Doctor')
        player.Revive(cmd[2])

    elif cmd[0] == 'detective:' and cmd[1] == 'tell':
        player = game.GetRuleInstance('Detective')
        player.RequestRule(cmd[2])
        pass

    elif cmd[0] == 'sniper:' and cmd[1] == 'kill':
        player = game.GetRuleInstance('Sniper')
        player.Kill(cmd[2])

    elif cmd[0] == 'sniper:' and cmd[1] == 'kill':
        pass

    else:
        print('invalid command')

    if game.GameRunning and game.GetWinner() != None:
        print(f'The {game.GetWinner()} team won the game')