from AdventOfCode.AoCLib import AoCLibChallenge

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        data = []
        
        for line in self.inData:
            tmp = line.split(" ")

            l = [int(x) for x in tmp[1].split(",")]
            
            data.append([tmp[0], l])

        self.inData = data

    def findOptions(self, row, options, depth=0):
        if len(options) == 0:
             if row.count("#") == 0:
                return 1

             return 0

        best = max(options)
        bestIx = options.index(best)

        valid = 0


        for x in range(len(row)-best+1):
            fits = True

            if row[x:x+best].count(".") > 0:
                x += best
                continue

            leftOkay  = (x == 0             or row[x-1]    != '#')
            rightOkay = (x == len(row)-best or row[x+best] != '#')

            if leftOkay and rightOkay:
                left  = self.findOptions(row[:max(0,x-1)], options[:bestIx], depth+1)

                if left == 0:
                    continue

                right = self.findOptions(row[x+best+1:], options[bestIx+1:], depth+1)

                valid += left * right

        return valid

    def run(self):
        valid = 0
        
        for row, options in self.inData:
            valid += self.findOptions(row, options)

        print(f"Valid: {valid}")

class Challenge2(Challenge1):
    ChallengeNr = 2

    def setup(self):
        super().setup()

    def findOptions(self, row, options, depth=0):

        if len(options) == 0:
             if row.count("#") == 0:
                return 1

             return 0

        key = (row, *options)

        if key in self.databank:
            return self.databank[key]

        best = max(options)
        bestIx = options.index(best)

        valid = 0


        for x in range(len(row)-best+1):
            fits = True

            if row[x:x+best].count(".") > 0:
                x += best
                continue

            leftOkay  = (x == 0             or row[x-1]    != '#')
            rightOkay = (x == len(row)-best or row[x+best] != '#')

            if leftOkay and rightOkay:
                left  = self.findOptions(row[:max(0,x-1)], options[:bestIx], depth+1)

                if left == 0:
                    continue

                right = self.findOptions(row[x+best+1:], options[bestIx+1:], depth+1)

                valid += left * right

        self.databank[key] = valid

        return valid

    def run(self):
        valid = 0

        self.databank = {}
        
        x = 0
        for row, options in self.inData:
            if x % 10 == 0:
                print(f"{x}/{len(self.inData)}\r", end="")

            valid += self.findOptions("."+"?".join(row for x in range(5))+".", options*5)

            x+=1

        print(f"Valid: {valid}")
        print(f"Datarecords: {len(self.databank)}")

