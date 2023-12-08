from AdventOfCode.AoCLib import AoCLibChallenge

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        self.data = []

        for line in self.inData:
            x, y = line.split()
            self.data.append((x, *self.getType(x), int(y)))

    def getType(self, cards):
        saved_cards = {}
        processed = 0
        score = 0
        scorelookup = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, 'T': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12}

        for card in cards:
            if card in saved_cards:
                saved_cards[card] += 1
            else:
                saved_cards[card] = 1
            processed += 1

            score = score << 4
            score += scorelookup[card]

        return self.classify(saved_cards, score)

    def classify(self, saved_cards, score):
        if len(saved_cards) == 1:
            return "five_of_a_kind", 0x700000 + score

        fourpair  = sum(saved_cards[x] == 4 for x in saved_cards.keys()) == 1

        if fourpair:
            return "four_of_a_kind", 0x600000 + score
            
        threepair = sum(saved_cards[x] == 3 for x in saved_cards.keys()) == 1
        twopair   = sum(saved_cards[x] == 2 for x in saved_cards.keys())

        if threepair and twopair:
            return "full_house", 0x500000 + score

        if threepair:
            return "three_of_a_kind", 0x400000 + score
        if twopair == 2:
            return "two_pair", 0x300000 + score

        if twopair == 1:
            return "one_pair", 0x200000 + score

        if len(saved_cards) == 5:
            return "high_card", 0x100000 + score

    def run(self):
        print(self.data)
        self.data = sorted(self.data, key=lambda line: line[2])
        
        for game, gtype, score, bid in self.data:
            print(f"{game}\t{gtype}\t{score:x}\t{bid}")

        value = 0

        for rank in range(len(self.data)):
            game, gtype, score, bid = self.data[rank]

            value += (rank + 1) * bid

        print(f"Score: {value}")

class Challenge2(Challenge1):
    ChallengeNr = 2

    def getType(self, cards):
        saved_cards = {}
        processed = 0
        score = 0
        scorelookup = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, 'T': 9, 'J': 0, 'Q': 10, 'K': 11, 'A': 12}
        jokers = 0

        for card in cards:
            if card == 'J':
                jokers += 1

            if card in saved_cards:
                saved_cards[card] += 1
            else:
                saved_cards[card] = 1
            processed += 1

            score = score << 4
            score += scorelookup[card]

        print(f"Found {jokers} jokers in {cards}")

        if jokers == 0:
            return self.classify(saved_cards, score)

        fourpair  = sum(saved_cards[x] == 4 for x in saved_cards.keys()) == 1
        threepair = sum(saved_cards[x] == 3 for x in saved_cards.keys()) == 1
        twopair   = sum(saved_cards[x] == 2 for x in saved_cards.keys())
        singles   = sum(saved_cards[x] == 1 for x in saved_cards.keys())


        if jokers == 1:
            if fourpair:
                return "five_of_a_kind", 0x700000 + score
            elif threepair:
                return "four_of_a_kind", 0x600000 + score
            elif twopair == 2:
                return "full_house", 0x500000 + score
            elif twopair:
                return "three_of_a_kind", 0x400000 + score
            elif singles == 5:
                return "one_pair", 0x200000 + score
        elif jokers == 2:
            if threepair:
                return "five_of_a_kind", 0x700000 + score
            elif twopair == 2: # joker is also a pair
                return "four_of_a_kind", 0x600000 + score
            elif singles == 3: # joker is a pair
                return "three_of_a_kind", 0x400000 + score
        elif jokers == 3:
            if twopair and threepair: # joker is a threepair
                return "five_of_a_kind", 0x700000 + score
            elif singles == 2:
                return "four_of_a_kind", 0x600000 + score

        return "five_of_a_kind", 0x700000 + score

    def run(self):
        super().run()
