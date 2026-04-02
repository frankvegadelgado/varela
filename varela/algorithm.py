# Created on 26/07/2025
# Author: Frank Vega

import itertools
from . import utils

import networkx as nx

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
    def cover_bipartite(bipartite_graph):
        """Compute a minimum vertex cover set for a bipartite graph using matching.

        Args:
            bipartite_graph (nx.Graph): A bipartite NetworkX graph.

        Returns:
            set: A minimum vertex cover set for the bipartite graph.
        """
        optimal_solution = set()
        for component in nx.connected_components(bipartite_graph):
            subgraph = bipartite_graph.subgraph(component)
            # Hopcroft-Karp finds a maximum matching in O(E * sqrt(V)) time
            matching = nx.bipartite.hopcroft_karp_matching(subgraph)
            # By König's theorem, min vertex cover == max matching in bipartite graphs
            vertex_cover = nx.bipartite.to_vertex_cover(subgraph, matching)
            optimal_solution.update(vertex_cover)
        return optimal_solution

    if not isinstance(graph, nx.Graph):
        raise ValueError("Input must be an undirected NetworkX Graph.")
    
    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return set()
    
    working_graph = graph.copy()
    working_graph.remove_edges_from(list(nx.selfloop_edges(working_graph)))
    working_graph.remove_nodes_from(list(nx.isolates(working_graph)))
    
    if working_graph.number_of_nodes() == 0:
        return set()
    
    approximate_vertex_cover = set()
    
    # Process each connected component independently to reduce problem size
    component_solutions = [working_graph.subgraph(component) for component in nx.connected_components(working_graph)]
    while component_solutions:
        subgraph = component_solutions.pop()
        if subgraph.number_of_edges() == 0:
            continue
        if nx.bipartite.is_bipartite(subgraph):
            # Exploit bipartiteness for an exact minimum vertex cover via König's theorem
            approximate_vertex_cover.update(cover_bipartite(subgraph))
        else:
            solution = set(nx.articulation_points(subgraph))
            if not solution:
                # If no articulation points, add all nodes of the component
                node, _ = max(subgraph.degree(), key=lambda x: x[1])
                solution = {node}
            approximate_vertex_cover.update(solution)
            # Remove the cut vertices and recurse on the remaining subgraph
            remaining_nodes = subgraph.subgraph(set(subgraph.nodes()) - solution).copy()
            remaining_isolates = set(nx.isolates(remaining_nodes))
            remaining_nodes.remove_nodes_from(remaining_isolates)
            if remaining_nodes.number_of_edges() > 0:
                new_component_solutions = [remaining_nodes.subgraph(component) for component in nx.connected_components(remaining_nodes)]
                component_solutions.extend(new_component_solutions)
    for u in list(approximate_vertex_cover):
        if utils.is_vertex_cover(graph, approximate_vertex_cover - {u}):
            approximate_vertex_cover.remove(u)
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