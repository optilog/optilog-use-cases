from optilog.modelling import Bool, Add, Problem
from optilog.solvers.sat import Glucose41

n = 8


def q(i, j):
    return Bool(f"Q_{i}_{j}")


p = Problem()

for i in range(n):
    queens = [q(i, j) for j in range(n)]
    p.add_constr(Add(queens) == 1)

for j in range(n):
    queens = [q(i, j) for i in range(n)]
    p.add_constr(Add(queens) == 1)

for i in range(n):
    diagonal_down = [(i + di, di) for di in range(n - i)]
    diagonal_up = [(i - di, di) for di in range(i)]
    mirror_diagonal_down = [(i, n - j - 1) for (i, j) in diagonal_down]
    mirror_diagonal_up = [(i, n - j - 1) for (i, j) in diagonal_up]

    all_diagonals = (
        diagonal_down,
        diagonal_up,
        mirror_diagonal_down,
        mirror_diagonal_up,
    )

    for diagonal in all_diagonals:
        if len(diagonal) <= 1:
            continue
        vars = [q(i, j) for i, j in diagonal]
        p.add_constr(Add(vars) <= 1)


def visualize(n, interp):
    queens = {v.name for v in interp if isinstance(v, Bool)}

    print("-" * (3 * n + 1))
    for i in range(n):
        print("|", end="")
        for j in range(n):
            if q(i, j).name in queens:
                print(" Q", end="|")
            else:
                print("  ", end="|")
        print("")
        print("-" * (3 * n + 1))


cnf = p.to_cnf_dimacs()

s = Glucose41()
s.add_clauses(cnf.clauses)

assert s.solve(), "Unsatisfiable formula"

model = s.model()
model = cnf.decode_dimacs([lit for lit in model if lit > 0])

print(model)
visualize(n, model)
