import random
import itertools
import re
from typing import List, Dict

class Node:
    def __init__(self, cpt, label, parents):
        self.label = label
        self.parents = parents
        num_parents = len(parents)

        if num_parents == 0:
            self.cpt = {(): cpt[0]}

        elif num_parents == 1:
            self.cpt = {
                (True,):  cpt[0],
                (False,): cpt[1]
            }

        elif num_parents == 2:
            self.cpt = {
                (True,  True):  cpt[0],
                (True,  False): cpt[1],
                (False, True):  cpt[2],
                (False, False): cpt[3]
            }

        else:
            raise ValueError("Only supports up to 2 parents")


class BayNet:

    all_vars = ["B", "E", "A", "J", "M"]

    Nodes = {
        "B" : Node([.001], "B", []),
        "E" : Node([.002], "E", []),
        "A" : Node([.70, .01, .70, .01], "A", ["B", "E"]),
        "J" : Node([.90, .05], "J", ["A"]),
        "M" : Node([.70, .01], "M", ["A"])
    }


    def P(V, value, e):
        node = BayNet.Nodes[V]
        parent_values = tuple(e[p] for p in node.parents)

        if value:
            return node.cpt[parent_values]
        else: 
            return 1 - node.cpt[parent_values]


    def getEnumeration(vars: List[str]):
        result = []
        domains = {var: [True, False] for var in vars}

        for assignment in itertools.product(*[domains[v] for v in vars]):
            result.append(dict(zip(vars, assignment)))
        return result
        

    def enumerateAll(vars: list, e: dict) -> float:
        if(len(vars) == 0):
            return 1.0
        
        V = vars[0]
        rest = vars[1:]

        if V in e:
            return BayNet.P(V, e[V], e) * BayNet.enumerateAll(rest, e)
        else:
            prob = 0
            for v in [True, False]:
                e_extended = {**e, V: v}
                prob += BayNet.P(V, v ,e_extended) * BayNet.enumerateAll(rest, e_extended)
            return prob

        



    def enumerateAsk(evidenceVars: Dict[str, bool], queryVars: List[str]):
        Q = {}
        enumeration = BayNet.getEnumeration(queryVars)
        for state in enumeration:
        
            exi = {**evidenceVars, **state}
            Q[tuple(state.items())] = BayNet.enumerateAll(BayNet.all_vars, exi)
        
        total = sum(Q.values())
        for key in Q:
            Q[key] /= total

        Q_normalized = {}
        for k, v in Q.items():
            Q_normalized[tuple(k)] = v

        true_state = tuple((var, True) for var in queryVars)
        value = Q_normalized.get(true_state, None)
        print(value)
        return Q_normalized

    def generateSample():
        # Burglary
        B_value = False
        E_value = False
        A_value = False
        J_value = False
        M_value = False

        B_true = BayNet.Nodes["B"].cpt[()]
        rand = round(random.random(), 4)
        if rand < B_true:
            B_value = True
        else:
            B_value = False


        # Earthquake
        E_true = BayNet.Nodes["E"].cpt[()]
        rand = round(random.random(), 4)
        if rand < E_true:
            E_value = True
        else:
            E_value = False


        # Alarm
        A_true = BayNet.Nodes["A"].cpt[(B_value, E_value)]
        rand = round(random.random(), 4)
        if rand < A_true:
            A_value = True
        else:
            A_value = False


        # JohnCalls
        J_true = BayNet.Nodes["J"].cpt[A_value,]
        rand = round(random.random(), 4)
        if rand < J_true:
            J_value = True
        else:
            J_value = False


        # MaryCalls
        M_true = BayNet.Nodes["M"].cpt[A_value,]
        rand = round(random.random(), 4)
        if rand < M_true:
            M_value = True
        else:
            M_value = False

        # for da sampling! Reject if no likely
        sample = {
            "B": B_value,
            "E": E_value,
            "A": A_value,
            "J": J_value,
            "M": M_value
        }
        return sample

    def prior(evidenceVars: Dict[str, bool], queryVars: List[str], num_samples: int):
        result = 0
        for x in range(10):
            samples = []
            usedSamples = []
            while(len(samples) < num_samples):
                samples.append(BayNet.generateSample())              

            for sample in samples:
                if all(sample[var] == evidenceVars[var] for var in evidenceVars):
                    usedSamples.append(sample)

            matches = 0
            for sample in usedSamples:
                if all(sample[var] is True for var in queryVars):
                    matches += 1
            if(len(usedSamples) > 0):
                result += matches/len(usedSamples)
        result /= 10

        print(f"P({queryVars} | {evidenceVars} ) = {result}")
        return result

    def Rejection(evidenceVars: Dict[str, bool], queryVars: List[str], num_samples: int):
        result = 0
        for x in range(10):
            samples = []
            usedSamples = []
            while(len(samples) < num_samples):
                sample = BayNet.generateSample()
                if all(sample[var] == evidenceVars[var] for var in evidenceVars):
                    samples.append(sample)   
                   # print(sample["A"])
                    #print(len(samples))
            

            matches = 0
            for sample in samples:
                if all(sample[var] == True for var in queryVars):
                    matches += 1
        
            result += matches/len(samples)

        result /= 10

        print(f"P({queryVars} | {evidenceVars} ) = {result}")
        return result
        

    def generateLWSample(evidenceVars: Dict[str, bool]):
        sample = {}
        weight = 1.0

        B_prob = BayNet.Nodes["B"].cpt[()]
        if "B" in evidenceVars:
            sample["B"] = evidenceVars["B"]
            weight *= B_prob if sample["B"] else (1 - B_prob)
        else:
            sample["B"] = (random.random() < B_prob)

        E_prob = BayNet.Nodes["E"].cpt[()]
        if "E" in evidenceVars:
            sample["E"] = evidenceVars["E"]
            weight *= E_prob if sample["E"] else (1 - E_prob)
        else:
            sample["E"] = (random.random() < E_prob)
        
        A_prob = BayNet.Nodes["A"].cpt[(sample["B"], sample["E"])]
        if "A" in evidenceVars:
            sample["A"] = evidenceVars["A"]
            weight *= A_prob if sample["A"] else (1 - A_prob)
        else:
            sample["A"] = (random.random() < A_prob)

        J_prob = BayNet.Nodes["J"].cpt[(sample["A"],)]
        if "J" in evidenceVars:
            sample ["J"] = evidenceVars["J"]
            weight *= J_prob if sample["J"] else (1 - J_prob)
        else:
            sample["J"] = (random.random() < J_prob)

        M_prob = BayNet.Nodes["M"].cpt[(sample["A"],)]
        if "M" in evidenceVars:
            sample ["M"] = evidenceVars["M"]
            weight *= M_prob if sample["M"] else (1 - M_prob)
        else:
            sample["M"] = (random.random() < M_prob)

        return (sample, weight)

    def lw(evidenceVars: Dict[str, bool], queryVars: List[str], num_samples: int): #TODO : finish the lw function
        result = 0.0

        for a in range(10):
            total_weight = 0.0
            match_weight = 0.0
            for x in range(num_samples):

                sample, weight = BayNet.generateLWSample(evidenceVars)
                total_weight += weight

                if all (sample[var] is True for var in queryVars):
                    match_weight += weight

            # just checking for div by zero even though it won't happen like ever
            if total_weight > 0:
                run_prob = match_weight / total_weight
            else:
                run_prob = 0.0

            result += run_prob

        result /= 10.0

        print(f"P({queryVars} | {evidenceVars}) = {result}")
        return result



def parse_input(input_str: str):
    """
    Parses input like: [< A, t >< B, f >][J, M]
    Returns: (evidenceVars: dict, queryVars: list)
    """

    # Extract the two bracketed groups
    m = re.match(r"\s*\[(.*?)\]\s*\[(.*?)\]\s*$", input_str)
    if not m:
        raise ValueError("Invalid input format")

    evidence_raw, query_raw = m.groups()

    # --- Evidence parsing ---
    # Matches things like < A, t >
    evidence_pairs = re.findall(r"<\s*([A-Za-z])\s*,\s*([tfTF])\s*>", evidence_raw)

    evidenceVars = {}
    for var, val in evidence_pairs:
        evidenceVars[var] = (val.lower() == "t")

    # --- Query parsing ---
    # Query is a list of variables separated by commas or whitespace
    queryVars = re.findall(r"[A-Za-z]", query_raw)

    return evidenceVars, queryVars

if __name__ == "__main__":

    conv = input("input sample size: ")
    num_samp = int(conv)

    while True:
        print("\nEnter query in format [< A, t >< B, f >][J, M]")
        print("Or type 'exit' to quit.")
        raw = input("Input: ").strip()

        if raw.lower() == "exit":
            break

        try:
            evidenceVars, queryVars = parse_input(raw)
        except Exception as e:
            print("Parse error:", e)
            continue

        print("\nParsed:")
        print("Evidence:", evidenceVars)
        print("Query:", queryVars)

        print("\n=== Exact ===")
        BayNet.enumerateAsk(evidenceVars, queryVars)

        print("\n=== Prior Sampling ===")
        BayNet.prior(evidenceVars, queryVars, num_samp)

        print("\n=== Rejection Sampling ===")
        BayNet.Rejection(evidenceVars, queryVars, num_samp)

        print("\n=== Likelihood Weighting ===")
        BayNet.lw(evidenceVars, queryVars, num_samp)