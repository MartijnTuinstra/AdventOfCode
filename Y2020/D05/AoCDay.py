from AdventOfCode.AoCLib import AoCLibChallenge

import re

def toBin(s, key):
    value = 0

    for letter in s:
        if letter == key:
            value = value | 1

        value = value << 1

    return value >> 1

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        self.passes = self.inData

    def seatID(self, seat):
        row = toBin(seat[:7], 'B')
        column = toBin(seat[-3:], 'R')

        id = row*8 + column

        print(f"{seat}: row {row}, column {column}, id {id}")

        return id

    def run(self):
        maxId = 0
        for seat in self.passes:
            maxId = max(maxId, self.seatID(seat))

        print(f"maxID: {maxId}")

        return maxId

class Challenge2(Challenge1):
    ChallengeNr = 2

    def run(self):
        maxId = super().run()

        seatList = [0 for i in range(maxId+1)]

        for seat in self.passes:
            seatList[self.seatID(seat)] = 1

        
        for i in range(len(seatList)):
            if seatList[i] == 1:
                continue
            print(f"Seat {i:3d} empty")
