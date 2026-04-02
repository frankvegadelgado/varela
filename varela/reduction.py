import networkx as nx

def vc_to_vc_reduction(G, t):
    """
    Input: NetworkX graph G
    """

    Gp = nx.Graph()

    def star(node):
        nodes = [f"{node}_0", f"{node}_1", f"{node}_2", f"{node}_3"]
        u, v, w, z = nodes[0], nodes[1], nodes[2], nodes[3]
        Gp.add_edge(u, z)
        Gp.add_edge(v, z)
        Gp.add_edge(w, z)
        return nodes

    # create cliques + stars
    node_map = {}

    for v in G.nodes():
        copies = []

        for i in range(t):
            tri = star(f"{v}_copy{i}")
            copies.append(tri)

        node_map[v] = copies

    # edges
    for u, v in G.edges():
        for i in range(t):
            for k in range(3):
                Gp.add_edge(
                    node_map[u][i][k],
                    node_map[v][i][k]
                )

    return Gp
	
def extract_original_vc(vertex_cover, G, t):
    """
    Recover vertex cover of original graph
    """

    original_vc = set()

    for v in G.nodes():
        selected = 0

        for i in range(t):
            tri_nodes = [
                f"{v}_copy{i}_0",
                f"{v}_copy{i}_1",
                f"{v}_copy{i}_2"
            ]

            count = sum(1 for n in tri_nodes if n in vertex_cover)

            if count == 3:
                selected += 1

        # majority decision
        if selected > t // 2:
            original_vc.add(v)

    return original_vc	