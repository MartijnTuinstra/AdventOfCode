from AdventOfCode.AoCLib import AoCLibChallenge

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        pass

    def run(self):

        score = 0

        for hash in self.inData[0].split(","):

            value = 0

            for c in hash:
                value += ord(c)
                value *= 17
                value = value % 256

            score += value
            print(value)

        print(f"Score {score}")
        


class Challenge2(Challenge1):
    ChallengeNr = 2

    def run(self):
        
        score = 0
        boxes = [[] for x in range(256)]

        for hash in self.inData[0].split(","):

            value = 0
            op = ""

            for c in hash:
                if c == "-" or c == "=":
                    op = c
                    break

                value = ((value + ord(c)) * 17) % 256

            label = value

            if op == "=":
                ix = -1
                for i in range(len(boxes[label])):
                    if boxes[label][i].startswith(hash.split("=")[0]):
                        ix = i
                        break

                if ix == -1:
                    boxes[label].append(" ".join(hash.split("=")))
                else:
                    boxes[label][ix] = " ".join(hash.split("="))
            elif op == "-":
                ix = -1
                for i in range(len(boxes[label])):
                    if boxes[label][i].startswith(hash.split("-")[0]):
                        ix = i
                        break

                if ix != -1:
                    boxes[label].pop(ix)
        

        for i in range(len(boxes)):

            for slot in range(len(boxes[i])):
                s = (i + 1) * (slot + 1) * int(boxes[i][slot].split(" ")[1])
                print(boxes[i][slot].split(" ")[0], i+1, slot+1)
                score += s

        print(f"score: {score}")

