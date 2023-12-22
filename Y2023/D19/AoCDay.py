from AdventOfCode.AoCLib import AoCLibChallenge

class Challenge1(AoCLibChallenge):
    ChallengeNr = 1

    def setup(self):
        split = self.inData.index('')

        self.workflow = {}
        self.parts = []

        for row in self.inData[:split]:
            name, rules = row.split("{")
            rules = rules[:-1]

            t_rules = rules.split(",")
            rules = []

            for rule in t_rules:
                if ":" in rule:
                    ineq, dest = rule.split(":")
                    rules.append((ineq[0], ineq[1], int(ineq[2:]), dest))
                    continue
                rules.append((None, None, None, rule))
           
            self.workflow[name] = rules

        print(self.workflow)

        for row in self.inData[split+1:]:
            row = row[1:-1].split(",")

            parameters = {}
            for elem in row:
                n, v = elem.split("=")

                parameters[n] = int(v)

            self.parts.append(parameters)

        print(self.parts)

    def run(self):

        acceptedparts = []

        for part in self.parts:

            workflow = self.workflow["in"]
            print(part)

            debug = "in "

            while workflow is not None:

                dest = None

                for r_p, r_eq, r_v, r_dest in workflow:
                    if r_eq == "<" and part[r_p] < r_v or \
                       r_eq == ">" and part[r_p] > r_v:
                        dest = r_dest
                        break
                    elif r_eq is None:
                        dest = r_dest

                debug += f"{dest} "

                if dest == "R":
                    # Rejected
                    print(debug)
                    break
                elif dest == "A":
                    # Accepted
                    print(debug)
                    acceptedparts.append(part)
                    break
                else:
                    workflow = self.workflow[dest]

        print(f"Accepted: {len(acceptedparts)}") 

        score = 0

        for part in acceptedparts:
            score += part['x'] + part['m'] + part['a'] + part['s']

        print(f"Score: {score}")

class Challenge2(Challenge1):
    ChallengeNr = 2

    def setup(self):
        super().setup()

    def run(self):
        
        superpart = {"x":[1, 4000], "m": [1, 4000], "a":[1, 4000], "s":[1, 4000]}
        acceptedparts = []

        stack = [("in", superpart)]

        while len(stack):
            wf, part = stack.pop()

            if wf == "A":
                acceptedparts.append(part)
                continue
            elif wf == "R":
                continue

            for r_p, r_eq, r_v, r_dest in self.workflow[wf]:
                newpart = {k:v for k,v in part.items()}

                if r_eq == "<" and part[r_p][0] < r_v:
                    if part[r_p][1] < r_v:
                        newpart = {k:[x for x in v] for k,v in part.items()}
                        stack.append((r_dest, newpart))
                    elif part[r_p][1] >= r_v:
                        newpart = {k:[x for x in v] for k,v in part.items()}
                        newpart[r_p][1] = r_v-1
                        stack.append((r_dest, newpart))
                        
                        part[r_p][0] = r_v

                elif r_eq == ">" and part[r_p][1] > r_v:
                    if part[r_p][0] > r_v:
                        newpart = {k:[x for x in v] for k,v in part.items()}
                        stack.append((r_dest, newpart))
                    elif part[r_p][0] <= r_v:
                        newpart = {k:[x for x in v] for k,v in part.items()}
                        newpart[r_p][0] = r_v+1
                        stack.append((r_dest, newpart))

                        part[r_p][1] = r_v

                elif r_eq is None:
                    stack.append((r_dest, part))

        print(acceptedparts)

        totalscore = 0

        for part in acceptedparts:
            score  = (part['x'][1] - part['x'][0] + 1)
            score *= (part['m'][1] - part['m'][0] + 1)
            score *= (part['a'][1] - part['a'][0] + 1)
            score *= (part['s'][1] - part['s'][0] + 1)

            totalscore += score

        print(f"Score: {totalscore}")
