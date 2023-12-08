from AdventOfCode.AoCLib import AoCLibChallenge

import re

class Passport:
    def __init__(self, data):
        data = " ".join(data)

        self.data = {}
        for element in data.split(" "):
            key, value = element.split(":")

            self.data[key] = value

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        self.passports = []
        tmp = []

        for line in self.inData:
            if line == "":
                self.passports.append(Passport(tmp))
                tmp = []
                continue

            tmp.append(line)

    def isValid(self, passport):
        keys = passport.data.keys()

        if len(keys) == 8:
            return True

        if len(keys) == 7 and "cid" not in keys:
            return True

        return False


    def run(self):
        valid = 0
        for passport in self.passports:
            valid += 1 if self.isValid(passport) else 0
            
        print(f"Valid passports: {valid}")

class Challenge2(Challenge1):
    ChallengeNr = 2

    def isValid(self, passport):
        keys = passport.data.keys()

        if len(keys) < 7 or (len(keys) == 7 and "cid" in keys):
            return False

        byr = int(passport.data['byr'])
        if byr < 1920 or byr > 2002:
            return False

        iyr = int(passport.data['iyr'])
        if iyr < 2010 or iyr > 2020:
            return False

        eyr = int(passport.data['eyr'])
        if eyr < 2020 or eyr > 2030:
            return False

        if not (passport.data['hgt'].endswith("cm") or passport.data['hgt'].endswith("in")):
            return False

        hgt = (int(passport.data['hgt'][:-2]), passport.data['hgt'][-2:])
        if hgt[1] == "cm" and (hgt[0] < 150 or hgt[0] > 193):
            return False
        elif hgt[1] == "in" and (hgt[0] < 59 or hgt[0] > 76):
            return False

        hcl = re.match("(#[0-9a-z]{6})", passport.data['hcl'])
        if hcl is None:
            return False

        if passport.data['ecl'] not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
            return False

        if len(passport.data['pid']) != 9:
            return False

        try:
            int(passport.data['pid'])
        except ValueError:
            return False

        return True

