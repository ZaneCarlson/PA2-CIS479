import itertools
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
        return Q_normalized
    

    

    def prior(evidenceVars, queryVars):
        return


    def Rejection(evidenceVars, queryVars):
        return


    def LW(evidenceVars, queryVars):
        return
