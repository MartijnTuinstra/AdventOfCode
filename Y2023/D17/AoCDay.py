from AdventOfCode.AoCLib import AoCLibChallenge

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        self.inDataTo2D(elementFunc=lambda x: int(x))

    def run(self):
        self.crucible_dijkstra(1, 3)


    def crucible_dijkstra(self, min_steps, max_steps):
        # Dijkstra algorithm
        #
        
        heat = {}
        stack = []
        for x in range(self.inData.width):
            for y in range(self.inData.height):
                heat[complex(x, y)] = [[0xFFFFFFFF]*(max_steps+1) for _ in range(4)]
                #stack.append((complex(x,y), 0))

        stack.append((complex(0,0), 0, 0, 1 )) # pos, loss, straight, RIGHT
        stack.append((complex(0,0), 0, 0, 1j)) # pos, loss, straight, DOWN

        end = complex(self.inData.width -1, self.inData.height -1)

        def dir_to_int(dir):
            if dir == complex( 1,  0): return 0
            if dir == complex(-1,  0): return 1
            if dir == complex( 0,  1): return 2
            if dir == complex( 0, -1): return 3

        def is_better(steps, position, loss, dir):
            current = heat[position][dir_to_int(dir)][steps-1]

            if loss < current:
                heat[position][dir_to_int(dir)][steps-1] = loss
                return True

            return False

        j = 0
        while len(stack):
            j += 1
            ix = 0
            for i in range(1, len(stack)):
                if stack[i][1] < stack[ix][1]:
                    ix = i

            pos, heatloss, steps, direction = stack.pop(ix)

            if j % 1000 == 0:
                print(f"{pos}, {heatloss}     ", end="\r")

            if pos == end:
                print(f"\n{pos}, {heatloss}")
                return

            # turn left or right (relative to direction)
            #  always <= max_step
            if steps >= min_steps:
                for turn_direction in (direction * 1j, direction * -1j):
                    new_loss = self.inData.getLocation(pos + turn_direction)

                    if new_loss == '':
                        continue

                    # step = 1, pos = pos + turn_direction, cost
                    # = heatloss+newcost, dir
                    if is_better(1, pos + turn_direction,
                                 heatloss + new_loss, turn_direction):
                        stack.append((pos + turn_direction, heatloss + new_loss, 1, turn_direction))

            if steps < max_steps:
                new_loss = self.inData.getLocation(pos + direction)

                if new_loss == '':
                    continue

                if is_better(steps+1, pos + direction, new_loss, direction):
                    stack.append((pos+direction, heatloss + new_loss, steps+1, direction))


class Challenge2(Challenge1):
    ChallengeNr = 2

    def setup(self):
        super().setup()

    def run(self):
        self.crucible_dijkstra(4, 10)
