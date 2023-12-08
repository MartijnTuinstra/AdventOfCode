from AdventOfCode.AoCLib import AoCLibChallenge

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        self.seeds = []
        self.maps = {}

        self.inData.append('')

        tmp = []
        for line in self.inData:
            if not line:
                if not self.seeds:
                    self.seeds = [int(x) for x in tmp[0].split(" ")[1:]]
                else:
                    self.maps.update({
                        tmp[0].split(" ")[0]: [[int(x) for x in y.split()] for y in tmp[1:]]
                    })

                tmp = []
                continue

            tmp.append(line)

    def map(self, number, map_s):
        map = self.maps[map_s]

        for dest, src, l in map:
            if number >= src and number < src + l:
                return (number - src) + dest

        return number

    def run(self):
        n = [x for x in self.seeds]
        types = ["seed", "soil", "fertilizer", "water", "light", "temperature", "humidity", "location"]

        for type_i in range(len(types)-1):
            map_s = f"{types[type_i]}-to-{types[type_i+1]}"

            new_n = []

            for number in n:
                new_n.append(self.map(number, map_s))

            n = new_n

        print(f"Min distance: {min(n)}")


class Range:
    def __init__(self, x, length, offset=0):
        self.x = x
        self.length = length
        self.offset = offset

    def isInRange(self, other):
        # returns selected_range, left_over_range
        if not isinstance(other, Range):
            raise ValueError("Must have Range object")

        if self.x >= other.x and self.x < other.x+other.length and self.x + self.length > other.x and self.x + self.length <= other.x + other.length:
            #yes fully
            # self:    ----
            #other:  --------
            return self, None
        elif self.x >= other.x and self.x < other.x+other.length and self.x + self.length > other.x + other.length:
            # yes partially, left part is in, right part is out
            # self:   ----
            #other: ----
            #  ret:   --++
            y = other.x + other.length
            keepPartLength = self.length - ((self.x+self.length) - (other.x+other.length))
            return Range(self.x, keepPartLength, self.offset), \
                   Range(y, ((self.x+self.length) - (other.x+other.length)), self.offset + keepPartLength)
        elif self.x < other.x and self.x + self.length > other.x:
            # yes partially
            # self:  ----
            #other:    ----
            #  ret:  ++--
            y = self.x + self.length
            return Range(other.x, self.length - (-self.x + other.x), self.offset + (other.x - self.x)), \
                   Range(self.x, self.length - (other.x - self.x), self.offset)
        else:
            return None, self

    def map(self, src, dest):
        return Range(self.x + (dest.x - src.x), self.length, self.offset)

    def __eq__(self, other):
        if not isinstance(other, Range):
            raise ValueError("Must have Range object")

        return (self.x == other.x) and (self.length == other.length)

    def __repr__(self):
        offsetstr = f"+{self.offset} " if self.offset else ""
        return f"Range [{offsetstr}{self.x}, {self.x+self.length-1}]"

class Challenge2(Challenge1):
    ChallengeNr = 2

    def setup(self):
        super().setup()

        seeds = []
        for s in range(0, len(self.seeds), 2):
            seeds.append(Range(self.seeds[s], self.seeds[s+1], self.seeds[s]))

        self.seeds = seeds

        for mapname, mapping in self.maps.items():
            tmp = []
            for dest,src,l in mapping:
                tmp.append((Range(dest, l), Range(src, l)))

            self.maps[mapname] = tmp

    def map(self, r, map_s):
        map = self.maps[map_s]

        current_range = r

        ret = []

        for dest, src in map:
            inRange, outRange = r.isInRange(src)
            if inRange:
                ret.append(inRange.map(src, dest))
                current_range = outRange

            if current_range is None:
                break

        if current_range and not (current_range == r):
            ret.extend(self.map(current_range, map_s))
        
        if not ret:
            return [r]
        else:
            return ret

    def run(self):
        stack = [x for x in self.seeds]
        types = ["seed", "soil", "fertilizer", "water", "light", "temperature", "humidity", "location"]

        for type_i in range(len(types)-1):
            map_s = f"{types[type_i]}-to-{types[type_i+1]}"

            new_n = []

            for number in stack:
                new_n.extend(self.map(number, map_s))

            stack = new_n

        min_location = 0xFFFFFFFF
        seed = -1
        for r in stack:
            if r.x < min_location:
                print(f"seed: {seed}, location: {min_location}")
                min_location = r.x
                seed = r.offset

        print(f"seed: {seed}, location: {min_location}")


