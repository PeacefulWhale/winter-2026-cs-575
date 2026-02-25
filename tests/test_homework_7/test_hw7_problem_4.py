import networkx as nx
from typing import Tuple, Hashable, Set


def test_hw7_problem_4() -> None:
    """
    Problem 4: Create a graph and a partition of the nodes such that 0.5 <= Q <= 0.6.
    Graph must have >= 12 vertices, >= 2 edges, and partition must have >= 3 sets.
    """

    # Build graph
    G = nx.Graph()
    VERT_COUNT = 4
    COMPONENT_COUNT = 3
    # Create Y components with X vertices each
    for i in range(COMPONENT_COUNT):
        G.add_nodes_from(range(i * VERT_COUNT, (i + 1) * VERT_COUNT))
        # Connect all the vertices in this component together
        for u in range(i * VERT_COUNT, (i + 1) * VERT_COUNT):
            for v in range(u + 1, (i + 1) * VERT_COUNT):
                G.add_edge(u, v)
    
    # So, to make this from 0.66 to somewhere between 0.5 and 0.6, I'm going to add some edges between the components until it drops enough
    G.add_edge(0, (VERT_COUNT * COMPONENT_COUNT) - 1)
    G.add_edge(1, (VERT_COUNT * COMPONENT_COUNT) - 2)
    G.add_edge(3, (VERT_COUNT * COMPONENT_COUNT) - 3)

    # TODO: Define partition
    # Just the two sides
    partition: Tuple[Set[Hashable], ...]
    # A bit of a long one liner... but it works...
    partition = tuple(set(range(i * VERT_COUNT, (i + 1) * VERT_COUNT)) for i in range(COMPONENT_COUNT))

    import matplotlib.pyplot as plt
    pos = nx.spring_layout(G)
    # Color nodes based on partition
    colors = ['lightblue', 'lightcoral', 'lightgreen', 'lightyellow', 'lightpink']
    node_colors = [colors[i % len(colors)] for i, node in enumerate(G.nodes()) 
                   for i, group in enumerate(partition) if node in group]
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color='gray', node_size=500)
    plt.savefig("/workspaces/winter-2026-cs-575/7_4_output.png")
    
    # Validate structure
    assert isinstance(G, nx.Graph)
    assert G.number_of_nodes() >= 12
    assert G.number_of_edges() >= 2

    # Validate partition
    assert len(partition) >= 3
    assert all(len(group) > 0 for group in partition)
    union = set().union(*partition)
    assert union == set(G.nodes())
    assert sum(len(group) for group in partition) == len(union)

    # Check modularity
    q = nx.community.modularity(G, partition)
    assert 0.5 <= q <= 0.6
