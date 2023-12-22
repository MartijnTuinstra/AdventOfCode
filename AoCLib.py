import timeit
import sys

from collections import namedtuple
from pathlib import Path
from subprocess import Popen, PIPE
from selectors import DefaultSelector, EVENT_READ

class Arr2D:
    def __init__(self, data):
        self.data = data

        self.sizecls = namedtuple("ArraySize", "height width")
        self.size = self.sizecls(len(self.data), len(self.data[0]))
        self.height = len(self.data)
        self.width = len(self.data[0])

        self.loc = (0, 0)

    def getLocation(self, x, y=0):
        if isinstance(x, complex):
            y = int(x.imag)
            x = int(x.real)

        if x < 0 or y < 0:
            return ''
        elif x >= self.width or y >= self.height:
            return ''

        return self.data[y][x]
    def setLocation(self, x, y, value):
        if x < 0 or y < 0:
            print(f" Cannot set location {x}:{y}")
            return ''
        elif x >= self.width or y >= self.height:
            print(f" Cannot set location {x}:{y}")
            return ''

        self.data[y][x] = value

    def __len__(self):
        return self.size

    def __getitem__(self, index):
        return self.data[index]

    def __iter__(self):
        self.loc = (0, 0)
        return self

    def __next__(self):
        result = ((self.loc[0], self.loc[1]), self.getLocation(*self.loc))

        self.loc = (self.loc[0], self.loc[1]+1)

        if self.loc[1] >= len(self.data[0]):
            self.loc = (self.loc[0]+1, 0)

        if self.loc[0] >= len(self.data):
            raise StopIteration

        return result

    def print_with_highlight(self, func):
        for y in range(self.height):
            for x in range(self.width):
                if func(x, y):
                    print(f"\u001b[31m{str(self.data[y][x])}\u001b[0m", end="")
                else:
                    print(str(self.data[y][x]), end="")
            print()

    def __repr__(self):
        s = ""

        for row in self.data:
            for c in row:
                s += str(c)
            s+= "\n"

        s = s[:-1]
        return s

def AoCLoad(path):
    lines = []
    with open(path, "r") as f:
        lines = f.read().splitlines()

    return lines

def executeProcess(cmdlist):
    print("Run "+str(cmdlist))
    process = Popen(cmdlist,
                    stdout=PIPE,
                    stderr=PIPE,
                    universal_newlines=True)

    sel = DefaultSelector()
    sel.register(process.stdout, EVENT_READ)
    sel.register(process.stderr, EVENT_READ)

    ok = True
    pipes = 2

    while ok:
        for pipe, _ in sel.select():
            line = pipe.fileobj.readline()
            if not line:
                sel.unregister(pipe.fileobj)
                pipes -= 1

                if pipes == 0:
                    ok = False
                    break

            if pipe.fileobj == process.stderr:
                print("\033[0;31m" + line + "\033[0m", file=sys.stderr, end="")
            else:
                print(line, end="")

    return_code = process.poll()
    print('RETURN CODE', return_code)

def buildC(directory, infile):
    outfile = directory / "AoCDay"

    print(f"Building {directory / infile} -> {directory / outfile}")

    executeProcess(['gcc', f'{directory / infile}', f"-I{Path(__file__).parents[0]}", '-o', f'{directory / outfile}'])


class AoCLibChallenge:
    def execute(self, path):
        self.inData = AoCLoad(path)

        t = timeit.timeit( stmt=self.run, setup=self.setup, number=1 )

        print(f"Time taken to execute Challenge {self.ChallengeNr}: {t}")

    def inDataTo2D(self, elementFunc=lambda x: x, rowFunc=lambda y: y, arrcls=Arr2D):
        data = [rowFunc([elementFunc(x) for x in r]) for r in self.inData]
        self.inData = arrcls(data)

    def inDataTo1D_Grouped(self, elementFunc=lambda x: x, rowFunc=lambda y: y):
        data = []
        tmp = []

        for line in self.inData:
            if line == "":
                data.append(tmp)
                tmp = []
                continue

            tmp.append(line)

        data.append(tmp)

        self.inData = data


class runC_Challenge:
    def __init__(self, nr, runlocation):
        self.ChallengeNr = nr
        self.runfile = runlocation / "AoCDay"

    def execute(self, inpath):
        executeProcess([str(self.runfile), str(self.ChallengeNr), str(inpath)])
