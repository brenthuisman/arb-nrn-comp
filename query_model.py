import sys
import dbbs_models

model = getattr(dbbs_models, sys.argv[1])
cell = model()

type_alias = {
    "s": "soma",
    "d": "dendrites",
    "a": "axon",
    "aa": "ascending_axon",
    "pf": "parallel_fiber",
}

queries = sys.argv[1:]
for query in queries:
    types, asks = query.split(":")
    sections = list(s for s in cell.sections if any(t in s.labels for t in types))
    if "L" in asks:
        print("Length of", types, len(sections))
    if "M" in asks:
        print(
            "Mechanism dict of",
        )
