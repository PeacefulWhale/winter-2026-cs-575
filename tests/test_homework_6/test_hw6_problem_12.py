import matplotlib.pyplot as plt
from network_utilities import adjacency_list_to_digraph
import networkx as nx
import numpy as np 

def test_homework_problem_katz_vs_pagerank() -> None:
    """
    Students should design a directed graph with >= 8 nodes such that:
    - Katz centrality is approximately uniform across nodes
    - PageRank distinguishes between hub nodes and nodes pointed to by hubs
    """
    G = nx.DiGraph()
    G.add_edges_from([
        # Hub node 0, 1, 2 which many point to
        (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
        (3, 1), (4, 1), (5, 1),
        (3, 2), (4, 2),
        # Then have some connections between the rest to make katz more uniform
        (3, 7), (3, 6),
        (4, 3),
        (5, 6),
        (6, 5),
        (7, 7), # Self-loop to increase Katz centrality of node 7
    ])

    # Compute centralities
    katz = nx.katz_centrality_numpy(G, alpha=0.1, beta=1.0)
    pagerank = nx.pagerank(G, alpha=0.85)

    katz_vals = np.array(list(katz.values()))
    pr_vals = np.array(list(pagerank.values()))

    pos = nx.spring_layout(G)
    # Color them according to PageRank for visualization
    nx.draw(G, pos, with_labels=True, node_color=pr_vals, cmap=plt.cm.Blues)
    plt.savefig("/workspaces/winter-2026-cs-575/6_12_output.png")
    plt.close()

    # # Create graph (STUDENT IMPLEMENTS THIS)
    # adjacency_list: dict[int, set[int]] = {
    #     # Example structure students must design
    #     # 1: {...},
    #     # ...
    # }
    # G = adjacency_list_to_digraph(adjacency_list)

    # Basic structural checks
    assert isinstance(G, nx.DiGraph)
    assert G.number_of_nodes() >= 8

    # Katz should be approximately uniform
    # (small variance relative to mean)
    assert np.std(katz_vals) < 0.2 * np.mean(katz_vals)

    # PageRank should NOT be uniform
    assert np.std(pr_vals) > 0.2 * np.mean(pr_vals)

    # There should exist a hub node whose PageRank is higher
    max_pr = np.max(pr_vals)
    min_pr = np.min(pr_vals)
    assert max_pr > 2 * min_pr
