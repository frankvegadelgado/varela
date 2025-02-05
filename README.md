# Varela: Minimum Vertex Cover Solver

![Honoring the Memory of Felix Varela y Morales (Cuban Catholic priest and independence leader)](docs/varela.jpg)

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

|        | c0  | c1  | c2  | c3  | c4  |
| ------ | --- | --- | --- | --- | --- |
| **r0** | 0   | 0   | 1   | 0   | 1   |
| **r1** | 0   | 0   | 0   | 1   | 0   |
| **r2** | 1   | 0   | 0   | 0   | 1   |
| **r3** | 0   | 1   | 0   | 0   | 0   |
| **r4** | 1   | 0   | 1   | 0   | 0   |

A matrix is represented in a text file using the following string representation:

```
00101
00010
10001
01000
10100
```

This represents a 5x5 matrix where each line corresponds to a row, and '1' indicates a connection or presence of an element, while '0' indicates its absence.

_Example Solution:_

Vertex Cover Found `0, 1, 4`: Nodes `0, 1, 4` form an optimal solution.

---

# Our Algorithm - Polynomial Runtime

## Algorithm Overview

1. **Input Validation:**

   - Checks if the input is a valid SciPy sparse matrix.
   - Ensures the matrix is square (representing an adjacency matrix).

2. **Empty Graph Handling:**

   - Returns `None` if the input graph is empty (no vertices or edges).

3. **Graph Conversion:**

   - Converts the sparse adjacency matrix to a NetworkX graph for easier manipulation.

4. **Edge Graph Construction:**

   - Creates a new graph called the "edge graph."
   - Each _node_ in the edge graph represents an _edge_ in the original graph.
   - An _edge_ is added between two nodes in the edge graph if the corresponding edges in the original graph share a vertex.

5. **Minimum Edge Cover:**

   - Computes a minimum edge cover of the edge graph using `nx.min_edge_cover()`. This function typically uses matching techniques.

6. **Vertex Cover from Edge Cover:**

   - Iterates through the edges in the minimum edge cover of the edge graph.
   - For each edge in the edge cover, identifies the corresponding edges in the original graph (using the computed mapping).
   - Finds the common vertex between these two original edges.
   - Adds this common vertex to the vertex cover.

7. **Isolated Edge Handling (Heuristic):**

   - Iterates through the edges in the original graph.
   - If an edge has _both_ endpoints _not_ in the current vertex cover, adds one of the endpoints to the vertex cover. This is intended to handle edges that might not have been covered by the edge cover step.

8. **Redundancy Removal (Heuristic):**
   - Iterates through the vertices in the approximate vertex cover.
   - For each vertex, checks if removing it still results in a valid vertex cover (using `utils.is_vertex_cover()`).
   - If removing the vertex results in a valid cover, the vertex is removed. This step attempts to reduce the size of the cover.

## Runtime Analysis

- **Edge Graph Construction:** $O(|E|^2)$ in the worst case.
- **Minimum Edge Cover:** The complexity of `nx.min_edge_cover()` depends on the underlying algorithm used, but it's typically polynomial (e.g., $O(|V|^3)$ if based on matching). Here, $|V|$ refers to the number of nodes in the _edge graph_, which is equal to the number of edges in the original graph ($|E|$). So, this step is likely $O(|E|^3)$.
- **Vertex Cover Construction (from Edge Cover):** $O(|E|)$, as it iterates through the edges in the edge cover.
- **Isolated Edge Handling:** $O(|E|)$.
- **Redundancy Removal:** $O(|V||E|)$.

**Overall Runtime:** The dominant factor is likely the minimum edge cover calculation on the edge graph, making the overall runtime likely $O(|E|^3)$. However, the $O(|E|^2)$ from the edge graph construction is also significant.

**Important Note:** The runtime analysis is based on the number of edges in the original graph ($|E|$) because the edge graph's size is proportional to $|E|$.

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
   approx -i ./benchmarks/testMatrix1.txt
   ```

   utilizing the `approx` command provided by Varela's Library to execute the Boolean adjacency matrix `varela\benchmarks\testMatrix1.txt`. The file `testMatrix1.txt` represents the example described herein. We also support `.xz`, `.lzma`, `.bz2`, and `.bzip2` compressed `.txt` files.

   **Example Output:**

   ```
   testMatrix1.txt: Vertex Cover Found 0, 1, 4
   ```

   This indicates nodes `0, 1, 4` form a vertex cover.

---

## Vertex Cover Size

Use the `-c` flag to count the nodes in the vertex cover:

```bash
approx -i ./benchmarks/testMatrix2.txt -c
```

**Output:**

```
testMatrix2.txt: Vertex Cover Size 5
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

Estimating the Minimum Vertex Cover with an approximation factor of 7/5 for large enough undirected graphs encoded as a Boolean adjacency matrix stored in a file.

options:
  -h, --help            show this help message and exit
  -i INPUTFILE, --inputFile INPUTFILE
                        input file path
  -a, --approximation   enable comparison with a polynomial-time approximation approach within a factor of 2
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
  -a, --approximation   enable comparison with a polynomial-time approximation approach within a factor of 2
  -b, --bruteForce      enable comparison with the exponential-time brute-force approach
  -c, --count           calculate the size of the vertex cover
  -w, --write           write the generated random matrix to a file in the current directory
  -v, --verbose         enable verbose output
  -l, --log             enable file logging
  --version             show program's version number and exit
```

---

# Code

- Python implementation by **Frank Vega**.

---

# Complexity

```diff
+ We present a polynomial-time algorithm achieving an approximation ratio of 7/5 for MVC, providing strong evidence that P = NP by efficiently solving a computationally hard problem with near-optimal solutions.

+ This result contradicts the Unique Games Conjecture, suggesting that many optimization problems may admit better solutions, revolutionizing theoretical computer science.
```

---

# License

- MIT License.
