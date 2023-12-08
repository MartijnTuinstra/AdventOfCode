
from AdventOfCode.AoCLib import AoCLibChallenge

rockData = """####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
"""

class Rock:
    def __init__(self, pattern):
        self.height = len(pattern)
        self.width = len(pattern[0])

        self.pattern = [0] * self.height

        for y in range(self.height):
            for x in range(self.width):
                self.pattern[y] |= (1 << (7-x)) if pattern[y][x] == '#' else 0

    def get(self, x, y):
        if x < 0 or y < 0:
            return None
        elif x >= self.width or y >= self.height:
            return None

        return self.pattern[y] & (1 << (7-x))

    def __repr__(self):
        return f"Rock: {self.pattern}"

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        tmp_rock = []
        self.rocks = []
        for line in rockData.split("\n"):
            if line == "":
                self.rocks.append(Rock(tmp_rock))
                tmp_rock = []
                continue

            tmp_rock.append(line)

        for line in self.inData:
            self.stream = line

        print("rocks" + str(self.rocks))

    def printChamber(self, chamber, data=None, height=None, offsetY=0):
        if height is None:
            height = len(chamber[0])

        chambermap = ["|"]
        for y in range(height, -1, -1):
            chambermap[-1] += f"{y+offsetY:4d}|"
            for x in range(7):
                if data is not None and data[0].get(x-data[1][0], data[0].height-1-y+data[1][1]):
                    chambermap[-1] += "@"
                else:
                    chambermap[-1] += '#' if chamber[y] & (1 << (7-x)) else '.'


            chambermap[-1] += "|"
            chambermap.extend(["|"])

        print("\n".join(chambermap[:-1]))
        print("+----+-------+")

    def collides(self, chamber, rock, newPosition):
        for x in range(rock.width):
            for y in range(rock.height):
                if not rock.get(x,y):
                    continue

                if chamber[rock.height-y-1+newPosition[1]] & (1 << (7-(x+newPosition[0]))):
                    return True
        return False

    def applyRock(self, chamber, rock, position):
        for x in range(rock.width):
            for y in range(rock.height):
                if not rock.get(x,y):
                    continue

                chamber[rock.height-y-1+position[1]] |= (1 << (7-(x+position[0])))

        return chamber


    def run(self):
        chamber = [0] * 4000 # Chamber: 7bits wide(x), 100 height(y)

        highestRock = 0 # Floor
        currentRock = 0
        currentJet = 0

        currentPosition = (0, 0)

        done = 0

        while done < 2022:
            # Init new rock
            rock = self.rocks[currentRock]
            currentRock = (currentRock + 1) % len(self.rocks)

            currentPosition = [2, highestRock + 3]
            printHighest = currentPosition[1]+rock.height-1

            #self.printChamber(chamber, (rock, currentPosition), printHighest)

            rockStuck = False

            while not rockStuck:
                # Get jet
                jet = self.stream[currentJet]
                currentJet = (currentJet + 1) % len(self.stream)

                newPosition = [currentPosition[0], currentPosition[1]]
                if jet == '<':
                    newPosition = [max(0, currentPosition[0] - 1), currentPosition[1]]
                elif jet == '>':
                    newPosition = [min(7-rock.width, currentPosition[0] + 1), currentPosition[1]]

                if self.collides(chamber, rock, newPosition):
                    newPosition = currentPosition

                currentPosition = [newPosition[0], newPosition[1]]

                #self.printChamber(chamber, (rock, currentPosition), printHighest)

                newPosition = [currentPosition[0], currentPosition[1]]
                newPosition[1] = max(-1, currentPosition[1] - 1)

                if self.collides(chamber, rock, newPosition) or newPosition[1] == -1:
                    chamber = self.applyRock(chamber, rock, currentPosition)
                    #self.printChamber(chamber, None, printHighest)
                    highestRock = max(highestRock, currentPosition[1] + rock.height)
                    rockStuck = True
                    done += 1
                    continue

                currentPosition = newPosition

                #self.printChamber(chamber, (rock, currentPosition), printHighest)

            #done = True

        self.printChamber(chamber, (rock, currentPosition), printHighest)

class Challenge2(Challenge1):
    ChallengeNr = 2

    def run(self):
        chamberSize = 1000000
        chamber = [0] * chamberSize # Chamber: 7bits wide(x), 100 height(y)

        highestRock = 0 # Floor
        currentRock = 0
        currentJet = 0

        currentPosition = (0, 0)

        step = 0

        lookup = dict()

        while step < 1000000000000:
            if step % 10000 == 0:
                print(step)
            # Init new rock
            rock = self.rocks[currentRock]
            currentRock = (currentRock + 1) % len(self.rocks)

            currentPosition = [2, highestRock + 3]
            printHighest = currentPosition[1]+rock.height-1

            key = currentRock, currentJet
            # Check if combination of rock and jet has occurred before
            if key in lookup:
                # Get previous occurrance
                Step, HighestRock = lookup[key]
                # divisor / modulo of (1e12-step) / (step-Step)
                # check if there can be n blocks of size (current step - previous Step)
                d, m = divmod(1e12-step, step-Step)
                # if modulo is zero
                if m == 0:
                    print(f"Calculated at {step}")
                    print(highestRock + (highestRock-HighestRock)*d)
                    break
            else:
                lookup[key] = step, highestRock

            if currentPosition[1] > chamberSize - 10:
                print("OVERFLOW")
                break

            rockStuck = False

            while not rockStuck:
                # Get jet
                jet = self.stream[currentJet]
                currentJet = (currentJet + 1) % len(self.stream)

                newPosition = [currentPosition[0], currentPosition[1]]
                if jet == '<':
                    newPosition = [max(0, currentPosition[0] - 1), currentPosition[1]]
                elif jet == '>':
                    newPosition = [min(7-rock.width, currentPosition[0] + 1), currentPosition[1]]

                if self.collides(chamber, rock, newPosition):
                    newPosition = currentPosition

                currentPosition = [newPosition[0], newPosition[1]]

                #self.printChamber(chamber, (rock, currentPosition), highestRock)

                newPosition = [currentPosition[0], currentPosition[1]]
                newPosition[1] = max(-1, currentPosition[1] - 1)

                if self.collides(chamber, rock, newPosition) or newPosition[1] == -1:
                    chamber = self.applyRock(chamber, rock, currentPosition)
                    #self.printChamber(chamber, None, highestRock)
                    highestRock = max(highestRock, currentPosition[1] + rock.height)
                    rockStuck = True
                    step += 1
                    continue

                currentPosition = newPosition

                #self.printChamber(chamber, (rock, currentPosition), highestRock)

            #step = True

        #self.printChamber(chamber, (rock, currentPosition), printHighest)
