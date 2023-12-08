from AdventOfCode.AoCLib import AoCLibChallenge

import primefac

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        self.route = self.inData[0]

        self.nodes = {}

        for s in self.inData[2:]:
            name = s[0:3]
            t1 = s[7:10]
            t2 = s[12:15]

            self.nodes[name] = (t1, t2)

    def run(self):
        location = "AAA"
        destination = "ZZZ"
        i = 0

        while location != destination:
            choice = self.route[i % len(self.route)]
            i += 1

            if choice == 'L':
                location = self.nodes[location][0]
            else:
                location = self.nodes[location][1]

        print(i, location)



class Challenge2(Challenge1):
    ChallengeNr = 2

    def setup(self):
        super().setup()

    def run(self):
        locations = []
        paths = []

        for node in self.nodes.keys():
            if node[-1:] == 'A':
                locations.append([node])

        j = 0
        for j in range(len(locations)):
            i = 0

            path = [(i, locations[j][0])]
            search = True
            while search:
                if locations[j][-1][-1] == 'Z':
                    path.append((i, locations[j][-1]))
                    search = False

                choice = self.route[i % len(self.route)]
                i += 1

                if choice == 'L':
                    locations[j].append(self.nodes[locations[j][-1]][0])
                else:
                    locations[j].append(self.nodes[locations[j][-1]][1])

            paths.append(path)

        cycles = [x[1][0] for x in paths]

        factors = []

        for x in cycles:
            for factor in primefac.primefac(x):
                factors.append(factor)

        result = 1

        for factor in set(factors):
            result *= factor

        print(f"Result: {result}")
