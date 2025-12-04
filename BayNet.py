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


        

    def exact_inference(queryVars, evidenceVars):
        return


