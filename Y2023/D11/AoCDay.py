from AdventOfCode.AoCLib import AoCLibChallenge

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        data = []

        self.emptyRow = []
        self.emptyColumn = []

        for y in range(len(self.inData)):
            if '#' not in self.inData[y]:
                self.emptyRow.append(y)

        for x in range(len(self.inData[0])):
            hasGalaxy = False

            for y in range(len(self.inData)):
                if self.inData[y][x] == '#':
                    hasGalaxy = True
                    break

            if not hasGalaxy:
                self.emptyColumn.append(x)

    def run(self, distance_inbetween=1):

        galaxies = []
        
        for y in range(len(self.inData)):
            for x in range(len(self.inData[y])):
                if self.inData[y][x] == '#':
                    galaxies.append((x, y))

        galaxies_pairs = {}
        total_dist = 0

        for i in range(len(galaxies)):
            for j in range(i+1, len(galaxies)):
                A = galaxies[i]
                B = galaxies[j]

                dist = abs(A[0]-B[0]) + abs(A[1]-B[1])

                for x in range(min(A[0], B[0]), min(A[0], B[0]) + abs(A[0]-B[0])):
                    if x in self.emptyColumn:
                        dist += distance_inbetween

                for y in range(min(A[1], B[1]), min(A[1], B[1]) + abs(A[1]-B[1])):
                    if y in self.emptyRow:
                        dist += distance_inbetween
                
                galaxies_pairs[(A, B)] = dist
                total_dist += dist

        print(f"Total distance: {total_dist} of {len(galaxies_pairs)} pairs")


class Challenge2(Challenge1):
    ChallengeNr = 2

    def setup(self):
        super().setup()

    def run(self):
        super().run(1000000-1)
