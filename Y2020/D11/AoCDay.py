from AdventOfCode.AoCLib import AoCLibChallenge
import copy

class SeatingArea:
    def __init__(self, area):
        self.area = area
        self.newArea = copy.deepcopy(area)

        self.iterlocation = (0, 0)

    def insideArea(self, x, y):
        if x < 0 or y < 0:
            return False
        if x >= len(self.area[0]) or y >= len(self.area):
            return False
        return True

    def getSeat(self, x, y):
        if self.insideArea(x, y):
            return self.area[y][x]
        else:
            return '.'

    def setSeat(self, x, y, value, changed):
        if not self.insideArea(x, y):
            return
        self.newArea[y][x] = value
        return changed

    def updateSeatingArea(self):
        for y in range(len(self.newArea)):
            for x in range(len(self.newArea[y])):
                self.area[y][x] = self.newArea[y][x]

    def findNeighbours(self, x, y):
        region = [ [None]*3 for i in range(3)]

        for j in range(0, 3):
            for i in range(0, 3):
                region[j][i] = self.getSeat(x+i-1, y+j-1)
        return region

    def rule(self, x, y):
        region = self.findNeighbours(x, y)
        occupied = 0
        free = 0
        for rx, ry in [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]:
            if region[ry+1][rx+1] == '#':
                occupied += 1
            elif region[ry+1][rx+1] == 'L':
                free += 1

        #print(region, occupied, free)
        if region[1][1] == 'L': #empty seat
            if occupied == 0:
                return ('#', True)
            else:
                return ('L', False)
        elif region[1][1] == '#': #occupied set
            if occupied >= 4:
                return ('L', True)
            else:
                return ('#', False)
        elif region[1][1] == '.':
            return ('.', False)

    def printBoard(self):
        print("\n".join(["".join(row) for row in self.area]))

    def applyRule(self, x, y):
        return self.setSeat(x, y, *self.rule(x, y))

    def __iter__(self):
        c = []
        for x in range(len(self.area[0])):
            c.extend((x, y) for y in range(len(self.area)))
        return iter(c)

    def count(self):
        count = 0
        for x, y in self:
            count += 1 if self.getSeat(x, y) == '#' else 0

        return count

class SeatingArea2(SeatingArea):
    def rule(self, x, y):
        occupied = 0
        #print(f" check {x} {y}")
        for direction in [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]:
            depth = 1
            inside = True;
            while(inside):
                nX = x + direction[0] * depth
                nY = y + direction[1] * depth
                #print(f" check {nX} {nY}")
                if not self.insideArea(nX, nY):
                    inside = False
                    continue

                s = self.getSeat(nX, nY)
                if s == 'L':
                    break
                elif s == '#':
                    occupied += 1
                    #print(f"  -- {nX} {nY}")
                    break

                depth += 1

        #print(f"{x} {y} found {occupied} occupied seats")
        s = self.getSeat(x, y)
        if s == '#' and occupied >= 5:
            return ('L', True)
        elif s == 'L' and occupied == 0:
            return ('#', True)
        return (s, False)


class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        data = []
        for row in self.inData:
            data.append([x for x in row])

        self.seatingArea = SeatingArea(data)

    def run(self):
        changed = True
        iteration = 0
        while changed:
            changed = False
            for x, y in self.seatingArea:
                changed = changed | self.seatingArea.applyRule(x, y)

            self.seatingArea.updateSeatingArea()
            #self.seatingArea.printBoard()
            iteration += 1

        print(f"After {iteration} iterations")
        self.seatingArea.printBoard()
        print(f"Occupied seats: {self.seatingArea.count()}")

class Challenge2(Challenge1):
    ChallengeNr = 2

    def setup(self):
        data = []
        for row in self.inData:
            data.append([x for x in row])

        self.seatingArea = SeatingArea2(data)

