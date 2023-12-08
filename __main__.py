import importlib
import sys
from pathlib import Path
import argparse

from AdventOfCode.Y2022.D16 import Challenge1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-T", "--test", action='store_true')

    parser.add_argument("-E", "--easy", action='store_true')
    parser.add_argument("-H", "--hard", action='store_true')

    parser.add_argument("year", type=int)
    parser.add_argument("day", type=int)

    args = parser.parse_args()

    challenge_module = None
    try:
        challenge_module = importlib.import_module(f"AdventOfCode.Y{args.year:04d}.D{args.day:02d}")
    except ImportError as e:
        # Display error message
        print(e)

    basepath = Path.cwd() / "AdventOfCode" / f"Y{args.year:04d}" / f"D{args.day:02d}"

    if not args.test:
        fileloc = basepath / "myinput.txt"
    else:
        fileloc = basepath / "input.txt"

    if args.easy:
        challenge_module.challenges[0].execute(str(fileloc))
        exit()

    if args.hard:
        challenge_module.challenges[1].execute(str(fileloc))
        exit()


    for challenge in challenge_module.challenges:
        challenge.execute(str(fileloc))
