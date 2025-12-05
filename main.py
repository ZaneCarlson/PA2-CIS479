import BayNet


queryVars = ["B", "J"]

result = BayNet.BayNet.enumerateAsk({"A": False}, queryVars)

print(result)