from itertools import product
from optilog.solvers.sat import Glucose41
from optilog.modelling import *


def c(i, j, v):
    return Bool(f"C_{i}_{j}_{v}")


cells = [
    # 0 -> empty cell
    [0, 5, 2, 0, 0, 6, 0, 0, 0],
    [1, 6, 0, 9, 0, 0, 0, 0, 4],
    [0, 4, 9, 8, 0, 3, 6, 2, 0],
    [4, 0, 0, 0, 0, 0, 8, 0, 0],
    [0, 8, 3, 2, 0, 1, 5, 9, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 2],
    [0, 9, 7, 3, 0, 5, 2, 4, 0],
    [2, 0, 0, 0, 0, 9, 0, 5, 6],
    [0, 0, 0, 1, 0, 0, 9, 7, 0],
]
n_rows, n_cols = (len(cells), len(cells[0]))
region_size = 3
numbers = list(range(1, 10))

p = Problem()

for i, j in product(range(n_rows), range(n_cols)):
    p.add_constr(Add([c(i, j, v) for v in numbers]) == 1)

    if cells[i][j] != 0:
        p.add_constr(c(i, j, cells[i][j]))


for i in range(n_rows):
    for v in numbers:
        vars = [c(i, j, v) for j in range(n_cols)]
        p.add_constr(Add(vars) == 1)

for j in range(n_cols):
    for v in numbers:
        vars = [c(i, j, v) for i in range(n_rows)]
        p.add_constr(Add(vars) == 1)

for div_i in range(n_rows // region_size):
    for div_j in range(n_cols // region_size):
        start_i = div_i * region_size
        start_j = div_j * region_size

        cells = [
            (i + start_i, j + start_j)
            for i in range(region_size)
            for j in range(region_size)
        ]

        for v in numbers:
            vars = [c(i, j, v) for (i, j) in cells]
            p.add_constr(Add(vars) == 1)


def visualize(interp):
    cells = {v.name for v in interp if isinstance(v, Bool)}

    row_separator = (
        "." + ".".join(["-" * (region_size * 2 + 1)] * (n_cols // region_size)) + "."
    )
    print(row_separator)
    for i in range(n_rows):
        row_content = "| "
        for j in range(n_cols):
            for v in numbers:
                if c(i, j, v).name in cells:
                    row_content += str(v)
            if j % region_size == region_size - 1:
                row_content += " | "
            else:
                row_content += " "
        print(row_content)
        if i % region_size == region_size - 1:
            print(row_separator)


cnf = p.to_cnf_dimacs()

s = Glucose41()
s.add_clauses(cnf.clauses)
assert s.solve(), "Unsatisfiable formula"

model = cnf.decode_dimacs([l for l in s.model() if l > 0])

print(model)
visualize(model)
