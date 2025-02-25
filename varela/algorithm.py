# Created on 02/05/2025
# Author: Frank Vega

import itertools
from . import utils


import networkx as nx

def find_vertex_cover(graph):
    """
    Computes an approximate vertex cover for an undirected graph in polynomial time.
    The algorithm uses edge covers, bipartite matching, and Konig's theorem to achieve
    an approximation ratio of less than 2.

    Args:
        graph (nx.Graph): A NetworkX Graph object representing the input graph.

    Returns:
        set: A set of vertex indices representing the approximate vertex cover.
             Returns None if the graph is empty or has no edges.
    """

    # Handle empty graph or graph with no edges
    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return None

    # Remove isolated nodes (nodes with no edges) as they are not part of any vertex cover
    graph.remove_nodes_from(list(nx.isolates(graph)))

    # Initialize an empty set to store the approximate vertex cover
    approximate_vertex_cover = set()

    # Find a minimum edge cover in the graph
    min_edge_cover = nx.min_edge_cover(graph)

    # Create a subgraph using the edges from the minimum edge cover
    min_edge_graph = nx.Graph(min_edge_cover)

    # Iterate over all connected components of the min_edge_graph
    for connected_component in nx.connected_components(min_edge_graph):
        # Create a subgraph for the current connected component
        subgraph = min_edge_graph.subgraph(connected_component)

        # Find a maximum matching in the bipartite subgraph using Hopcroft-Karp algorithm
        maximum_matching = nx.bipartite.hopcroft_karp_matching(subgraph)

        # Use Konig's theorem to find a vertex cover in the bipartite subgraph
        vertex_cover = nx.bipartite.to_vertex_cover(subgraph, maximum_matching)

        # Add the vertices from this connected component to the final vertex cover
        approximate_vertex_cover.update(vertex_cover)
    
    # Verify if the computed vertex cover is valid
    if not utils.is_vertex_cover(graph, approximate_vertex_cover):
        # Delete selected and isolated nodes
        graph.remove_nodes_from(approximate_vertex_cover)
        graph.remove_nodes_from(list(nx.isolates(graph)))
        # Compute approximate vertex cover (2-approximation)
        residual_vertex_cover = nx.approximation.vertex_cover.min_weighted_vertex_cover(graph)
        approximate_vertex_cover.update(residual_vertex_cover)

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