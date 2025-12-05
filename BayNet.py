import random

class Node:
    def __init__(self, cpt, dependants):
        self.dependants = dependants
        if(len(dependants) == 0):
            self.cpt = {(): cpt[0]}
        if(len(dependants) == 1):
            self.cpt = {
                (True): cpt[0],
                (False): cpt[1]
            }
        if(len(dependants)== 2):
            self.cpt = {
                (True, True): cpt[0],
                (True, False): cpt[1],
                (False, True): cpt[2],
                (False, False): cpt[3]
            }


class BayNet:

    all_vars = ["B", "E", "A", "J", "M"]

    Nodes = {
        "B" : Node([.001],  []),
        "E" : Node([.002], []),
        "A" : Node([.70, .01, .70, .01], ["B", "E"]),
        "J" : Node([.90, .05], ["A"]),
        "M" : Node([.70, .01], ["A"])
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