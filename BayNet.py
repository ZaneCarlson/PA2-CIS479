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


        

    def exact_inference(evidenceVars, queryVars):
        return


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