# Varela: Minimum Vertex Cover Solver

![Honoring the Memory of Felix Varela y Morales (Cuban Catholic priest and independence leader)](docs/varela.jpg)

This work builds upon [The Unique Games Conjecture](https://hal.science/hal-04935775).

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

Vertex Cover Found `1, 2, 3`: Nodes `1`, `2`, and `3` constitute an optimal solution.

---

# Approximate Vertex Cover Algorithm Analysis

## Overview

This algorithm finds an approximate vertex cover for an undirected graph with an approximation ratio of less than 2. It utilizes the NetworkX library and employs the following key strategies:

1. Processes connected components separately
2. Handles isolated edges as a special case
3. Transforms the problem using line graphs
4. Utilizes minimum edge cover to approximate vertex cover
5. Optimizes the solution by removing redundant vertices

## Runtime Analysis

Let $n$ be the number of vertices and $m$ be the number of edges in the graph.

1. Finding connected components: $O(n + m)$
2. For each component:
   - Creating line graph: $O(m^2)$
   - Finding minimum edge cover: $O(m^3)$
   - Converting edge cover to vertex cover: $O(m)$
   - Removing redundant vertices: $O(n m)$

Worst-case time complexity: $O(m^2 + m^3 + n m)$

The dominant term is typically $O(m^3)$ from finding the minimum edge cover.

## Correctness

1. **Approximation Guarantee**:

   - The algorithm leverages the relationship between edge covers in the line graph and vertex covers in the original graph.
   - A minimum edge cover in the line graph corresponds to a set of edges in the original graph that cover all vertices.
   - This relationship ensures an approximation ratio of less than 2.

2. **Handling Special Cases**:

   - Empty graphs are correctly handled by returning None.
   - Isolated edges (2-node subgraphs) are treated separately, ensuring correctness for these simple cases.

3. **Connected Components**:

   - Processing each connected component separately ensures correctness for disconnected graphs without affecting the approximation ratio.

4. **Optimization Step**:

   - Removing redundant vertices at the end maintains the vertex cover property while potentially improving the approximation.

5. **Reliance on NetworkX**:
   - The correctness partly depends on the correct implementation of NetworkX functions, particularly `min_edge_cover`.

While the algorithm provides a valid approximate vertex cover, its practical efficiency may vary depending on the input graph's structure and size. The use of line graphs might lead to increased memory usage for dense graphs.

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
   testMatrix1: Vertex Cover Found 1, 2, 3
   ```

   This indicates nodes `1, 2, 3` form a vertex cover.

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

Estimating the Minimum Vertex Cover with an approximation factor of < 2 for an undirected graph encoded in DIMACS format.

options:
  -h, --help            show this help message and exit
  -i INPUTFILE, --inputFile INPUTFILE
                        input file path
  -a, --approximation   enable comparison with a polynomial-time approximation approach within a factor of at most 2
  -b, --bruteForce      enable comparison with the exponential-time brute-force approach
  -c, --count           calculate the size of the vertex cover
  -v, --verbose         anable verbose output
  -l, --log             enable file logging
  --version             show program's version number and exit
```

---

# Testing Application

A command-line utility named `test_approx` is provided for evaluating the Algorithm using randomly generated, large sparse matrices. It supports the following options:

```bash
usage: test_approx [-h] -d DIMENSION [-n NUM_TESTS] [-s SPARSITY] [-a] [-b] [-c] [-w] [-v] [-l] [--version]

The Varela Testing Application using randomly generated, large sparse matrices.

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
  -v, --verbose         anable verbose output
  -l, --log             enable file logging
  --version             show program's version number and exit
```

---

# Batch Execution

Batch execution allows you to solve multiple graphs within a directory consecutively.

To view available command-line options for the `batch_approx` command, use the following in your terminal or command prompt:

```bash
batch_approx -h
```

This will display the following help information:

```bash
usage: batch_approx [-h] -i INPUTDIRECTORY [-a] [-b] [-c] [-v] [-l] [--version]

Estimating the Minimum Vertex Cover with an approximation factor of < 2 for all undirected graphs encoded in DIMACS format
and stored in a directory.

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
