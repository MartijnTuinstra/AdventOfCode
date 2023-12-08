from AdventOfCode.AoCLib import AoCLibChallenge

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        player = 0

        deck = [[], []]

        for line in self.inData:
            if line.startswith("Player"):
                continue
            elif line == '':
                player += 1
                continue
            deck[player].append(int(line))

        self.decks = deck

    def score(self):
        deck = []
        if len(self.decks[0]) == 0:
            deck = self.decks[1]
        else:
            deck = self.decks[0]

        length = len(deck)
        s = 0
        for i in range(length):
            s += deck[i] * (length - i)

        return s

    def run(self):
        self.decks = self.playGame(self.decks)

        print(f"Game score {self.score()}")

    def playGame(self, deck):
        gamelooplist = []
        
        while len(deck[0]) and len(deck[1]):
            
            p1 = deck[0].pop(0)
            p2 = deck[1].pop(0)

            if p1 > p2:
                deck[0].append(max(p1, p2))
                deck[0].append(min(p1, p2))
            else:
                deck[1].append(max(p1, p2))
                deck[1].append(min(p1, p2))

        return deck


class Challenge2(Challenge1):
    ChallengeNr = 2

    def setup(self):
        v = super().setup()
        self.maxCardValue = max([max(self.decks[0]), max(self.decks[1])])
        return v

    def gameId(self, deck):
        v = 0
        for k in deck[0]:
            v += k-1
            v *= self.maxCardValue

        for k in deck[1]:
            v += k-1
            v *= self.maxCardValue

        return v // self.maxCardValue

    def playGame(self, deck):
        gamelooplist = []
        
        while len(deck[0]) and len(deck[1]):

            gameID = self.gameId(deck)

            if gameID in gamelooplist:
                return [[None], []]
            
            gamelooplist.append(gameID)
            
            p1 = deck[0].pop(0)
            p2 = deck[1].pop(0)

            if p1 <= len(deck[0]) and  p2 <= len(deck[1]):
                subgamedeck = self.playGame([deck[0][:p1], deck[1][:p2]])
            
                if len(subgamedeck[1]) == 0:
                    deck[0].append(p1)
                    deck[0].append(p2)
                else:
                    deck[1].append(p2)
                    deck[1].append(p1)
            

            elif p1 > p2:
                deck[0].append(max(p1, p2))
                deck[0].append(min(p1, p2))
            else:
                deck[1].append(max(p1, p2))
                deck[1].append(min(p1, p2))

        return deck

"""
lvl = 1
gameNr = 0

def game(d):    
    global lvl, gameNr
    #AoCprint(f"recursive Combat {lvl} | {str(d)}")
    gids = []
    round = 1
    gameNr += 1
    AoCprint(f"=== Game {gameNr} ===")
    localGameNr = gameNr

    while (len(d[0]) and len(d[1])):
        AoCprint(f"-- Round {round} (Game {localGameNr}) --")
        round += 1
        gid = gameId(d)

        if gid in gids:
            AoCprint(f"Game loop detected {lvl}")
            return 1
            break
        gids.append(gid)

        AoCprint(f"Player 1's deck: {', '.join(str(x) for x in d[0])}")
        AoCprint(f"Player 2's deck: {', '.join(str(x) for x in d[1])}")

        p1 = d[0].pop(0)
        p2 = d[1].pop(0)
        
        AoCprint(f"Player 1 plays : {p1}")
        AoCprint(f"Player 2 playsf: {p2}")

        #AoCprint(f"P1: {p1}\tP2: {p2}")

        if p1 <= len(d[0]) and  p2 <= len(d[1]):
            lvl += 1
            rG = game([d[0][:p1], d[1][:p2]])
            
            AoCprint(f"...anyway, back to game {localGameNr}.\nPlayer {rG} wins round {round-1} of game {localGameNr}!")

            if rG == 1:
                d[0].append(p1)
                d[0].append(p2)
            else:
                d[1].append(p2)
                d[1].append(p1)
            

        elif p1 > p2:
            d[0].append(max(p1, p2))
            d[0].append(min(p1, p2))
            AoCprint(f"Player 1 wins round {round-1} of game {localGameNr}!")
        else:
            d[1].append(max(p1, p2))
            d[1].append(min(p1, p2))
            AoCprint(f"Player 2 wins round {round-1} of game {localGameNr}!")
    

    AoCprint(f"The winner of game {localGameNr} is player {2 if len(d[0]) == 0 else 1}!")
    return 2 if len(d[0]) == 0 else 1

game(decks)

def score(deck):
    length = len(deck)
    s = 0
    for i in range(length):
        s += deck[i] * (length - i)

    return s

AoCprint("== Post-game results ==")
AoCprint(f"Player 1's deck: {decks[0]}")
AoCprint(f"Player 2's deck: 7, 2, 5, 2, 1, 1, 10, 8, 9, 3")

if len(decks[0]):
    print(f"score: {score(decks[0])}")
else:
    print(f"score: {score(decks[1])}")
AoCprint(str(decks))

# checkTest(False)

"""
