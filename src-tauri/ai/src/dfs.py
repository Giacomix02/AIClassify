

tab = "\t"
resultString = None
con_bbox = dict(boxstyle="square,pad=1.0", color="green")


def merge_two_dicts(x, y):
    z = x.copy()  # start with keys and values of x
    z.update(y)  # modifies z with keys and values of y
    return z


def dfs_solver(constraints, context: dict, var_order):
    """generator for all solutions to csp.
    context is an assignment of values to some of the variables.
    var_order  is  a list of the variables in csp that are not in context.
    """
    to_eval = {c for c in constraints if c.can_evaluate(context)}
    result = all(c.holds(context) for c in to_eval)
    if result:
        if var_order == []:
            yield context
        else:
            rem_cons = [c for c in constraints if c not in to_eval]
            var = var_order[0]
            for val in var.domain:
                yield from dfs_solver(rem_cons, merge_two_dicts(context, {var: val}), var_order[1:])


def dfs_solve_all(csp, var_order=None):
    """depth-first CSP solver to return a list of all solutions to csp.
    """
    if var_order == None:  # use an arbitrary variable order
        var_order = list(csp.variables)
    return list(dfs_solver(csp.constraints, {}, var_order))


def dfs_solve1(csp, var_order=None):
    """depth-first CSP solver to find single solution or None if there are no solutions.
    """
    if var_order == None:  # use an arbitrary variable order
        var_order = list(csp.variables)
    gen = dfs_solver(csp.constraints, {}, var_order)
    try:  # Python generators raise an exception if there are no more elements.
        return next(gen)
    except StopIteration:
        return None


def runDfs(csp):
    # test_csp(dfs_solve1)
    test_csp(dfs_solve_all, csp)
    csp.show()
    # plt.show()


def test_csp(CSP_solver, csp):
    """CSP_solver is a solver that takes a csp and returns a solution
    csp is a constraint satisfaction problem
    solutions is the list of all solutions to csp
    This tests whether the solution returned by CSP_    solver is a solution.
    """
    print("Testing csp with", CSP_solver.__doc__)
    sol = CSP_solver(csp)
    print("Solution found:", sol)
