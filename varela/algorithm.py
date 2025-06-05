# Created on 02/05/2025
# Author: Frank Vega

import itertools
from . import utils

import networkx as nx
import baldor.algorithm as alg

def find_vertex_cover(graph):
    """
    Compute an approximate minimum vertex cover set for an undirected graph.

    Args:
        graph (nx.Graph): A NetworkX Graph object representing the input graph.

    Returns:
        set: A set of vertex indices representing the minimum vertex cover set.
             Returns an empty set if the graph is empty or has no edges.
    """
    # Check if the input graph is a valid undirected NetworkX Graph; raises an error if not.
    if not isinstance(graph, nx.Graph):
        raise ValueError("Input must be an undirected NetworkX Graph.")

    # Handle edge cases: return an empty set if the graph has no nodes or no edges, as no vertex cover is needed.
    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return set()

    # Identify and remove isolated nodes (nodes with degree 0) since they cannot be part of a vertex cover.
    isolated_nodes = list(nx.isolates(graph))
    graph.remove_nodes_from(isolated_nodes)

    # After removing isolated nodes, if the graph is empty, return an empty set (no vertex cover needed).
    if graph.number_of_nodes() == 0:
        return set()

    # Initialize an empty set to store the approximate vertex cover.
    approximate_vertex_cover = set()

    # Create a working copy of the graph to iteratively modify during the vertex cover computation.
    iterative_graph = graph.copy()

    # Initialize an empty graph to store the previous state of iterative_graph for cycle detection.
    previous_new_graph = nx.Graph()

    # Continue iterating until the current set forms a vertex cover for the original graph.
    while not utils.is_vertex_cover(graph, approximate_vertex_cover):

        # Check if the current iterative_graph is identical to the previous iteration's graph (cycle detection).
        # If identical, use NetworkX's min_weighted_vertex_cover to break the loop and finalize the vertex cover.
        if utils.graphs_are_identical(iterative_graph, previous_new_graph):
            approximate_vertex_cover.update(nx.approximation.vertex_cover.min_weighted_vertex_cover(iterative_graph))
            break
        # Otherwise, store the current iterative_graph as the previous state for the next iteration.
        else:
            previous_new_graph = iterative_graph                

        # Create a new graph to transform the current iterative graph for dominating set computation.
        new_graph = nx.Graph()

        # Construct the new graph by creating tuple nodes for each vertex and edge.
        for i in iterative_graph.nodes():
            for j in iterative_graph.neighbors(i):
                if not new_graph.has_edge((i, i), (j, j)):  # Ensure each edge (i, j) is processed only once by ordering i < j.
                    # Add edges to represent the vertex cover structure:
                    # (i, i) to (i, j): vertex i's representative to edge (i, j).
                    # (j, j) to (i, j): vertex j's representative to edge (i, j).
                    # (i, i) to (j, j): connect the vertex representatives.
                    new_graph.add_edge((i, i), (i, j))
                    new_graph.add_edge((j, j), (i, j))
                    new_graph.add_edge((i, i), (j, j))

        # Use Baldor's 2-approximation algorithm to find a dominating set in the new graph.
        # This dominating set corresponds to a vertex cover in the original graph via the transformation.
        tuple_vertex_cover = alg.find_dominating_set(new_graph)

        # Extract vertices from the dominating set where the tuple node is of the form (i, i),
        # meaning the vertex i is selected for the vertex cover; update the approximate vertex cover.
        approximate_vertex_cover.update({tuple_node[0] 
                                for tuple_node in tuple_vertex_cover 
                                if tuple_node[0] == tuple_node[1]})

        # Reconstruct the iterative graph using edges from the dominating set where tuple nodes
        # are of the form (i, j) with i != j, representing remaining edges to cover.
        iterative_graph = nx.Graph()
        iterative_graph.add_edges_from({tuple_node 
                                  for tuple_node in tuple_vertex_cover 
                                  if tuple_node[0] != tuple_node[1]})

    # Return the computed approximate vertex cover set.
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