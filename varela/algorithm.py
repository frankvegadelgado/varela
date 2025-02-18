# Created on 02/05/2025
# Author: Frank Vega

import itertools
from . import utils

import networkx as nx

def find_vertex_cover(graph):
    """
    Computes an approximate vertex cover in polynomial time with an approximation ratio of less than 2 for undirected graphs.

    Args:
        graph (nx.Graph): A NetworkX Graph object representing the input graph.

    Returns:
        set: A set of vertex indices representing the approximate vertex cover.
             Returns an empty set if the graph is empty or has no edges.
    """

    # Handle empty graph or graph with no edges
    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return set()  # Return an empty set instead of None for consistency

    # Initialize an empty set to store the approximate vertex cover
    approximate_vertex_cover = set()

    # Iterate over all connected components of the graph
    for connected_component in nx.connected_components(graph):
        # Create a subgraph for the current connected component
        subgraph = graph.subgraph(connected_component)

        # Skip if the subgraph has no edges (though this should not happen due to the initial check)
        if subgraph.number_of_edges() == 0:
            continue

        # Find a maximal independent set in the subgraph
        maximal_independent_set = nx.maximal_independent_set(subgraph)

        # Vertex cover is the complement of the maximal independent set
        vertex_cover = set(subgraph.nodes) - set(maximal_independent_set)
        
        # Add the vertices from this connected component to the final vertex cover
        approximate_vertex_cover.update(vertex_cover)

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