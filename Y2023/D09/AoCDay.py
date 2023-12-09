from AdventOfCode.AoCLib import AoCLibChallenge

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        self.values = [[int(y) for y in x.split()] for x in self.inData]

    def predictNext(self, l):
        if sum([x == 0 for x in l]) == len(l):
            return 0

        newl = [l[x+1] - l[x] for x in range(len(l)-1)]
        return l[-1] + self.predictNext(newl)

    def run(self):
        s = 0
        for value in self.values:
            s += self.predictNext(value)

        print(f"Value: {s}")

class Challenge2(Challenge1):
    ChallengeNr = 2

    def predictPrev(self, l):
        if sum([x == 0 for x in l]) == len(l):
            return 0

        newl = [l[x+1] - l[x] for x in range(len(l)-1)]
        return l[0] - self.predictPrev(newl)

    def run(self):
        s = 0
        for value in self.values:
            s += self.predictPrev(value)

        print(f"Value: {s}")

