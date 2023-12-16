from AdventOfCode.AoCLib import AoCLibChallenge

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        pass

    def run(self, start=(-1, 0, 1, 0)):

        visited = [['.' for y in range(len(self.inData[0]))] for x in range(len(self.inData))]

        beams = [start]

        active_splitters = {}

        while len(beams):
            x, y, dx, dy = beams.pop(0)

            i = 1

            while True:
                if (x + i * dx) < 0 or (x + i * dx) >= len(self.inData[0]):
                    break
                elif (y + i* dy) < 0 or (y + i * dy) >= len(self.inData):
                    break

                visited[y+i*dy][x+i*dx] = '#'

                c = self.inData[y+i*dy][x+i*dx]

                if c == "-" and dy != 0:
                    if (x+i*dx, y+i*dy) in active_splitters:
                        break
                    active_splitters.update({(x+i*dx, y+i*dy): True})
                    beams.append((x+i*dx, y+i*dy, -1, 0))
                    beams.append((x+i*dx, y+i*dy,  1, 0))
                    break

                if c == "|" and dx != 0:
                    if (x+i*dx, y+i*dy) in active_splitters:
                        break
                    active_splitters.update({(x+i*dx, y+i*dy): True})
                    beams.append((x+i*dx, y+i*dy, 0, -1))
                    beams.append((x+i*dx, y+i*dy, 0,  1))
                    break

                if c == "\\":
                    beams.append((x+i*dx, y+i*dy, dy, dx))
                    break

                if c == "/":
                    beams.append((x+i*dx, y+i*dy, -dy, -dx))
                    break

                i+=1


        count = 0

        for row in visited:
            print()
            for c in row:
                print(c, end="")
                if c == '#':
                    count += 1

        print(f"\ncount: {count}")

        return count
            

class Challenge2(Challenge1):
    ChallengeNr = 2

    def setup(self):
        super().setup()

    def run(self):
        
        options = []

        h = len(self.inData)
        w = len(self.inData[0])

        options += [(x, -1, 0,  1) for x in range(w)]
        options += [(x,  h, 0, -1) for x in range(w)]
        options += [(-1, y,  1, 0) for y in range(h)]
        options += [( w, y, -1, 0) for y in range(h)]

        best = 0
        bestoption = None

        for option in options:
            score = super().run(option)

            if score > best:
                best = score
                bestoption = option

        print(f"Best score: {best}")
