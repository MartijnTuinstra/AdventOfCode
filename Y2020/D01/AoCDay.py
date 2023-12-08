from AdventOfCode.AoCLib import AoCLibChallenge

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        pass

    def run(self):
        data = self.inData

        for value in data:
            for value2 in data:
                if value == value2:
                       continue
                if int(value) + int(value2) == 2020:
                    print(f"{value} + {value2} == 2020")
                    print(f"{value} * {value2}== {int(value)*int(value2)}")

class Challenge2(Challenge1):
    ChallengeNr = 2

    def setup(self):
        pass

    def run(self):
        data = self.inData

        for value in data:
            for value2 in data:
                for value3 in data:
                    if value == value2 or value == value3 or value2 == value3:
                        continue
                    if int(value) + int(value2) + int(value3) == 2020:
                        print(f"{value} + {value2} + {value3} == 2020")
                        print(f"{value} * {value2} * {value3}== {int(value)*int(value2)*int(value3)}")
