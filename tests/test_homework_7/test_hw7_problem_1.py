import networkx as nx
from typing import Tuple, Hashable, Set
import random


def test_hw7_problem_1() -> None:
    """
    Problem 1: Create a graph and a partition of the nodes such that Q = 0.
    Graph must have >= 5 vertices, >= 2 edges, and partition must have >= 2 sets.
    """

    # Build graph
    G: nx.Graph = nx.Graph()
    # TODO: Add vertices
    VERT_COUNT = 1000
    G.add_nodes_from(range(VERT_COUNT))

    # TODO: Add edges
    # Just randomly connect vertices together to create a graph with no community structure
    for i in range(VERT_COUNT * 5):
        y = random.randint(0, VERT_COUNT - 1)
        x = random.randint(0, VERT_COUNT - 1)
        if x != y:
            G.add_edge(x, y)

    # TODO: Define partition
    partition: Tuple[Set[Hashable], ...] = ()
    cut_size, partition = nx.approximation.randomized_partitioning(G, 42)

    # Okay, so we need to do this too:
    print(f"Total Edges: {G.number_of_edges()}, Total Nodes: {G.number_of_nodes()}")
    # The edges that connect vertices within groups in the partition
    edges_within_groups = 0
    for u, v in G.edges():
        if (u in partition[0] and v in partition[0]) or (u in partition[1] and v in partition[1]):
            edges_within_groups += 1
    print(f"Edges within groups: {edges_within_groups}")
    # The edges that connect vertices across groups in the partition
    edges_across_groups = 0
    for u, v in G.edges():
        if (u in partition[0] and v in partition[1]) or (u in partition[1] and v in partition[0]):
            edges_across_groups += 1
    print(f"Edges across groups: {edges_across_groups}")

    # The number of groups in the partition
    num_groups = len(partition)
    print(f"Number of groups in partition: {num_groups}")

    # For testing purposes, render out an image of the graph and save it to /workspaces/winter-2026-cs-575/output.png
    import matplotlib.pyplot as plt
    pos = nx.spring_layout(G)
    # Color nodes based on partition
    colors = ['lightblue', 'lightcoral', 'lightgreen', 'lightyellow', 'lightpink']
    node_colors = [colors[i % len(colors)] for i, node in enumerate(G.nodes()) 
                   for i, group in enumerate(partition) if node in group]
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color='gray', node_size=500)
    plt.savefig("/workspaces/winter-2026-cs-575/7_1_output.png")

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
    assert abs(q - 0.0) < 0.01  # Q ≈ 0
