from constraintGraph import Variable, Constraint, renderGraph
from dfs import dfs_solve1

def run_csp(values: list, results_limit: int = None, upper_limit: int = None, lower_limit: int = None) -> list:
    if values is None:
        return None

    domain = [1, 0]
    variables = []
    for i in range(0, 10):
        variables.append(Variable("X" + str(i), domain=domain))
        variables.append(Variable('V' + str(i), [values[i]]))

    # if results_limit is None:
    #     results_limit = 10
    if upper_limit is None:
        upper_limit = 101
    if lower_limit is None:
        lower_limit = -1
    constraint = []

    # constraint.append(Constraint([variables[i] for i in range(0, 20, 2)],
    #                              lambda a, b, c, d, e, f, g, h, j, m:
    #                              a + b + c + d + e + f + g + h + j + m <= results_limit,
    #                              f"sum(X0, ... ,X9) <= {results_limit}"
    #                              )
    #                   )
    j = 0
    for i in range(0, 20, 2):
        constraint.append(Constraint([variables[i], variables[i + 1]],
                                     lambda x, y:
                                     (lower_limit <= y <= upper_limit and x == 1) or (not (lower_limit <= y <= upper_limit) and x == 0),
                                     f"{lower_limit} <= X{j}*{values[j]} <= {upper_limit}"))
        j += 1
    csp = renderGraph(variables, constraint)
    results: dict = dfs_solve1(csp)

    return (csp.variables, results)


def times_le(x, y, z):
    mul = x * y
    return mul <= z


def times_ge(x, y, z):
    mul = x * y
    return mul >= z
