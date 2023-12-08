from AdventOfCode.AoCLib import AoCLibChallenge

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        self.inDataTo2D()

    def findandpurge(self, numbers, newloc):

        if newloc in numbers:
            del numbers[newloc]

            numbers = self.findandpurge(numbers, (newloc[0]-1, newloc[1]))
            numbers = self.findandpurge(numbers, (newloc[0]+1, newloc[1]))

        return numbers

    def getNumberFromLocation(self, numberlist, loc):
        if loc not in numberlist:
            return None

        print(f"Searching for number {loc}")
        number = [numberlist[loc]]
        del numberlist[loc]

        locations = [(loc[0]-1, loc[1]), (loc[0]+1, loc[1])]

        while len(locations):
            newloc = locations.pop(0)

            if newloc in numberlist:
                locations.extend([(newloc[0]-1, newloc[1]), (newloc[0]+1, newloc[1])])

                if newloc[0] < loc[0]:
                    number = [numberlist[newloc]] + number
                else:
                    number = number + [numberlist[newloc]]

                del numberlist[newloc]

        return int("".join(number))


    def convertList(self, numbers):
        lostnumbers = []
        while len(numbers):
            loc = list(numbers.keys())[0]
            number = [numbers[loc]]
            del numbers[loc]

            locations = [(loc[0]-1, loc[1]), (loc[0]+1, loc[1])]

            while len(locations):
                newloc = locations.pop(0)

                if newloc in numbers:
                    locations.extend([(newloc[0]-1, newloc[1]), (newloc[0]+1, newloc[1])])

                    if newloc[0] < loc[0]:
                        number = [numbers[newloc]] + number
                    else:
                        number = number + [numbers[newloc]]

                    del numbers[newloc]

            lostnumbers.append(int("".join(number)))

        return lostnumbers


    def run(self):
        numbers = {}
        symbols = []
        for loc, elem in self.inData:
            if elem not in ".1234567890":
                symbols.append((loc, elem))
            elif elem != ".":
                numbers.update({loc: elem})

        numberslost  = {k:v for k,v in numbers.items()}
        numbersfound = {k:v for k,v in numbers.items()}

        for symloc, symbol in symbols:
            for locdiff in [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]:
                newloc = (symloc[0]+locdiff[0], symloc[1]+locdiff[1])

                numberslost = self.findandpurge(numberslost, newloc)

        for loc in numberslost.keys():
            del numbersfound[loc]

        print(f"Sum of found numbers {sum(self.convertList(numbersfound))}")
        print(self.convertList(numberslost))


class Challenge2(Challenge1):
    ChallengeNr = 2

    def setup(self):
        super().setup()

    def run(self):
        numbers = {}
        symbols = []

        for loc, elem in self.inData:
            if elem not in ".1234567890":
                symbols.append((loc, elem))
            elif elem != ".":
                numbers.update({loc: elem})

        value = 0

        for symloc, symbol in symbols:
            if symbol != "*":
                continue

            print("==========")

            ratio = []

            locallist = {k:v for k,v in numbers.items()}

            
            for locdiff in [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]:
                newloc = (symloc[0]+locdiff[0], symloc[1]+locdiff[1])

                n = self.getNumberFromLocation(locallist, newloc)

                if n is not None:
                    ratio.append(n)

            if len(ratio) >= 2:
                ratio = list(set(ratio))
                value += ratio[0]*ratio[-1]

            else:
                print(symloc, symbol, ratio)
                for y in range(-2, 2):
                    for x in range(-4, 4):
                        if x == 0 and y == 0:
                            print('X', end="")
                            continue
                        print(self.inData.getLocation(x+symloc[0], y+symloc[1]), end="")
                    print()

        print(f"Sum of gear ratios: {value}")
