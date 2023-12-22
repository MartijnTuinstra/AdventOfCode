from AdventOfCode.AoCLib import AoCLibChallenge

class module:
    def __init__(self, name, targets):
        self.name = name
        self.targets = targets

    @classmethod
    def create(cls, node_type, name, targets):
        if node_type == "%":
            return flip(name, targets)
        elif node_type == "&":
            return conj(name, targets)
        else:
            return broad(name, targets)

    def __repr__(self):
        return f"{self.name} -> {self.targets}"


class conj(module):
    def __init__(self, name, targets):
        super().__init__(name, targets)
        self.state = {}

    def register_state(self, origin):
        self.state[origin] = 0

    def compute(self, origin, signal):
        self.state[origin] = signal

        return [(self.name, dest, not all(self.state.values())) for dest in self.targets]

    def __repr__(self):
        return f"{self.name} | {self.state} -> {self.targets}"

class flip(module):
    def __init__(self, name, targets):
        super().__init__(name, targets)
        self.state = 0

    def compute(self, origin, signal):
        if signal == 0:
            self.state = self.state ^ 1
            return [(self.name, dest, self.state) for dest in self.targets]
        return []

class broad(module):
    def compute(self, origin, signal):
        return [(self.name, dest, signal) for dest in self.targets]

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        self.modules = {}

        for row in self.inData:
            name, target = row.split(" -> ")

            if name[0] == "%" or name[0] == "&":
                self.modules[name[1:]] = module.create(name[0], name[1:], target.split(", "))
            else:
                self.modules[name] = module.create("B", "broadcaster", target.split(", "))

        for mod in self.modules.values():
            for t in mod.targets:
                if t not in self.modules:
                    continue
                if not isinstance(self.modules[t], conj):
                    continue
                self.modules[t].register_state(mod.name)
        
        print(self.modules)

    def run(self):
        

        pulselist = []
        signalcount = [0, 0]

        i = 0
        while i < 1000:
            i += 1
            j = 0

            print(f"{i}", end="\r")

            pulselist = [("button", "broadcaster", 0)]
            #pulselist = [("broadcaster", "sp", 0)]

            while len(pulselist):
                j += 1

                if j % 1000 == 0:
                    print(f"{i}: {j} / {len(pulselist)}", end="\r")
                origin, target, signal = pulselist.pop(0)
                signalcount[signal] += 1

                # print(f"{origin} {signal}-> {target}")

                if target not in self.modules:
                    continue

                pulselist.extend(self.modules[target].compute(origin, signal))

       #     for k, (t, d, s) in self.modules.items():
       #         if t != "%":
       #             continue
       #         print(k, s)
       #     print(signalcount)
        print(signalcount)
        print(signalcount[0]*signalcount[1])


class Challenge2(Challenge1):
    ChallengeNr = 2

    def setup(self):
        super().setup()

    def run(self):
        
        pulselist = []
        signalcount = [0, 0]
        stop = False

        i = 0
        while not stop:
            i += 1
            j = 0

            print(f"{i}", end="\r")

            pulselist = [("button", "broadcaster", 0)]
            #pulselist = [("broadcaster", "sp", 0)]

            while len(pulselist):
                j += 1

                if j % 1000 == 0:
                    print(f"{i}: {j} / {len(pulselist)}", end="\r")
                origin, target, signal = pulselist.pop(0)
                signalcount[signal] += 1

                # print(f"{origin} {signal}-> {target}")

                if target not in self.modules:
                    if target == "rx":
                        if any(self.modules['bq'].state.values()):
                            print(f"{i} RX received | bq state: {self.modules['bq'].state}")
                        if signal == 0:
                            stop = True
                            break
                    continue

                pulselist.extend(self.modules[target].compute(origin, signal))

       #     for k, (t, d, s) in self.modules.items():
       #         if t != "%":

        print(i)
