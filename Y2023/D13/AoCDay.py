from AdventOfCode.AoCLib import AoCLibChallenge

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        self.patterns = []
        
        tmp = []
        for line in self.inData:
            if line == '':
                self.patterns.append(tmp)
                tmp = []
                continue

            tmp.append(line)
        self.patterns.append(tmp)

    def run(self):
        score = 0

        for pattern in self.patterns:
            possible_y = []
            possible_x = {}

            for y in range(len(pattern)):
                if y < len(pattern)-1 and pattern[y] == pattern[y+1]:
                    possible_y.append(y)

                for x in range(len(pattern[y])-1):
                    if pattern[y][x] == pattern[y][x+1]:
                        if x in possible_x:
                            possible_x[x] += 1
                        else:
                            possible_x[x] = 1

            mirror_y = []
            mirror_x = []

            # test possibilites
            for y in possible_y:
                valid = True
                for i in range(1, len(pattern)):
                    if (y-i) < 0 or (y+i+1) >= len(pattern):
                        break

                    if pattern[y-i] != pattern[y+i+1]:
                        valid = False
                        break

                if valid:
                    mirror_y.append(y)

            for x in [k for k, v in possible_x.items() if v == len(pattern)]:
                valid = True
                for i in range(1, len(pattern[0])):
                    if (x-i) < 0 or (x+i+1) >= len(pattern[0]):
                        break

                    if sum(pattern[y][x-i] != pattern[y][x+i+1] for y in range(len(pattern))):
                        valid = False
                        break

                if valid:
                    mirror_x.append(x)
            
            if mirror_x:
                score += (mirror_x[0]+1)
            if mirror_y:
                score += 100 * (mirror_y[0]+1)

        print(f"Score: {score}")


class Challenge2(Challenge1):
    ChallengeNr = 2

    def setup(self):
        super().setup()

    def run(self):
        score = 0

        for pattern in self.patterns:
            possible_y = []
            possible_x = {}

            for y in range(len(pattern)):
                if y < len(pattern)-1 and sum(pattern[y][x] != pattern[y+1][x] for x in range(len(pattern[0]))) <= 1:
                    possible_y.append(y)

                for x in range(len(pattern[y])-1):
                    if pattern[y][x] == pattern[y][x+1]:
                        if x in possible_x:
                            possible_x[x] += 1
                        else:
                            possible_x[x] = 1

            mirror_y = []
            mirror_x = []

            # test possibilites
            for y in possible_y:
                faults = 0
                for i in range(len(pattern)):
                    if (y-i) < 0 or (y+i+1) >= len(pattern):
                        break

                    faults += sum(pattern[y-i][x] != pattern[y+i+1][x] for x in range(len(pattern[0])))
                    if faults > 1:
                        break

                if faults == 1:
                    mirror_y.append(y)

            for x in [k for k, v in possible_x.items() if v >= len(pattern) - 1]:
                faults = 0
                for i in range(len(pattern[0])):
                    if (x-i) < 0 or (x+i+1) >= len(pattern[0]):
                        break

                    faults += sum(pattern[y][x-i] != pattern[y][x+i+1] for y in range(len(pattern)))
                    if faults > 1:
                        break

                if faults == 1:
                    mirror_x.append(x)
           
            if len(mirror_x) > 1 or len(mirror_y) > 1:
                for r in pattern:
                    print(r)

            if mirror_x:
                score += (mirror_x[0]+1)
            if mirror_y:
                score += 100 * (mirror_y[0]+1)

        print(f"Score: {score}")
