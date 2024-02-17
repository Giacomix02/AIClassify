PAUSE = True
PAUSE_LENGTH = 0.2


class Variable(object):
    """A random variable.
    name (string) - name of the variable
    domain (list) - a list of the values for the variable.
    Variables are ordered according to their name.
    """

    def __init__(self, name, domain, position=None):
        """Variable
        name a string
        domain a list of printable values
        position of form (x,y)
        """
        self.name = name  # string
        self.domain = domain  # list of values
        self.position = position if position else (random.random(), random.random())
        self.size = len(domain)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name  # f"Variable({self.name})"


class Constraint(object):
    """A Constraint consists of
    * scope: a tuple of variables
    * condition: a Boolean function that can applied to a tuple of values for variables in scope
    * string: a string for printing the constraints. All of the strings must be unique.
    for the variables
    """

    def __init__(self, scope, condition, string=None, position=None):
        self.scope = scope
        self.condition = condition
        if string is None:
            self.string = str(self.condition.__name__) + str(self.scope)
        else:
            self.string = string
        self.position = position

    def __repr__(self):
        return self.string

    def can_evaluate(self, assignment):
        """
        assignment is a variable:value dictionary
        returns True if the constraint can be evaluated given assignment
        """
        return all(v in assignment for v in self.scope)  # and len(self.scope) == len(assignment)

    def holds(self, assignment):
        """returns the value of Constraint con evaluated in assignment.

        precondition: all variables are assigned in assignment, ie self.can_evaluate(assignment) is true
        """
        return self.condition(*tuple(assignment[v] for v in self.scope))


class CSP(object):
    """A CSP consists of
    * a title (a string)
    * variables, a set of variables
    * constraints, a list of constraints
    * var_to_const, a variable to set of constraints dictionary
    """

    def __init__(self, title, variables, constraints):
        """title is a string
        variables is set of variables
        constraints is a list of constraints
        """
        self.title = title
        self.variables = variables
        self.constraints = constraints
        self.var_to_const = {var: set() for var in self.variables}
        for con in constraints:
            for var in con.scope:
                self.var_to_const[var].add(con)

    def __str__(self):
        """string representation of CSP"""
        return str(self.title)

    def __repr__(self):
        """more detailed string representation of CSP"""
        return f"CSP({self.title}, {self.variables}, {([str(c) for c in self.constraints])})"

    def consistent(self, assignment):
        """assignment is a variable:value dictionary
        returns True if all of the constraints that can be evaluated
                        evaluate to True given assignment.
        """
        return all(con.holds(assignment)
                   for con in self.constraints
                   if con.can_evaluate(assignment))

    def show(self):
        plt.ion()  # interactive
        plt.title(self.title)
        var_bbox = dict(boxstyle="round4,pad=1.0,rounding_size=0.5")
        con_bbox = dict(boxstyle="square,pad=1.0", color="green")
        for var in self.variables:
            if var.position is None:
                var.position = (random.random(), random.random())
        for con in self.constraints:
            if con.position is None:
                con.position = tuple(sum(var.position[i] for var in con.scope) / len(con.scope)
                                     for i in range(2))
            bbox = dict(boxstyle="square,pad=1.0", color="green")
            for var in con.scope:
                ax.annotate(con.string, var.position, xytext=con.position,
                            arrowprops={'arrowstyle': '-'}, bbox=con_bbox,
                            ha='center')
        for var in self.variables:
            x, y = var.position
            plt.text(x, y, var.name, bbox=var_bbox, ha='center')


def showConstraintFail(constraint):
    con_bbox = dict(boxstyle="square,pad=1.0", color="green")
    for var in constraint.scope:
        ax.annotate(constraint.string, var.position, xytext=constraint.position, color='red',  # type: ignore
                    arrowprops={'arrowstyle': '-', "color": "r"}, bbox=con_bbox,
                    ha='center')
    if (PAUSE):
        plt.pause(PAUSE_LENGTH)
    for var in constraint.scope:
        ax.annotate(constraint.string, var.position, xytext=constraint.position,  # type: ignore
                    arrowprops={'arrowstyle': '-'}, bbox=con_bbox,
                    ha='center')


def renderGraph(variables, constraint):
    csp = CSP("CSP", variables, constraint)
    return csp
