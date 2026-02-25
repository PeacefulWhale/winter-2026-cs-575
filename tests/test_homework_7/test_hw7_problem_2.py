import random

import networkx as nx
from typing import Tuple, Hashable, Set


def test_hw7_problem_2() -> None:
    """
    Problem 2: Create a graph and a partition of the nodes such that Q >= 0.95.
    Graph must have >= 5 vertices, >= 2 edges, and partition must have >= 2 sets.
    """

    # Build graph
    G: nx.Graph = nx.Graph()
    # TODO: Add vertices
    # TODO: Add edges
    VERT_COUNT = 10
    COMPONENT_COUNT = 20
    # Create Y components with X vertices each
    for i in range(COMPONENT_COUNT):
        G.add_nodes_from(range(i * VERT_COUNT, (i + 1) * VERT_COUNT))
        # Connect all the vertices in this component together
        for u in range(i * VERT_COUNT, (i + 1) * VERT_COUNT):
            for v in range(u + 1, (i + 1) * VERT_COUNT):
                G.add_edge(u, v)

    # TODO: Define partition
    # Just the two sides
    partition: Tuple[Set[Hashable], ...]
    # A bit of a long one liner... but it works...
    partition = tuple(set(range(i * VERT_COUNT, (i + 1) * VERT_COUNT)) for i in range(COMPONENT_COUNT))

    # For testing purposes, render out an image of the graph and save it to /workspaces/winter-2026-cs-575/output.png
    import matplotlib.pyplot as plt
    pos = nx.spring_layout(G)
    # Color nodes based on partition
    colors = ['lightblue', 'lightcoral', 'lightgreen', 'lightyellow', 'lightpink']
    node_colors = [colors[i % len(colors)] for i, node in enumerate(G.nodes()) 
                   for i, group in enumerate(partition) if node in group]
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color='gray', node_size=500)
    plt.savefig("/workspaces/winter-2026-cs-575/7_2_output.png")
    plt.close()

    # Basic structural checks
    assert isinstance(G, nx.Graph)
    assert G.number_of_nodes() >= 5
    assert G.number_of_edges() >= 2

    # Partition validity checks
    assert len(partition) >= 2
    assert all(len(group) > 0 for group in partition)
    union = set().union(*partition)
    assert union == set(G.nodes())
    assert sum(len(group) for group in partition) == len(union)

    # Modularity check
    q = nx.community.modularity(G, partition)
    assert q >= 0.95    # Q >= 0.95