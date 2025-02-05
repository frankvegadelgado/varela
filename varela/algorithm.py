# Created on 02/05/2025
# Author: Frank Vega

import scipy.sparse as sparse
import itertools
import networkx as nx
import numpy as np
from . import utils

def find_vertex_cover(adjacency_matrix):
    """
    Calculates an approximate vertex cover in polynomial time with an approximation ratio of 7/5 for large enough undirected graphs.

    Args:
        adjacency_matrix: A SciPy sparse adjacency matrix.

    Returns:
        A set of vertex indices representing the approximate vertex cover, or None if the graph is empty.
        Raises ValueError if the input matrix is not square or if the graph is invalid.
        Raises TypeError if the input is not a sparse matrix.
    """

    # Validate input type
    if not sparse.issparse(adjacency_matrix):
        raise TypeError("Input must be a SciPy sparse matrix.")

    # Validate matrix shape
    n = np.int64(adjacency_matrix.shape[0])
    if adjacency_matrix.shape[0] != adjacency_matrix.shape[1]:
        raise ValueError("Adjacency matrix must be square.")

    # Handle empty graph
    if n == 0 or adjacency_matrix.nnz == 0:
        return None  # Handle empty graph

    # Convert the sparse matrix to a NetworkX graph
    # Avoid duplicates in undirected graphs
    graph = nx.Graph(utils.sparse_matrix_to_edges(adjacency_matrix))

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
    # It's solved by employing matching techniques in O(|V|^3)
    min_edge_cover = nx.min_edge_cover(edge_graph)

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

 
def find_vertex_cover_brute_force(adj_matrix):
    """
    Calculates the exact minimum vertex cover using brute-force (exponential time).

    Args:
        adj_matrix: A SciPy sparse adjacency matrix.

    Returns:
        A set of vertex indices representing the minimum vertex cover, or None if the graph is empty.
        Raises ValueError if the input matrix is not square.
        Raises TypeError if the input is not a sparse matrix.
    """
  
    if not sparse.issparse(adj_matrix):
        raise TypeError("Input must be a SciPy sparse matrix.")
  
    n_vertices = adj_matrix.shape[0]
    if adj_matrix.shape[0] != adj_matrix.shape[1]:
        raise ValueError("Adjacency matrix must be square.")
  
    if n_vertices == 0 or adj_matrix.nnz == 0:
        return None # Handle empty graph

    # Convert the sparse matrix to a NetworkX graph
    graph = nx.Graph(utils.sparse_matrix_to_edges(adj_matrix))

    for k in range(1, n_vertices + 1): # Iterate through all possible sizes of the cover
        for cover_candidate in itertools.combinations(range(n_vertices), k):
            cover_candidate = set(cover_candidate)
            if utils.is_vertex_cover(graph, cover_candidate):
                return cover_candidate
                
    return None



def find_vertex_cover_approximation(adj_matrix):
    """
    Calculates the approximate vertex cover using an approximation (polynomial time).

    Args:
        adj_matrix: A SciPy sparse adjacency matrix.

    Returns:
        A set of vertex indices representing an approximation of the minimum vertex cover, or None if the graph is empty.
        Raises ValueError if the input matrix is not square.
        Raises TypeError if the input is not a sparse matrix.
    """
    
    if not sparse.issparse(adj_matrix):
        raise TypeError("Input must be a SciPy sparse matrix.")
  
    n_vertices = adj_matrix.shape[0]
    if adj_matrix.shape[0] != adj_matrix.shape[1]:
        raise ValueError("Adjacency matrix must be square.")
  
    if n_vertices == 0 or adj_matrix.nnz == 0:
        return None # Handle empty graph

    # Convert the sparse matrix to a NetworkX graph
    graph = nx.Graph(utils.sparse_matrix_to_edges(adj_matrix))

    #networkx doesn't have a guaranteed minimum vertex cover function, so we use approximation
    vertex_cover = nx.approximation.vertex_cover.min_weighted_vertex_cover(graph)
    return vertex_cover