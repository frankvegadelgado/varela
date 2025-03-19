# Created on 02/05/2025
# Author: Frank Vega

import itertools
from . import utils


import networkx as nx
from . import chordal
def find_vertex_cover(graph):
    """
    Compute an exact minimum vertex cover set for an undirected graph by transforming it into a chordal graph.

    Args:
        graph (nx.Graph): A NetworkX Graph object representing the input graph.

    Returns:
        set: A set of vertex indices representing the minimum vertex cover set.
             Returns an empty set if the graph is empty or has no edges.
    """
    # Validate input graph
    if not isinstance(graph, nx.Graph):
        raise ValueError("Input must be an undirected NetworkX Graph.")

    # Handle empty graph or graph with no edges
    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return set()

    # Remove isolated nodes (nodes with no edges) as they are not part of any Vertex Cover Set
    isolated_nodes = list(nx.isolates(graph))
    graph.remove_nodes_from(isolated_nodes)

    # If the graph becomes empty after removing isolated nodes, return an empty set
    if graph.number_of_nodes() == 0:
        return set()

    # Create a new graph to transform the original into a chordal graph structure
    chordal_graph = nx.Graph()

    # Add edges to the new graph in a way that creates a chordal structure
    # This structure guarantees that its dominating set serves as a vertex cover to the original graph
    for i in graph.nodes():
        for j in graph.neighbors(i):
            if i < j:
                # Create the nodes as tuple nodes in the chordal graph
                chordal_graph.add_edge((i, i), (i, j))
                chordal_graph.add_edge((j, j), (i, j))
                chordal_graph.add_edge((i, i), (j, i))
                chordal_graph.add_edge((j, j), (j, i))

    # Add additional edges to ensure chordality
    for i in graph.nodes():
        for j in graph.nodes():
            if i < j:
                chordal_graph.add_edge((i, i), (j, j))
    
    # Compute the minimum dominating set in the transformed graph
    tuple_nodes = chordal.minimum_dominating_set_chordal(chordal_graph)
    
    # Extract nodes from the tuple nodes of the dominating set in the chordal graph
    optimal_vertex_cover = {node for tuple_node in tuple_nodes for node in tuple_node}

    return optimal_vertex_cover

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