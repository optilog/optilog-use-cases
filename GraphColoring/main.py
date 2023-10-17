from optilog.modelling import *
from optilog.solvers.sat import Glucose41

vertexes = [1, 2, 3, 4, 5, 6, 7, 8]
edges = [
    (1, 2),
    (1, 5),
    (2, 5),
    (2, 4),
    (3, 4),
    (3, 7),
    (4, 5),
    (4, 8),
    (4, 6),
    (5, 8),
    (6, 7),
    (6, 8),
]
colors = ["red", "green", "blue", "yellow"]


def x(v, c):
    return Bool(f"x_{v}_{c}")


p = Problem()
for v in vertexes:
    p.add_constr(Add([x(v, c) for c in colors]) == 1)

for c in colors:
    for v1, v2 in edges:
        p.add_constr(~(x(v1, c) & x(v2, c)))


cnf = p.to_cnf_dimacs()

s = Glucose41()
s.add_clauses(cnf.clauses)
assert s.solve(), "Unsatisfiable formula"

print(s.model())

model = cnf.decode_dimacs([l for l in s.model() if l > 0])
print(model)
