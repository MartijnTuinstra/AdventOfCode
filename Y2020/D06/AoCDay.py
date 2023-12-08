from AdventOfCode.AoCLib import AoCLibChallenge
import operator
from functools import reduce

def letterToBin(letter):
    return 1 << (ord(letter) - ord('a'))

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        self.data = []
        tmp = []

        for line in self.inData:
            if line == "":
                self.data.append(tmp)
                tmp = []
                continue

            tmp.append(line)

        self.data.append(tmp)

    def run(self):
        maxId = 0
        groupdata = []
        for group in self.data:
            question = 0
            for person in group:
                question = question | reduce(operator.ior, [letterToBin(x) for x in person])
            groupdata.append(question.bit_count())

        print(f"Count qeustions: {sum(groupdata)}")

        return maxId

class Challenge2(Challenge1):
    ChallengeNr = 2

    def run(self):
        maxId = 0
        groupdata = []
        for group in self.data:
            question = 0xFFFFFFFF
            for person in group:
                question = question & reduce(operator.ior, [letterToBin(x) for x in person])
            groupdata.append(question.bit_count())

        print(f"Count qeustions: {sum(groupdata)}")

        return maxId
