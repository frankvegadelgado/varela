# Created on 02/05/2025
# Author: Frank Vega

import itertools
import networkx as nx
from . import utils


def find_vertex_cover(graph):
    """
    Computes an approximate vertex cover in polynomial time with an approximation ratio of less than 2 for undirected graphs.

    Args:
        graph: A NetworkX Graph.

    Returns:
        A set of vertex indices representing the approximate vertex cover, or None if the graph is empty.
    """

    # Handle empty graph
    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return None
    
    approximate_vertex_cover = set()
    connected_components = nx.connected_components(graph)
    for connected_component in connected_components:
        subgraph = graph.subgraph(connected_component)
        if subgraph.number_of_edges() > 0:
            if subgraph.number_of_nodes() == 2:
                # Include isolated edges
                for u, _ in subgraph.edges():
                    approximate_vertex_cover.add(u)
            else:
                
                # Create an edge graph where each node represents an edge in the original graph
                edge_graph = nx.line_graph(subgraph)                    
    
                # Find the minimum edge cover in the edge graph
                min_edge_cover = nx.min_edge_cover(edge_graph)

                # Convert the edge matching back to a vertex cover
                candidate_vertex_cover = set()
                for edge1, edge2 in min_edge_cover:
                    # Extract the common vertex between the two edges
                    common_vertex = edge1[0] if edge1[0] == edge2[0] else edge1[1]
                    candidate_vertex_cover.add(common_vertex)

                # Remove redundant vertices from the vertex cover
                vertex_cover = set(candidate_vertex_cover)
                for u in candidate_vertex_cover:
                    # Check if removing the vertex still results in a valid vertex cover
                    if utils.is_vertex_cover(subgraph, vertex_cover - {u}):
                        vertex_cover.remove(u)

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