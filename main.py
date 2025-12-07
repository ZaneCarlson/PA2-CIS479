import BayNet


queryVars = ["B", "E"]

result = BayNet.BayNet.enumerateAsk({"M": True, "J": False}, queryVars)

print(result)