# Non-Commercial Implementation Code
import networkx as nx
import io
import contextlib
# Suppress OR-Tools DLL loading output
with contextlib.redirect_stdout(io.StringIO()):
    from ortools.linear_solver import pywraplp


def minimum_dominating_set_chordal(graph):
    # Ensure the graph is chordal
    if not nx.is_chordal(graph):
        raise ValueError("The input graph is not chordal.")

    # Create a solver instance
    solver = pywraplp.Solver.CreateSolver('SCIP')  # Use 'CBC' for open-source MILP

    # Create binary variables for each node
    x = {}
    for node in graph.nodes():
        x[node] = solver.IntVar(0, 1, f'x_{node}')

    # Objective function: minimize the sum of x_i
    solver.Minimize(solver.Sum([x[node] for node in graph.nodes()]))

    # Constraints: each node must be dominated by at least one node in the set
    for node in graph.nodes():
        solver.Add(solver.Sum([x[nbr] for nbr in graph.neighbors(node)]) + x[node] >= 1)

    # Solve the problem
    status = solver.Solve()

    # Extract the solution
    if status == pywraplp.Solver.OPTIMAL:
        dominating_set = [node for node in graph.nodes() if x[node].solution_value() > 0.5]
        return dominating_set
    else:
        raise Exception("No optimal solution found.")
