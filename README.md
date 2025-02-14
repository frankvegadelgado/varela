# Varela: Minimum Vertex Cover Solver

![Honoring the Memory of Felix Varela y Morales (Cuban Catholic priest and independence leader)](docs/varela.jpg)

This work builds upon [The Unique Games Conjecture](https://www.researchgate.net/publication/388791285_The_Unique_Games_Conjecture).

---

# The Minimum Vertex Cover Problem

The **Minimum Vertex Cover (MVC)** problem is a classic optimization problem in computer science and graph theory. It involves finding the smallest set of vertices in a graph that **covers** all edges, meaning at least one endpoint of every edge is included in the set.

## Formal Definition

Given an undirected graph $G = (V, E)$, a **vertex cover** is a subset $V' \subseteq V$ such that for every edge $(u, v) \in E$, at least one of $u$ or $v$ belongs to $V'$. The MVC problem seeks the vertex cover with the smallest cardinality.

## Importance and Applications

- **Theoretical Significance:** MVC is a well-known NP-hard problem, central to complexity theory.
- **Practical Applications:**
  - **Network Security:** Identifying critical nodes to disrupt connections.
  - **Bioinformatics:** Analyzing gene regulatory networks.
  - **Wireless Sensor Networks:** Optimizing sensor coverage.

## Related Problems

- **Maximum Independent Set:** The complement of a vertex cover.
- **Set Cover Problem:** A generalization of MVC.

---

## Problem Statement

Input: A Boolean Adjacency Matrix $M$.

Answer: Find a Minimum Vertex Cover.

### Example Instance: 5 x 5 matrix

|        | c1  | c2  | c3  | c4  | c5  |
| ------ | --- | --- | --- | --- | --- |
| **r1** | 0   | 0   | 1   | 0   | 1   |
| **r2** | 0   | 0   | 0   | 1   | 0   |
| **r3** | 1   | 0   | 0   | 0   | 1   |
| **r4** | 0   | 1   | 0   | 0   | 0   |
| **r5** | 1   | 0   | 1   | 0   | 0   |

The input for undirected graph is typically provided in [DIMACS](http://dimacs.rutgers.edu/Challenges) format. In this way, the previous adjacency matrix is represented in a text file using the following string representation:

```
p edge 5 4
e 1 3
e 1 5
e 2 4
e 3 5
```

This represents a 5x5 matrix in DIMACS format such that each edge $(v,w)$ appears exactly once in the input file and is not repeated as $(w,v)$. In this format, every edge appears in the form of

```
e W V
```

where the fields W and V specify the endpoints of the edge while the lower-case character `e` signifies that this is an edge descriptor line.

_Example Solution:_

Vertex Cover Found `1, 2, 5`: Nodes `1`, `2`, and `5` constitute an optimal solution.

---

# Our Algorithm - Polynomial Runtime

## Algorithm Overview

1. **Input**: Adjacency matrix of graph G
2. **Create Edge Graph**:
   - Nodes represent edges of G
   - Connect nodes if edges share a vertex
3. **Find Minimum Edge Cover** in edge graph
4. **Extract Vertex Cover**:
   - Add common vertices from edge cover
5. **Handle Isolated Edges**:
   - Add vertices for uncovered edges
6. **Remove Redundant Vertices**
7. **Output**: Approximate minimum vertex cover

Key Features:

- Polynomial-time complexity: O($|E|^3$)
- Approximation ratio: ≤ 3/2
- Suitable for large, sparse graphs

## Correctness

1. **Edge Graph Construction**

   - Preserves edge relationships of original graph

2. **Minimum Edge Cover**

   - Ensures every edge in edge graph is covered

3. **Vertex Cover Extraction**

   - Guarantees at least one endpoint of each edge is in cover

4. **Isolated Edge Handling**

   - Covers any remaining uncovered edges

5. **Redundancy Removal**
   - Optimizes cover size while maintaining validity

Correctness Guarantee:

- Every edge in original graph has at least one endpoint in cover
- Resulting set is a valid, approximate minimum vertex cover

Approximation Quality:

- Achieves ≤ 3/2 approximation ratio
- Trade-off between accuracy and polynomial-time efficiency

## Runtime Analysis

This section analyzes the runtime and space complexity of the given vertex cover approximation algorithm.

### Time Complexity Breakdown

1. **Input Processing and Graph Creation:** $O(|E|)$

   - $|E|$ represents the number of edges in the input graph.
   - This step involves converting the sparse matrix representation to a NetworkX graph, which iterates through the non-zero entries (edges).

2. **Edge Graph Construction:** $O(|E| \Delta)$

   - $\Delta$ represents the maximum degree of any vertex in the graph.
   - For each edge in the original graph, we examine its endpoints' neighbors to create corresponding edges in the edge graph. The number of neighbors is bounded by $\Delta$.

3. **Minimum Edge Cover Computation:** $O(|E|^3)$

   - This step utilizes the `nx.min_edge_cover()` function. The complexity relates to the number of _nodes_ in the edge graph (which is $|E|$). The complexity is therefore $O(|E|^3)$.

4. **Vertex Cover Extraction:** $O(|E|)$

   - This step iterates through the edges in the computed minimum edge cover, which is bounded by the number of edges in the original graph.

5. **Isolated Edge Handling:** $O(|E|)$

   - We iterate through all edges in the original graph to handle any isolated edges.

6. **Redundancy Removal:** $O(k |E|)$, or $O(|E|^2)$ in the worst case.
   - $k$ is the size of the vertex cover. In the worst-case, the size of the vertex cover can be $O(|E|)$, so the overall time complexity is $O(|E|^2)$.
   - For each vertex in the (potentially large) vertex cover, we check if its removal still leaves a valid cover. This check involves examining all edges.

### Overall Complexity

- **Time Complexity:** $O(|E|^3)$ (dominated by the minimum edge cover computation).
- **Space Complexity:** $O(|V| + |E| + |E|\Delta)$. In the worst-case scenario (dense graphs where $E = O(|V|^2)$ and $\Delta = O(|V|)$), this becomes $O(|V|^3)$.

### Key Observations

- This algorithm provides an _approximation_ of the minimum vertex cover, trading accuracy for a polynomial runtime.
- The practical runtime performance can often be significantly better than the worst-case theoretical bound, especially for sparse graphs.
- This approach is suitable for sparse and large graphs where computing the _exact_ minimum vertex cover is computationally infeasible.

---

# Compile and Environment

## Prerequisites

- Python ≥ 3.10

## Installation

```bash
pip install varela
```

## Execution

1. Clone the repository:

   ```bash
   git clone https://github.com/frankvegadelgado/varela.git
   cd varela
   ```

2. Run the script:

   ```bash
   approx -i ./benchmarks/testMatrix1
   ```

   utilizing the `approx` command provided by Varela's Library to execute the Boolean adjacency matrix `varela\benchmarks\testMatrix1`. The file `testMatrix1` represents the example described herein. We also support `.xz`, `.lzma`, `.bz2`, and `.bzip2` compressed text files.

   **Example Output:**

   ```
   testMatrix1: Vertex Cover Found 1, 2, 5
   ```

   This indicates nodes `1, 2, 5` form a vertex cover.

---

## Vertex Cover Size

Use the `-c` flag to count the nodes in the vertex cover:

```bash
approx -i ./benchmarks/testMatrix2 -c
```

**Output:**

```
testMatrix2: Vertex Cover Size 5
```

---

# Command Options

Display help and options:

```bash
approx -h
```

**Output:**

```bash
usage: approx [-h] -i INPUTFILE [-a] [-b] [-c] [-v] [-l] [--version]

Estimating the Minimum Vertex Cover with an approximation factor of ≤ 3/2 for an undirected graph encoded in DIMACS format and stored in a file.

options:
  -h, --help            show this help message and exit
  -i INPUTFILE, --inputFile INPUTFILE
                        input file path
  -a, --approximation   enable comparison with a polynomial-time approximation approach within a factor of at most 2
  -b, --bruteForce      enable comparison with the exponential-time brute-force approach
  -c, --count           calculate the size of the vertex cover
  -v, --verbose         enable verbose output
  -l, --log             enable file logging
  --version             show program's version number and exit
```

---

# Testing Application

A command-line utility named `test_approx` is provided for evaluating the Algorithm using randomly generated, large sparse matrices. It supports the following options:

```bash
usage: test_approx [-h] -d DIMENSION [-n NUM_TESTS] [-s SPARSITY] [-a] [-b] [-c] [-w] [-v] [-l] [--version]

The Varela Testing Application.

options:
  -h, --help            show this help message and exit
  -d DIMENSION, --dimension DIMENSION
                        an integer specifying the dimensions of the square matrices
  -n NUM_TESTS, --num_tests NUM_TESTS
                        an integer specifying the number of tests to run
  -s SPARSITY, --sparsity SPARSITY
                        sparsity of the matrices (0.0 for dense, close to 1.0 for very sparse)
  -a, --approximation   enable comparison with a polynomial-time approximation approach within a factor of at most 2
  -b, --bruteForce      enable comparison with the exponential-time brute-force approach
  -c, --count           calculate the size of the vertex cover
  -w, --write           write the generated random matrix to a file in the current directory
  -v, --verbose         enable verbose output
  -l, --log             enable file logging
  --version             show program's version number and exit
```

---

# Batch Execution

Batch execution allows you to solve multiple graphs within a directory simultaneously.

To view available command-line options for the `batch_approx` command, use the following in your terminal or command prompt:

```bash
batch_approx -h
```

This will display the following help information:

```bash
usage: batch_approx [-h] -i INPUTDIRECTORY [-a] [-b] [-c] [-v] [-l] [--version]

Estimating the Minimum Vertex Cover with an approximation factor of ≤ 3/2 for all undirected graphs encoded in DIMACS format and stored in a directory.

options:
  -h, --help            show this help message and exit
  -i INPUTDIRECTORY, --inputDirectory INPUTDIRECTORY
                        Input directory path
  -a, --approximation   enable comparison with a polynomial-time approximation approach within a factor of at most 2
  -b, --bruteForce      enable comparison with the exponential-time brute-force approach
  -c, --count           calculate the size of the vertex cover
  -v, --verbose         anable verbose output
  -l, --log             enable file logging
  --version             show program's version number and exit
```

---

# Code

- Python implementation by **Frank Vega**.

---

# Complexity

```diff
+ This result contradicts the Unique Games Conjecture, suggesting that many optimization problems may admit better solutions, revolutionizing theoretical computer science.
```

---

# License

- MIT License.
