import networkx as nx
from graphe import generate_random_graph

#Trouver les composantes connexes par un parcours en largeur
def trouver_composantes(G):
    visited = set()
    composantes = []

    for depart in G.nodes():
        if depart in visited:
            continue

        composante = set()
        file_FIFO = [depart]

        while file_FIFO:
            sommet = file_FIFO.pop(0)
            if sommet in visited:
                continue

            visited.add(sommet)
            composante.add(sommet)

            for voisin in G.neighbors(sommet):
                if voisin not in visited:
                    file_FIFO.append(voisin)
        
        composantes.append(composante)

    return composantes

#Nettoyage du graphe
def nettoyage(aretes, N):
    G = nx.Graph()
    G.add_nodes_from(range(N))

    for u, v in aretes:
        if u != v:
            G.add_edge(u, v)

    composantes = trouver_composantes(G)

    if len(composantes) > 1:
        noeud_ref = list(composantes[0])[0]
        for composante in composantes[1:]:
            noeud_composante = list(composante)[0]
            G.add_edge(noeud_ref, noeud_composante)
    
    return G

    