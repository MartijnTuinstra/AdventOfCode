from AdventOfCode.AoCLib import AoCLibChallenge

pipes = {
  '|': [0+1j, 0-1j],
  '-': [-1, 1],
  'L': [-1j, 1],
  'J': [-1j, -1],
  '7': [1j, -1],
  'F': [1j, 1],
  '.': []
}

t = [-1, -1-1j, -1j, 1-1j, 1, 1+1j, 1j, -1+1j]

pipe_boundaries = {
  k: [x/2 for x in t if x not in v] for k, v in pipes.items()
}

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        self.inDataTo2D()

    def findLoop(self, location, direction):
        nextLocation = location + direction
        loop = []

        while nextLocation != location:
            pipe = self.inData.getLocation(int(nextLocation.real),
                    int(nextLocation.imag))

            if pipe == '':
                return False, []

            loop.append(nextLocation)

            pipe_connections = [x for x in pipes[pipe] if x+direction != 0]

            if len(pipe_connections) != 1:
                return False, []

            direction = pipe_connections[0]
            nextLocation = nextLocation + direction

        return True, loop

    def run(self):
        start_location = -1-1j
        
        for (x, y), value in self.inData:
            if value == 'S':
                start_location = complex(x, y)
                break

        found = False
        loop = []
        for d in [1, 1j, -1, -1j]:
            found, loop = self.findLoop(start_location, d)

            if found:
                break

        for k, v in pipes.items():
            connecting = 0
            for d in v:
                newloc = start_location + d
                if newloc == loop[0] or newloc == loop[-1]:
                    connecting += 1

            if connecting == 2:
                self.inData.setLocation(int(start_location.real), int(start_location.imag), k)

                break


        loop = [start_location] + loop + [start_location]

        print(f"Farthest point: {len(loop)//2}")
        return loop


class Challenge2(Challenge1):
    ChallengeNr = 2

    def findRegion(self, start, loop, loopboundary, otherRegions):
        stack = [start]
        visited = []
        max_iter = 0

        while len(stack) and max_iter < 1000000:
            max_iter += 1

            if max_iter % 1000 == 0:
                print(f"{max_iter}, stack: {len(stack)}, visited: {len(visited)}")


            loc = stack.pop(0)

            visited.append(loc)

            if int(loc.real) != loc.real or int(loc.imag) != loc.imag:
                # tile in between
                for delta in t:
                    delta /= 2

                    newloc = loc+delta

                    if newloc in visited or newloc in stack:
                        continue

                    if newloc in loopboundary:
                        stack.append(newloc)
                    elif int(newloc.real) == newloc.real or \
                            int(newloc.imag) == newloc.imag:
                        tile = self.inData.getLocation(int(newloc.real),int(newloc.imag))

                        if tile == '.':
                            stack.append(newloc)
                continue


            for d in [-1, -1j, 1, 1j]:
                newLoc = loc + d

                if newLoc in visited:
                    continue
                tile = self.inData.getLocation(int(newLoc.real),
                        int(newLoc.imag))

                new_dirs = []
                new_dirs_search = []
                new_outside = []
                if tile == '':
                    continue
                elif tile == '.' or newLoc not in loop:
                    new_dirs_search = [1, 1j, -1, -1j]
                    new_outside = [1, 1j, -1, -1j]
                else:
                    continue

                for d2 in new_dirs_search:
                    if d + d2 == 0:
                        continue

                    if newLoc + d2 in visited or \
                       newLoc + d2 in otherRegions:
                        continue


                    if newLoc + d2 in loop and \
                       newLoc + (d2/2) not in visited and \
                       newLoc + (d2/2) not in stack:
                        stack.append(newLoc + (d2/2))
                        continue


                    new_dirs.append(d2)


                if newLoc not in stack:
                    stack.append(newLoc)

        return visited


    def run(self):
        loop = super().run()

        print(pipe_boundaries)


        loopboundary = []
        for loc in loop:
            tile = self.inData.getLocation(int(loc.real), int(loc.imag))
            if tile == 'S':
                continue
            loopboundary.extend([loc+x for x in pipe_boundaries[tile]])

        loopboundary = list(set(loopboundary))
        loops = []

        it = 0

        while len(loopboundary):
            my_loop = [loopboundary.pop(0)]

            stack = [my_loop[0]]

            print("Next loop")

            while len(stack):
                it += 1

                if it % 1000 == 0:
                    print(it)

                loc = stack.pop(0)

                my_loop.append(loc)

                for x in t:
                    newloc = loc + (x/2)

                    try:
                        ix = loopboundary.index(newloc)
                        stack.append(loopboundary.pop(ix))
                    except ValueError:
                        pass

            loops.append(my_loop)

        for x in range(len(loops)):
            loops[x] = [y for y in loops[x] if (int(y.real) == y.real) ^ (int(y.imag) == y.imag)]

        regions = []
        allRegions = []
        
        for l in loops:
            tmp = []
            for x in l:
                for y in [-0.5, -0.5j, 0.5, 0.5j]:
                    newloc = x+y
                    if not ((int(newloc.real) == newloc.real) or \
                            (int(newloc.imag) == newloc.imag)):
                        continue
                    elif newloc in loop:
                        continue
                    elif newloc in tmp:
                        continue

                    tmp.append(newloc)

            regions.append(tmp)
            allRegions.extend(tmp)


        for r in range(len(regions)):
            newlocations = [x for x in regions[r]]

            it = 0
            while len(newlocations):
                loc = newlocations.pop(0)
                it += 1

                for d in [-1, -1j, 1, 1j]:
                    newloc = loc + d

                    if newloc.real < 0 or newloc.real >= self.inData.width or \
                       newloc.imag < 0 or newloc.imag >= self.inData.height:
                        continue

                    if newloc in loop:
                        continue

                    elif newloc in regions[r]:
                        continue

                    elif newloc not in newlocations:
                        regions[r].append(newloc)
                        newlocations.append(newloc)


        for l in loops:
            print(l)
        """
        tiles = self.inData.width * self.inData.height



        for (y, x), value in self.inData:
            if complex(x, y) not in loop and complex(x,y) not in allRegions:
                print(f"search {complex(x,y)}")
                region = self.findRegion(complex(x,y), loop, loopboundary, allRegions)
                allRegions.extend(region)
                regions.append(region)

                print(f"==============================================\n")

        for r in range(len(regions)):
            regions[r] = list(set([x for x in regions[r] if int(x.real) == x.real and int(x.imag) == x.imag]))
            print(regions[r])
        print(set([x for x in allRegions if int(x.real) == x.real and int(x.imag) == x.imag]))

        """
        """
        while len(stack) and max_iter >= 0:
            max_iter -= 1
            loc = stack.pop(0)

            print(f"Visit {loc}", end="")

            search_dir = stack_directions[loc]
            del stack_directions[loc]

            outside = stack_outside[loc]
            del stack_outside[loc]

            visited.append(loc)

            print(f"\tsearch: {search_dir}\toutside: {outside}")

            for d in search_dir:
                newLoc = loc + d

                if newLoc in visited:
                    continue

                tile = self.inData.getLocation(int(newLoc.real),
                        int(newLoc.imag))

                new_dirs = []
                new_dirs_search = []
                new_outside = []
                if tile == '':
                    continue
                elif tile == '.' or newLoc not in loop:
                    new_dirs_search = [1, 1j, -1, -1j]
                    new_outside = [1, 1j, -1, -1j]
                elif newLoc in loop:
                    new_dirs_search = [x for x in pipes[tile] if x+d != 0]
                    new_outside = list(set([-1*d] + pipes[tile]))
                    print(f"  route appends")


                for d2 in new_dirs_search:
                    if d + d2 == 0:
                        continue

                    if newLoc + d2 in visited:
                        continue

                    new_dirs.append(d2)


                if newLoc not in stack:
                    stack.append(newLoc)
                    stack_directions[newLoc] = new_dirs
                    stack_outside[newLoc] = new_outside
                else:
                    stack_directions[newLoc] = list(set(stack_directions[newLoc] + new_dirs))
                    stack_outside[newLoc] = list(set(stack_outside[newLoc] + new_outside))



                print(f" new stack: {stack}")
        """

        letter = "0123456789ABCDEGHKMNPQRSTUVWXYZ"

        i = 0
        for region in range(len(regions)):
            regionId = i if len(regions[region]) > 1 else len(letter)-1
            print(f"Region {regionId}: has size {len(regions[region])}")

            for comp in regions[region]:
                self.inData.setLocation(int(comp.real), int(comp.imag), letter[regionId])

            if len(regions[region]) > 1:
                i += 1

        for y in range(self.inData.height):
            print("")
            for x in range(self.inData.width):
                loc = self.inData.getLocation(x, y)
                if complex(x,y) in loop:
                    print(f"\033[0;31m{loc}\033[0m", end="")
                elif complex(x,y) in allRegions:
                    try:
                        print(f"\033[0;3{(2+letter.index(loc)%6)}m{loc}\033[0m", end="")
                    except ValueError:
                        print(f"\033[0;41m{loc}\033[0m", end="")
                else:
                    print(loc, end="")
