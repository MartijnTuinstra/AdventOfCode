from AdventOfCode.AoCLib import AoCLibChallenge

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        self.data = []

        for row in self.inData:
            d, l, c = row.split()

            if d == "U":
                d = -1j
            elif d == "D":
                d = 1j
            elif d == "R":
                d = 1
            elif d == "L":
                d = -1

            self.data.append((d, int(l), c[2:-1]))

    def run(self):

        plan = {complex(0, 0): '000000'}
        
        pos = complex(0, 0)

        topleft  = complex(0,0)
        botright = complex(0,0)

        circumference = 0

        for dir, length, color  in self.data:
            pos = pos + length * dir
            plan[pos] = color

            circumference += length

            if pos.real > botright.real:
                botright = complex(pos.real, botright.imag)
            if pos.imag > botright.imag:
                botright = complex(botright.real, pos.imag)
            if pos.real < topleft.real:
                topleft = complex(pos.real, topleft.imag)
            if pos.imag < topleft.imag:
                topleft = complex(topleft.real, pos.imag)

        print(plan)
        print(topleft, botright)

        inside = False
        area = 0

        key_list = list(plan.keys())
        print(key_list)
        for i in range(len(plan)):

            print(f"{key_list[i]} * {key_list[(i+1) % len(key_list)]}")

            area += key_list[i].real*key_list[(i+1) % len(key_list)].imag
            area -= key_list[i].imag*key_list[(i+1) % len(key_list)].real

        print(f"Area: {area/2}, circumference: {circumference/2} | {area/2 + circumference/2 + 1}")

class Challenge2(Challenge1):
    ChallengeNr = 2

    def setup(self):
        self.data = []

        for row in self.inData:
            d, l, c = row.split()

            c = c[2:-1]

            l = int(c[:5], 16)

            if c[5] == "3":
                d = -1j
            elif c[5] == "1":
                d = 1j
            elif c[5] == "0":
                d = 1 
            elif c[5] == "2":
                d = -1
            else:
                print(f"unknown direction {c[5]} | {c}")

            self.data.append((d, l, c))


    def run(self):
        super().run()
