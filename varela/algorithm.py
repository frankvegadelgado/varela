# Created on 26/07/2025
# Author: Frank Vega

import itertools
from . import utils

import networkx as nx
import math
from hvala.algorithm import find_vertex_cover as hvala_find_vertex_cover
from . import reduction

def find_vertex_cover(graph):
    """
    Compute a near-optimal vertex cover for an undirected graph with an approximation ratio under sqrt(2).
    
    A vertex cover is a set of vertices such that every edge in the graph is incident 
    to at least one vertex in the set. This function finds an approximate solution
    using a polynomial-time reduction approach.
    
    Args:
        graph (nx.Graph): Input undirected graph.
    
    Returns:
       set: A set of vertex indices representing the approximate vertex cover set.
             Returns an empty set if the graph is empty or has no edges.
             
    Raises:
        ValueError: If input is not a NetworkX Graph object.
        RuntimeError: If the polynomial-time reduction fails (max degree > 1 after transformation).
    """
    
    # Reject non-graph inputs early to avoid misleading errors downstream
    if not isinstance(graph, nx.Graph):
        raise ValueError("Input must be an undirected NetworkX Graph.")
    
    # An empty graph or one with no edges has a trivially empty vertex cover
    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return set()
    
    # Work on a copy so the caller's graph is never mutated
    working_graph = graph.copy()

    # Self-loops are irrelevant to vertex cover (a single vertex already covers them)
    working_graph.remove_edges_from(list(nx.selfloop_edges(working_graph)))

    # Isolated vertices cannot belong to any edge, so they never need to be in the cover
    working_graph.remove_nodes_from(list(nx.isolates(working_graph)))
    
    # After stripping self-loops and isolates the graph may now be empty
    if working_graph.number_of_nodes() == 0:
        return set()
    
    approximate_vertex_cover = set()

    # The number of reduction rounds is bounded logarithmically in n so that the
    # total work stays polynomial while still exploring enough transformed instances
    # to push the approximation ratio below sqrt(2)
    bound = math.ceil(math.log2(3 * len(graph.nodes())))

    # Process each connected component independently; a vertex cover of the whole
    # graph is the union of vertex covers of its components
    for component in nx.connected_components(working_graph):
        component_subgraph = working_graph.subgraph(component).copy()

        # Seed the candidate list with the cover found directly on the original component
        solutions = [hvala_find_vertex_cover(component_subgraph)]

        # Generate additional candidates by reducing the component to increasingly
        # transformed graphs and mapping each resulting cover back to the original
        # vertex set; odd offsets 2t+1 stagger the reduction parameter so successive
        # instances expose different structural properties of the component
        for t in range(bound):
            reduced_graph = reduction.vc_to_vc_reduction(component_subgraph, 2 * t + 1)
            reduced_cover = hvala_find_vertex_cover(reduced_graph)
            # Map the cover found in the reduced graph back to vertices of the original component
            solutions.append(reduction.extract_original_vc(reduced_cover, component_subgraph, 2 * t + 1))

        # Keep only the smallest cover among all candidates for this component;
        # taking the minimum over multiple reductions is what drives the ratio below sqrt(2)
        solution = min(solutions, key=len)
        approximate_vertex_cover.update(solution)

    # Verify the result is a genuine vertex cover before returning it;
    # a failure here indicates a bug in the reduction or extraction logic
    if not utils.is_vertex_cover(graph, approximate_vertex_cover):
        raise RuntimeError(
            f"Polynomial-time reduction failed: the set {approximate_vertex_cover} "
            f"is not a vertex cover for the original graph."
        )

    return approximate_vertex_cover

def find_vertex_cover_brute_force(graph):
    """
    Computes an exact minimum vertex cover in exponential time.

    Args:
        graph: A NetworkX Graph.

    Returns:
        A set of vertex indices representing the exact vertex cover, or None if the graph is empty.
    """

    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return None

    working_graph = graph.copy()
    working_graph.remove_edges_from(list(nx.selfloop_edges(working_graph)))
    working_graph.remove_nodes_from(list(nx.isolates(working_graph)))
    
    if working_graph.number_of_nodes() == 0:
        return set()

    n_vertices = len(working_graph.nodes())

    for k in range(1, n_vertices + 1): # Iterate through all possible sizes of the cover
        for candidate in itertools.combinations(working_graph.nodes(), k):
            cover_candidate = set(candidate)
            if utils.is_vertex_cover(working_graph, cover_candidate):
                return cover_candidate
                
    return None



def find_vertex_cover_approximation(graph):
    """
    Computes an approximate vertex cover in polynomial time with an approximation ratio of at most 2 for undirected graphs.

    Args:
        graph: A NetworkX Graph.

    Returns:
        A set of vertex indices representing the approximate vertex cover, or None if the graph is empty.
    """

    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return None

    #networkx doesn't have a guaranteed minimum vertex cover function, so we use approximation
    vertex_cover = nx.approximation.vertex_cover.min_weighted_vertex_cover(graph)
    return vertex_cover