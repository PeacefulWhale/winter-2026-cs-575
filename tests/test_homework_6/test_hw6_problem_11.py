import matplotlib.pyplot as plt
from network_utilities import adjacency_list_to_digraph
import networkx as nx
import numpy as np 

def test_homework_problem_ev_vs_katz_collapse() -> None:
    """
    Students should design a directed graph with >= 6 nodes such that:
    - Eigenvector centrality assigns near-zero values to at least 3 nodes
    - Katz centrality assigns no near-zero values
    """
    G = nx.DiGraph()
    G.add_edges_from([
        # We need 3 nodes that have an in-degree of 0
        (0, 1), (2, 1), (3, 1),  # Node 1 gets some centrality, the others get none
        # Connect the rest together in a triangle
        (1, 4), (4, 5), (5, 1)  # Nodes 1, 4, 5 form a strongly connected component
    ])
    # We have to make a graph of this for the homework
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    plt.savefig("/workspaces/winter-2026-cs-575/6_11_output.png")
    plt.close()
    # Create graph (STUDENT IMPLEMENTS THIS)
    # adjacency_list: dict[int, set[int]] = {
    #     # Example structure students must design
    #     # 1: {...},
    #     # ...
    # }
    # G = adjacency_list_to_digraph(adjacency_list)

    # Basic structural checks
    assert isinstance(G, nx.DiGraph)
    assert G.number_of_nodes() >= 6

    # Compute centralities
    eig = nx.eigenvector_centrality(G, max_iter=2000)
    katz = nx.katz_centrality_numpy(G, alpha=0.1, beta=1.0)

    eig_vals = np.array(list(eig.values()))
    katz_vals = np.array(list(katz.values()))

    # Count near-zero eigenvector entries
    near_zero_eig = np.sum(eig_vals < 1e-3)

    # At least 3 nodes should collapse under eigenvector centrality
    assert near_zero_eig >= 3

    # Katz should assign no near-zero values
    assert np.all(katz_vals > 1e-3)