import networkx as nx
from typing import Tuple, Hashable, Set


def test_hw7_problem_3() -> None:
    """
    Problem 3: Create a graph and a partition of the nodes such that Q = -1/2.
    Graph must have >= 5 vertices, >= 2 edges, and partition must have >= 2 sets.
    """

    # Build graph
    G: nx.Graph = nx.Graph()
    # TODO: Add vertices
    # TODO: Add edges
    VERT_COUNT = 10
    PARTITION_COUNT = 2
    G.add_nodes_from(range(VERT_COUNT * PARTITION_COUNT))
    # Make it so every node in a partition is connected to every node outside that partition, but no nodes within it's own partition
    for i in range(PARTITION_COUNT):
        for u in range(i * VERT_COUNT, (i + 1) * VERT_COUNT):
            for v in range(0, PARTITION_COUNT * VERT_COUNT):
                if v < i * VERT_COUNT or v >= (i + 1) * VERT_COUNT:
                    G.add_edge(u, v)


    # TODO: Define partition
    partition: Tuple[Set[Hashable], ...] = ()
    partition = tuple(set(range(i * VERT_COUNT, (i + 1) * VERT_COUNT)) for i in range(PARTITION_COUNT))

    # For testing purposes, render out an image of the graph and save it to /workspaces/winter-2026-cs-575/output.png
    import matplotlib.pyplot as plt
    pos = nx.spring_layout(G)
    # Color nodes based on partition
    colors = ['lightblue', 'lightcoral', 'lightgreen', 'lightyellow', 'lightpink']
    node_colors = [colors[i % len(colors)] for i, node in enumerate(G.nodes()) 
                   for i, group in enumerate(partition) if node in group]
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color='gray', node_size=500)
    plt.savefig("/workspaces/winter-2026-cs-575/7_3_output.png")
    plt.close()

    # Validate structure
    assert isinstance(G, nx.Graph)
    assert G.number_of_nodes() >= 5
    assert G.number_of_edges() >= 2

    # Validate partition
    assert len(partition) >= 2
    assert all(len(group) > 0 for group in partition)
    union = set().union(*partition)
    assert union == set(G.nodes())
    assert sum(len(group) for group in partition) == len(union)

    # Check modularity
    q = nx.community.modularity(G, partition)
    assert abs(q - (-0.5)) < 0.01  # Q ≈ -1/2
