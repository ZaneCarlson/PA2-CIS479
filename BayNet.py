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


    def prior(evidenceVars: Dict[str, bool], queryVars: List[str], num_samples: int):
        B_count_true = 0
        B_count_false = 0
        E_count_true = 0
        E_count_false = 0
        A_count_true = 0
        A_count_false = 0
        J_count_true = 0
        J_count_false = 0
        M_count_true = 0
        M_count_false = 0

        prob_sums = {q: 0.0 for q in queryVars}

        for x in range(10):
            query_true_counts = {q: 0 for q in
            queryVars}  # counts only for the query variables, conditioned on evidence
            kept_samples = 0  # samples that match the evidence
            num = 0


            # Run through the BayNetwork num_samples times
            while num < num_samples:
                # Burglary
                B_true = BayNet.Nodes["B"].cpt[()]
                rand = round(random.random(), 4)
                if rand < B_true:
                    B_value = True
                    B_count_true += 1
                else:
                    B_value = False
                    B_count_false += 1


                # Earthquake
                E_true = BayNet.Nodes["E"].cpt[()]
                rand = round(random.random(), 4)
                if rand < E_true:
                    E_value = True
                    E_count_true += 1
                else:
                    E_value = False
                    E_count_false += 1


                # Alarm
                A_true = BayNet.Nodes["A"].cpt[(B_value, E_value)]
                rand = round(random.random(), 4)
                if rand < A_true:
                    A_value = True
                    A_count_true += 1
                else:
                    A_value = False
                    A_count_false += 1


                # JohnCalls
                J_true = BayNet.Nodes["J"].cpt[A_value,]
                rand = round(random.random(), 4)
                if rand < J_true:
                    J_value = True
                    J_count_true += 1
                else:
                    J_value = False
                    J_count_false += 1


                # MaryCalls
                M_true = BayNet.Nodes["M"].cpt[A_value,]
                rand = round(random.random(), 4)
                if rand < M_true:
                    M_value = True
                    M_count_true += 1
                else:
                    M_value = False
                    M_count_false += 1

                # for da sampling! Reject if no likely
                sample = {
                    "B": B_value,
                    "E": E_value,
                    "A": A_value,
                    "J": J_value,
                    "M": M_value
                }

                # check if this sample matches the evidenceVars dict
                matches_evidence = True
                if evidenceVars is not None:
                    for var, val in evidenceVars.items(): # var is "A", "B", "J"; val is True/False
                        if sample[var] != val:
                            matches_evidence = False
                            break

                # if it doesn't match evidence, skip using this sample for queries
                if not matches_evidence:
                    num += 1
                    continue

                # this sample matches the evidence, keep it
                kept_samples += 1

                # update counts for query variables only, from this sample
                for q in queryVars:
                    if sample[q] is True:
                        query_true_counts[q] += 1

                num += 1



            # Compute probabilities for THIS RUN :)))
            if kept_samples > 0:
                run_probs = {q: query_true_counts[q] / kept_samples for q in queryVars}
            else:
                run_probs = {q: 0.0 for q in queryVars}

            # Add to total sum
            for q in queryVars:
                prob_sums[q] += run_probs[q]

        # average over 10 runs, to the 4th decimal place
        avg_probs = {q: round(prob_sums[q] / 10, 4) for q in queryVars}


        print(f"B_count_true: {B_count_true}")
        print(f"B_count_false: {B_count_false}")
        print(f"E_count_true: {E_count_true}")
        print(f"E_count_false: {E_count_false}")
        print(f"A_count_true: {A_count_true}")
        print(f"A_count_false: {A_count_false}")
        print(f"J_count_true: {J_count_true}")
        print(f"J_count_false: {J_count_false}")
        print(f"M_count_true: {M_count_true}")
        print(f"M_count_false: {M_count_false}")
        print("")

        print(avg_probs)

        return avg_probs




    def Rejection(evidenceVars, queryVars):
        return


    def LW(evidenceVars, queryVars):
        return



if __name__ == "__main__":
    evidenceVars = {"A": True, "B": False}
    queryVars = ["J"]
    conv = input("input sample size: ")
    num_samp = int(conv)

    BayNet.prior(evidenceVars, queryVars, num_samp)