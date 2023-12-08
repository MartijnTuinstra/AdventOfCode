from AdventOfCode.AoCLib import AoCLibChallenge

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        data = []
        for line in self.inData:
            card, numbers = line.split(": ")
            numbers1, numbers2 = numbers.split(" | ")
            numbers1 = [int(x) for x in numbers1.split()]
            numbers2 = [int(x) for x in numbers2.split()]

            data.append((int(card.split(" ")[-1]), numbers1, numbers2))

        self.inData = data

    def run(self):
        total = 0
        
        for card, winning, numbers in self.inData:
            value = 1

            for n in numbers:
                if n in winning:
                    value *= 2

            total += value // 2

        print(f"Total card value: {total}")

class Challenge2(Challenge1):
    ChallengeNr = 2

    def setup(self):
        super().setup()

    def run(self):
        cardcount = {}

        for card, winning, numbers in self.inData:
            if card in cardcount:
                cardcount[card] += 1
            else:
                cardcount[card] = 1
            i = 1

            for n in numbers:
                if n in winning:
                    if card+i in cardcount:
                        cardcount[card+i] += cardcount[card]
                    else:
                        cardcount[card+i] = cardcount[card]
                    i += 1

        print(f"Total number of cards: {sum(cardcount.values())}")
