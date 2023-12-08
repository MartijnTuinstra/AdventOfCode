from AdventOfCode.AoCLib import AoCLibChallenge

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        self.inDataTo2D()
        self.forrest = self.inData
        # forrest[down][right]

    def countTrees(self, down, right):
        count = 0
        x = 0
        width = self.forrest.width
        for y in range(0, self.forrest.height, down):
            if self.forrest[y][x % width] == '#':
                count += 1
            x += right

        return count

    def run(self):
        print(f"Trees: {self.countTrees(1, 3)}")

class Challenge2(Challenge1):
    ChallengeNr = 2

    def run(self):
        count = 1
        for i in ((1, 1), (1, 3), (1, 5), (1, 7), (2, 1)):
            count *= self.countTrees(*i)

        print(f"Trees: {count}")
