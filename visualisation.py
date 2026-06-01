import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

def visualiser(G, couleurs, cliques, titre="G'"):

    palette = [
        "#378ADD", "#1D9E75", "#D85A30", "#7F77DD",
        "#BA7517", "#D4537E", "#639922", "#E24B4A",
    ]

    # Tous les sommets qui appartiennent à au moins une clique
    noeuds_cliques = {n for c in cliques for n in c}

    # Une propriété par sommet, dans le même ordre que G.nodes()
    node_colors   = [palette[couleurs[n] % len(palette)]
                     for n in G.nodes()]

    node_borders  = ["#E24B4A" if n in noeuds_cliques else "#888780"
                     for n in G.nodes()]

    node_sizes    = [300 + G.degree(n) * 80
                     for n in G.nodes()]

    border_widths = [3.0 if n in noeuds_cliques else 0.8
                     for n in G.nodes()]
    
    # Trouver les arêtes qui relient deux membres d'une même clique
    aretes_cliques = set()
    for c in cliques:
        c_set = set(c)
        for u, v in G.edges():
            if u in c_set and v in c_set:
                aretes_cliques.add((min(u, v), max(u, v)))

    # Une couleur et une épaisseur par arête
    edge_colors = []
    edge_widths = []

    for u, v in G.edges():
        if (min(u, v), max(u, v)) in aretes_cliques:
            edge_colors.append("#E24B4A")  # rouge
            edge_widths.append(2.5)
        else:
            edge_colors.append("#cccccc")  # gris clair
            edge_widths.append(0.8)

    # Calcul des positions des noeuds
    pos = nx.spring_layout(G, seed=42)

    fig, ax = plt.subplots(figsize=(11, 7))

    nx.draw_networkx_edges(
        G, pos, ax=ax,
        edge_color=edge_colors,
        width=edge_widths,
        alpha=0.7
    )
    nx.draw_networkx_nodes(
        G, pos, ax=ax,
        node_color=node_colors,
        edgecolors=node_borders,
        linewidths=border_widths,
        node_size=node_sizes
    )
    nx.draw_networkx_labels(
        G, pos, ax=ax,
        font_size=9,
        font_color="white",
        font_weight="bold"
    )

    nb_couleurs = len(set(couleurs.values()))
    legende = [
        mpatches.Patch(
            color=palette[c % len(palette)],
            label=f"Classe {c}"
        )
        for c in range(nb_couleurs)
    ]
    legende.append(
        mpatches.Patch(
            facecolor="white",
            edgecolor="#E24B4A",
            linewidth=2,
            label="Dans une clique"
        )
    )

    ax.legend(handles=legende, loc="upper left", fontsize=9)
    ax.set_title(titre, fontsize=13, fontweight="bold")
    ax.axis("off")
    plt.tight_layout()
    plt.show()   