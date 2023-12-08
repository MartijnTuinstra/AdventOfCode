from AdventOfCode.AoCLib import AoCLibChallenge

import re

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        self.games = {}

        for line in self.inData:
            gameid, games = line.split(":")

            gameid = gameid.split(" ")[-1]

            games = games.split(";")

            gamecubes = []

            for game in games:
                cubes = re.findall("([0-9]+) ([a-z]+)", game)

                cubeinfo = {}

                for cube in cubes:
                    cubeinfo.update({cube[1]: int(cube[0])})

                gamecubes.append(cubeinfo)

            self.games.update({int(gameid): gamecubes})

    def run(self):
        maxcubes = {"red":12, "green":13, "blue":14}
        valid = 0
        validCount = 0

        print(self.games)

        for gameid, game in self.games.items():
            isValid = True
            for cubes in game:
                for cube in maxcubes.keys():
                    if cube not in cubes:
                        continue

                    if cubes[cube] > maxcubes[cube]:
                        isValid = False

            valid += 1 if isValid else 0
            validCount += gameid if isValid else 0

        print(f"Valid Games: {valid}/{validCount}")

class Challenge2(Challenge1):
    ChallengeNr = 2

    def setup(self):
        super().setup()

    def run(self):
        count = 0
        
        for gameid, game in self.games.items():
            maxcubes = {"red":0, "green":0, "blue":0}

            for cubes in game:
                for cube in cubes.keys():
                    maxcubes[cube] = max(maxcubes[cube], cubes[cube])

            power = maxcubes["red"] * maxcubes["green"] * maxcubes["blue"]

            count += power

        print(f"Count: {count}")
