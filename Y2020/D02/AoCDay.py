from AdventOfCode.AoCLib import AoCLibChallenge

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def isValid(min, max, letter, password):
        if password.count(letter) >= int(min) and password.count(letter) <= int(max):
            return True
        return False

    def setup(self):
        pass

    def run(self):
        valid = 0

        for password in self.inData:
            (minmax, letter, password) = [t(s) for t,s in zip((str,str,str), password.split())]

            mi, ma = minmax.split("-")

            print(f" - {mi} < {letter} < {ma} | {password} | {password.count(letter[0])}")

            if isValid(mi, ma, letter[0], password):
                valid += 1

        print(f"Valid passwords: {valid}")


class Challenge2(Challenge1):
    ChallengeNr = 2

    def isValid(min, max, letter, password):
        if (password[int(min)-1] == letter) + (password[int(max)-1] == letter) == 1:
            return True
        return False

