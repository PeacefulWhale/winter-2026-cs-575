import networkx as nx
from networkx import edge_betweenness_centrality as betweenness


def test_hw7_problem_5() -> None:
    """
    Problem 5: Create a graph in which the edges (0,1), (2,3), (4,5)
    are ordered by edge betweenness from highest to lowest in that exact order.
    """

    # Build graph
    G: nx.Graph = nx.Graph()
    # TODO: Add vertices
    # TODO: Add edges
    G.add_edges_from([(0,1), (2,3), (4,5)])
    # I'm going to do it the lazy way, by just adding a lot of nodes to either side lol
    G.add_edges_from([('a', 0), ('b', 0), ('c', 1), ('d', 1)])
    G.add_edges_from([('e', 2), ('f', 3)])

    import matplotlib.pyplot as plt
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, edge_color='gray', node_size=500)
    plt.savefig("/workspaces/winter-2026-cs-575/7_5_output.png")
    plt.close()

    # Validate required edges exist
    required_edges = [(0, 1), (2, 3), (4, 5)]
    for u, v in required_edges:
        assert G.has_edge(u, v), f"Missing required edge ({u}, {v})"

    # Compute edge betweenness
    edge_scores = betweenness(G)

    def score(u: int, v: int) -> float:
        return edge_scores.get((u, v), edge_scores.get((v, u)))

    scores = [score(u, v) for u, v in required_edges]
    assert all(s is not None for s in scores), "Failed to find all required edges"

    # Check ordering: highest to lowest in the given order
    assert scores[0] > scores[1] > scores[2]
