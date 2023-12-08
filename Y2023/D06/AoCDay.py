from AdventOfCode.AoCLib import AoCLibChallenge

from math import sqrt

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        self.races = []

        times     = self.inData[0].split()
        distances = self.inData[1].split()
        
        for i in range(1, len(times)):
            self.races.append((int(times[i]), int(distances[i])))

    def run(self):
        total = 1

        for time, record in self.races:
            # find distance
            #   distance = v * t
            #     , where t = (time - x), and v = x, x = button_time
            #   distance = x * (time - x) = x*time - x*x
            # local optimum is d (distance) / dx == 0:
            #   -2x - time => x = time / 2

            x = int(time / 2)

            distance = lambda y: y * (time - y)

            # search for other winning strategies
            # inverse for bounds
            # button_time = 1/2 * (t +/- sqrt(t*t - 4*record_distance))
            def bounds(t, r):
                return int(0.5 * (t + sqrt(t*t - 4 * r))), int(0.5 * (t - sqrt(t*t - 4 * r)))

            high, low = bounds(time, record)

            # Check if bounds are correct (rounding errors)
            while distance(low) <= record:
                low += 1
            while distance(high) <= record:
                high -= 1

            total *= high - low + 1

        print(f"Score: {total}")

class Challenge2(Challenge1):
    ChallengeNr = 2

    def setup(self):
        self.races = []

        times     = ""
        distances = ""
        
        for i in range(1, len(self.inData[0].split())):
            times     += self.inData[0].split()[i]
            distances += self.inData[1].split()[i]

        self.races.append((int(times), int(distances)))
