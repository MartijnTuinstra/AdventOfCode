from AdventOfCode.AoCLib import AoCLibChallenge

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        self.maxX = 0
        self.maxY = 0
        self.maxZ = 0

        for line in self.inData:
            c = [int(x) for x in line.split(",")]
            self.maxX = max(self.maxX, c[0])
            self.maxY = max(self.maxY, c[1])
            self.maxZ = max(self.maxZ, c[2])

        self.space = [ [ [0] * (self.maxZ+1) for i in range(self.maxY+1) ] for j in range(self.maxX+1) ]
        self.cubes = 0

        for line in self.inData:
            c = [int(x) for x in line.split(",")]
            self.space[c[0]][c[1]][c[2]] = 1
            print(f"Set {c[0]}|{c[1]}|{c[2]}")
            self.cubes += 1

        print(f"Stored {self.cubes} cubes")



    def run(self):
        sides = 0
        for x in range(0, self.maxX+1):
            for y in range(0, self.maxY+1):
                for z in range(0, self.maxZ+1):
                    if not self.space[x][y][z]:
                        continue

                    for sX, sY, sZ in [(-1,0,0), (0,-1,0), (0,0,-1), (1,0,0), (0,1,0), (0,0,1)]:
                        if x+sX < 0 or y+sY < 0 or z+sZ < 0 or \
                           x+sX > self.maxX or y+sY > self.maxY or z+sZ > self.maxZ:
                            continue

                        if self.space[x+sX][y+sY][z+sZ]:
                            sides += 1

        area = self.cubes * 6 - sides

        print(f"Area = {area}")




class Challenge2(Challenge1):
    ChallengeNr = 2

    def run(self):

        # Flood space
        stack = [(0,0,0)]

        while len(stack):
            x, y, z = stack.pop(0)
            self.space[x][y][z] = 2

            for sX, sY, sZ in [(-1,0,0), (0,-1,0), (0,0,-1), (1,0,0), (0,1,0), (0,0,1)]:
                if x+sX < 0 or y+sY < 0 or z+sZ < 0 or \
                    x+sX > self.maxX or y+sY > self.maxY or z+sZ > self.maxZ:
                    continue

                location = (x+sX,y+sY,z+sZ)

                if self.space[x+sX][y+sY][z+sZ] == 0 and location not in stack:
                    stack.append(location)

        for x in range(0, self.maxX+1):
            for y in range(0, self.maxY+1):
                for z in range(0, self.maxZ+1):
                    if self.space[x][y][z]:
                        continue

                    # enclosed air
                    print(f"Trapped air pocket {x}|{y}|{z}")
                    self.space[x][y][z] = 1
                    self.cubes += 1

        sides = 0

        for x in range(0, self.maxX+1):
            for y in range(0, self.maxY+1):
                for z in range(0, self.maxZ+1):
                    if self.space[x][y][z] != 1:
                        continue

                    for sX, sY, sZ in [(-1,0,0), (0,-1,0), (0,0,-1), (1,0,0), (0,1,0), (0,0,1)]:
                        if x+sX < 0 or y+sY < 0 or z+sZ < 0 or \
                           x+sX > self.maxX or y+sY > self.maxY or z+sZ > self.maxZ:
                            continue

                        if self.space[x+sX][y+sY][z+sZ] == 1:
                            sides += 1

        area = self.cubes * 6 - sides

        print(f"Area = {area}")
