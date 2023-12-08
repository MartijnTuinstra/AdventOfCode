from AdventOfCode.AoCLib import AoCLibChallenge
import re
import sys

ValveList = {}

def getPathToNode(origin, target):
    visited = []

    paths = [(x, []) for x in origin.linkedValves]

    while paths:
        path = paths.pop(0)

        route = path[1] + [path[0].name]

        if path[0] == target:
            return route

        if path[0] in visited:
            continue

        visited.append(path[0])

        paths.extend([(x, route) for x in path[0].linkedValves])


class Valve:
    def __init__(self, valveName, rate, linkedValves):
        self.name = valveName
        ValveList[self.name] = self

        self.rate = rate
        self.flow = None

        self.linkedValves = linkedValves
        self.pathToNode = {}

        self.releaved = 0
        self.route = []

    def linkValves(self):
        for i in range(len(self.linkedValves)):
            v = self.linkedValves[i]
            v = ValveList[v]
            self.linkedValves[i] = v

    def getDepthToAll(self):
        for v in ValveList.values():
            if v == self:
                continue

            if v.rate == 0:
                continue

            self.pathToNode[v.name] = getPathToNode(self, v)

    def print(self):
        print(f"{self.name} - {self.rate:2d} - {self.releaved:4d} - {self.route}")
        for d, r in self.pathToNode.items():
            print(f"  {d} => {r}")


class State:
    def __init__(self, location='AA', time=0, route=[], visited=[], score=0, rate=0):
        self.location = location
        self.time = time
        self.route = route
        self.visited = visited
        self.score=score
        self.rate=rate

    def findStates(self, maxtime, visited=[]):
        timeleft = maxtime - self.time
        newStateList = []
        valve = ValveList[self.location]
        options = []
        for dest, routeTo in valve.pathToNode.items():
            if dest in visited or dest in self.visited or len(routeTo) + 1 >= timeleft:
                continue

            newStateList.append(
                State(
                    dest,
                    self.time + len(routeTo) + 1,
                    self.route+routeTo+[dest],
                    self.visited+[dest],
                    self.score+(len(routeTo)+1)*sum(ValveList[x].rate for x in visited),
                    sum(ValveList[x].rate for x in (self.visited+[dest]))
                )
            )

        return newStateList

    def calculateRoute(self, maxtime):
        vlist = []
        pressure = 0
        for i in range(len(self.route)):
            flow = sum(ValveList[x].rate for x in vlist)
            pressure += flow

            if i > 0 and self.route[i] == self.route[i-1]:
                if self.route[i] not in vlist:
                    vlist = vlist + [self.route[i]]

        flow = sum(ValveList[x].rate for x in vlist)

        return pressure+flow*(maxtime - len(self.route))

    def getEndScore(self, maxtime):
        return self.score + (self.rate * (maxtime - len(self.route)))

    def getTime(self):
        return self.time

    def strRoute(self, route):
        return "".join(x for x in route)

    def __str__(self):
        return f"Ch1: {self.location} | {self.score} | {self.visited}\t{self.strRoute(self.route)}"

    def __repr__(self):
        return str(self)

    @classmethod
    def prune(cls, maxtime, newStateList):
        # No pruning necessary
        return newStateList

class State2:
    def __init__(self, location=('AA', 'AA'), time=(0,0), route=([],[]), visited=([],[]), score=(0, 0), rate=(0,0)):
        self.challenges = [
            State( location[0], time[0], route[0], visited[0], score[0], rate[0] ),
            State( location[1], time[1], route[1], visited[1], score[1], rate[1] )
        ]

    def findStates(self, maxtime):
        if len(self.challenges[0].route) <= len(self.challenges[1].route):
            newStateListMe = self.challenges[0].findStates(maxtime, self.challenges[0].visited + self.challenges[1].visited)
            newStateListEl = [self.challenges[1]]
        else:
            newStateListMe = [self.challenges[0]]
            newStateListEl = self.challenges[1].findStates(maxtime, self.challenges[0].visited + self.challenges[1].visited)

        newStateList = [None] * (len(newStateListMe)*len(newStateListEl))
        i = 0

        for MeState in newStateListMe:
            for ElState in newStateListEl:
                if MeState.location == ElState.location:
                    continue

                challenge = State2((MeState.location, ElState.location),
                                       (MeState.time, ElState.time),
                                       (MeState.route, ElState.route),
                                       (MeState.visited, ElState.visited),
                                       (MeState.score, ElState.score),
                                       (MeState.rate, ElState.rate)
                                      )
                newStateList[i] = challenge
                i+=1

        return newStateList[:i]

    def calculateRoute(self, maxtime):
        return State(route=self.challenges[0].route).calculateRoute(maxtime) + \
               State(route=self.challenges[1].route).calculateRoute(maxtime)

    def getEndScore(self, maxtime):
        return sum(x.getEndScore(maxtime) for x in self.challenges)

    def getTime(self):
        return (self.challenges[0].time + self.challenges[1].time) / 2

    def strRoute(self, route):
        return "".join(x for x in route)

    def __str__(self):
        return f"Ch2: {[l.location for l in self.challenges]} | {[l.score for l in self.challenges]} | {[l.visited for l in self.challenges]}\n   {self.strRoute(self.challenges[0].route)}\n   {self.strRoute(self.challenges[1].route)}"

    @classmethod
    def prune(cls, maxtime, newStateList):
        # Score each route
        statesScore = []
        for state in newStateList:
            statesScore.append((state.getEndScore(maxtime), state))

        statesScore = sorted(statesScore, key=lambda x: x[0], reverse=True)
        stateList = []

        # Keep the best routes // 500000 is found by trail and error
        for s in statesScore[:500000]:
            stateList.append(s[1])

        print(f"Prune: {len(newStateList)} -> {len(stateList)}")

        return stateList


class Challenge1(AoCLibChallenge):
    ChallengeNr = 1
    def setup(self):
        for line in self.inData:
            res = re.match(r"Valve ([A-Z]{2})[a-z\ ]*=([0-9]{1,3});[a-z\ ]*([A-Z,\ ]*)", line)
            Valve(res[1], int(res[2]), res[3].split(", "))

        for v in ValveList.values():
            v.linkValves()
        for v in ValveList.values():
            v.getDepthToAll()

    def run(self, statecls=State, maxtime=30):
        i = 0
        stateList = [statecls()]
        outputRoutes = []

        while len(stateList):
            newStateList = []
            print(f"Permutation {i} / {len(stateList)} states / average length {sum(x.getTime() for x in stateList)/len(stateList)}")
            i+=1
            j = 0

            while len(stateList):
                j+= 1
                if j % 10000 == 0:
                    print(f"{len(stateList):8d} remaining\u001b[1A")

                state = stateList.pop(0)

                newStates = state.findStates(maxtime)

                if len(newStates) == 0:
                    outputRoutes.append( state )

                newStateList.extend( newStates )

            stateList = statecls.prune(maxtime, newStateList)

        # Find best route
        bestRoute = (0, 0)

        for i in range(len(outputRoutes)):
            s = outputRoutes[i].calculateRoute(maxtime)

            if s > bestRoute[0]:
                bestRoute = (s, i)

        print(f"bestRoute: {bestRoute}\n{outputRoutes[bestRoute[1]]}")
        # print(f" {[x.route for x in outputRoutes[bestRoute[1]]]}")

class Challenge2(Challenge1):
    ChallengeNr = 2
    def run(self, statecls=State2, maxtime=26):
        return super().run(statecls, maxtime)

