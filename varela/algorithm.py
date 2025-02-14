# Created on 02/05/2025
# Author: Frank Vega

import scipy.sparse as sparse
import itertools
import networkx as nx
from . import utils
from networkx.algorithms.flow import shortest_augmenting_path


def find_vertex_cover(graph):
    """
    Computes an approximate vertex cover in polynomial time with an approximation ratio of at most 3/2 for undirected graphs.

    Args:
        graph: A NetworkX Graph.

    Returns:
        A set of vertex indices representing the approximate vertex cover, or None if the graph is empty.
    """

    # Handle empty graph
    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return None
    
    # Upper bound
    n = max(graph.nodes()) + 1

    # Create an edge graph where each node represents an edge in the original graph
    edge_graph = nx.Graph()
    for u, v in graph.edges():
        # Minimum and maximum vertices
        minimum = min(u, v)
        maximum = max(u, v)
        # Unique representation of the edge
        edge = n * minimum + maximum
        for a in graph.neighbors(minimum):
            if maximum < a:
                adjacent_edge = n * minimum + a
                edge_graph.add_edge(edge, adjacent_edge)
        for b in graph.neighbors(maximum):
            if b < minimum:
                adjacent_edge = n * b + maximum
                edge_graph.add_edge(edge, adjacent_edge)

    # Find the minimum edge cover in the edge graph
    min_edge_cover = nx.approximation.min_maximal_matching(edge_graph)

    # Convert the edge cover back to a vertex cover
    vertex_cover = set()
    for edge1, edge2 in min_edge_cover:
        # Extract the common vertex between the two edges
        common_vertex = (edge1 // n) if (edge1 // n) == (edge2 // n) else (edge1 % n)
        vertex_cover.add(common_vertex)

    # Include isolated edges (edges not covered by the vertex cover)
    for u, v in graph.edges():
        if u not in vertex_cover and v not in vertex_cover:
            vertex_cover.add(u)

    # Remove redundant vertices from the vertex cover
    approximate_vertex_cover = set(vertex_cover)
    for u in vertex_cover:
        # Check if removing the vertex still results in a valid vertex cover
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

    n_vertices = len(graph.nodes())

    for k in range(1, n_vertices + 1): # Iterate through all possible sizes of the cover
        for candidate in itertools.combinations(graph.nodes(), k):
            cover_candidate = set(candidate)
            if utils.is_vertex_cover(graph, cover_candidate):
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