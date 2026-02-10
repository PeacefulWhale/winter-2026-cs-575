import networkx as nx


def test_hw7_problem_2() -> None:
    """
    Students should design a graph with >= 50 nodes and >= 25 edges such that
    the modularity of their partition is in the range [0.95, 1.0].
    """

    # Build graph (STUDENT IMPLEMENTS THIS)
    G: nx.Graph = nx.Graph()
    G.add_nodes_from(range(50))

    # TODO: Add edges
    edges: list[tuple[int, int]] = [
        # (u, v),
    ]
    G.add_edges_from(edges)

    # TODO: Define partition
    partition: tuple[set[int], ...] = (
        set(G.nodes()),
    )

    # Basic structural checks
    assert isinstance(G, nx.Graph)
    assert G.number_of_nodes() >= 50
    assert G.number_of_edges() >= 25

    # Partition validity checks
    assert len(partition) >= 2
    assert all(len(group) > 0 for group in partition)
    union = set().union(*partition)
    assert union == set(G.nodes())
    assert sum(len(group) for group in partition) == len(union)

    # Modularity check
    q = nx.community.modularity(G, partition)
    assert 0.95 <= q <= 1.0