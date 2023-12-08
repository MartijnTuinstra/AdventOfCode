from AdventOfCode.AoCLib import AoCLibChallenge

import re

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        pass

    def run(self):
        lines = []

        numberlist = [(1, "one"), (2, "two"), (3, "three"), (4, "four"),\
                      (5, "five"), (6, "six"), (7, "seven"), (8, "eight"),\
                      (9, "nine")]

        for line in self.inData:
            tmp = ""
            tmp2 = ""
            i = 0
            print(f"Checking {line}")

            m = re.findall("(one|two|three|four|five|six|seven|eight|nine|zero|[0-9])", line)

            for match in m:
                if match in "123456789":
                    tmp2 += match
                    continue

                for n, number in numberlist:
                    if match == number:
                        tmp2 += str(n)
                        break

            while i < len(line):
                if line[i] in "123456789":
                    tmp += line[i]

                for n, number in numberlist:
                    if line[i:].startswith(number):
                        tmp += str(n)
                        break

                i += 1

            if (tmp != tmp2):
                print("NOT EQUAL: {tmp}, {tmp2}")

            if len(tmp) == 1:
                print(f"One Number: {tmp}")

            lines.append(int(tmp[0]+tmp[-1]))

        print(f"{lines}")
        print(f"Sum: {sum(lines)}")

class Challenge2(Challenge1):
    ChallengeNr = 2

    def setup(self):
        super().setup()

    def run(self):
        super().run()
