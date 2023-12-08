import sys
from pathlib import Path

from AdventOfCode.AoCLib import buildC, runC_Challenge

cwd = Path(__file__).parents[0]

buildC(cwd, "AoCDay.c")

challenges = [runC_Challenge(1, cwd), runC_Challenge(2, cwd)]
