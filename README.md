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

Vertex Cover Found `3, 4, 5`: Nodes `3`, `4`, and `5` constitute an optimal solution.

---

# Approximate Vertex Cover Algorithm Analysis

## Overview

The algorithm works as follows:

1. It first checks if the graph is empty or has no edges, returning an empty set in these cases.
2. It then iterates over all connected components of the graph.
3. For each connected component, it finds a maximal independent set.
4. The vertex cover for each component is computed as the complement of the maximal independent set.
5. The final vertex cover is the union of all component-wise vertex covers.

## Runtime Analysis

The runtime of this algorithm can be broken down as follows:

1. Checking for empty graph or no edges: $O(1)$
2. Finding connected components: $O(|V| + |E|)$, where $|V|$ is the number of vertices and $|E|$ is the number of edges.
3. For each component:
   - Creating a subgraph: $O(|V| + |E|)$
   - Finding a maximal independent set: $O(|V| + |E|)$
   - Computing the complement: $O(|V|)$
   - Updating the final set: $O(|V|)$

The total runtime is dominated by the operations on connected components, which are performed at most once for each vertex and edge. Therefore, the overall time complexity is $O(|V| + |E|)$.

## Correctness

The algorithm produces a valid vertex cover with an approximation ratio of less than 2. Here's why:

1. The algorithm correctly handles edge cases (empty graph or no edges).
2. For each connected component, it finds a maximal independent set. By definition, a maximal independent set is a set of vertices where no two vertices are adjacent, and no more vertices can be added while maintaining this property.
3. The complement of a maximal independent set is a valid vertex cover. This is because any edge not covered by the complement would have both its endpoints in the independent set, which contradicts the definition of an independent set.
4. The union of vertex covers for all components forms a valid vertex cover for the entire graph.
5. The approximation ratio is less than 2 because:
   - The size of a maximal independent set is at least half the size of a maximum independent set.
   - The complement of a maximum independent set is a minimum vertex cover.
   - Therefore, the size of our approximate vertex cover is at most twice the size of the minimum vertex cover.

In conclusion, this algorithm provides a polynomial-time 2-approximation for the vertex cover problem, which is consistent with the known bounds for this NP-hard problem.

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
   testMatrix1: Vertex Cover Found 3, 4, 5
   ```

   This indicates nodes `3, 4, 5` form a vertex cover.

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

Estimating the Minimum Vertex Cover with an approximation factor of less than 2 encoded for undirected graph in DIMACS format.

options:
  -h, --help            show this help message and exit
  -i INPUTFILE, --inputFile INPUTFILE
                        input file path
  -a, --approximation   enable comparison with another polynomial-time approximation approach within a factor of at most 2
  -b, --bruteForce      enable comparison with the exponential-time brute-force approach
  -c, --count           calculate the size of the vertex cover
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

Estimating the Minimum Vertex Cover with an approximation factor of less than 2 for all undirected graphs encoded in DIMACS format and stored in a directory.

options:
  -h, --help            show this help message and exit
  -i INPUTDIRECTORY, --inputDirectory INPUTDIRECTORY
                        Input directory path
  -a, --approximation   enable comparison with another polynomial-time approximation approach within a factor of at most 2
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
  -a, --approximation   enable comparison with another polynomial-time approximation approach within a factor of at most 2
  -b, --bruteForce      enable comparison with the exponential-time brute-force approach
  -c, --count           calculate the size of the vertex cover
  -w, --write           write the generated random matrix to a file in the current directory
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
