import random
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
    

    

    def prior(evidenceVars = dict[str, bool], queryVars=None):

        # Burglary
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
        J_true = BayNet.Nodes["J"].cpt[A_value]
        rand = round(random.random(), 4)
        if rand < J_true:
            J_value = True
        else:
            J_value = False


        # MaryCalls
        M_true = BayNet.Nodes["M"].cpt[A_value]
        rand = round(random.random(), 4)
        if rand < M_true:
            M_value = True
        else:
            M_value = False


        # evidenceVars is a list of tuples
        for var in evidenceVars:



        return




    def Rejection(evidenceVars, queryVars):
        return


    def LW(evidenceVars, queryVars):
        return



if __name__ == "__main__":
    BayNet.prior()