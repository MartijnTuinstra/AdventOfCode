from AdventOfCode.AoCLib import AoCLibChallenge
import re
from collections import namedtuple

depth = 0

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        self.data = {}
        self.reverse_data = {}

        for line in self.inData:
            elements = line.split(" ")

            subbags = []

            if elements[4] != "no":
                i = 4
                while True:
                    subbags.append((elements[i], elements[i+1]+" "+elements[i+2]))

                    if elements[i+3][-1] == ",":
                        i += 4
                    else:
                        break

            self.data[elements[0] +" "+ elements[1]] = subbags

            for amount, bag in subbags:
                if bag in self.reverse_data:
                    self.reverse_data[bag].append(elements[0] +" "+ elements[1])
                else:
                    self.reverse_data[bag] = [elements[0] +" "+ elements[1]]

    def canHoldMyBag(self, bag):
        global depth
        print(" "*depth+bag)
        if bag == "shiny gold":
            return True

        if len(self.data[bag]) == 0:
            return False

        retval = False

        depth += 1
        for amount, subbag in self.data[bag]:
            retval = retval | self.canHoldMyBag(subbag)
        depth -= 1

        return retval

    def run(self):
        #print(self.data["dull blue"])
        #print()
        #print(self.reverse_data)
        stack = ["shiny gold"]
        validbags = []

        while len(stack):
            bag = stack.pop(0)

            if bag not in self.reverse_data:
                print(f"Bag {bag} not in other bags")
                continue

            print(f"Bag {bag} goes into {self.reverse_data[bag]}")

            for prebag in self.reverse_data[bag]:
                if prebag not in validbags:
                    stack.append(prebag)
                    validbags.append(prebag)
        
        print(f" valid: {len(validbags)} | {validbags}")

class Challenge2(Challenge1):
    ChallengeNr = 2

    def calculateBags(self, bag):
        global depth
        cost = 1 if bag != "shiny gold" else 0

        if len(self.data[bag]) == 0:
            return 1

        depth += 1
        for amount, subbag in self.data[bag]:
            subamount = self.calculateBags(subbag)

            #print(" "*depth+f"{amount} * {subbag} == {subamount}")
            cost += int(amount) * subamount 
        depth -= 1

        return cost

    def run(self):

        cost = self.calculateBags("shiny gold")

        print(f"Bags: {cost}")
