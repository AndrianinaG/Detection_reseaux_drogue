import networkx as nx
from algo1_nettoyage import nettoyage
from graphe import generate_random_graph

def colorier_graphe(G):

    sorted_sommet = sorted(
        G.nodes(), 
        key=lambda x: G.degree(x), 
        reverse=True
    )

    couleurs = {}

    for sommet in sorted_sommet:

        couleurs_voisins = {
            couleurs[voisin] 
            for voisin in G.neighbors(sommet) 
            if voisin in couleurs   
        }

        couleur = 0
        while couleur in couleurs_voisins:
            couleur += 1

        couleurs[sommet] = couleur

    return couleurs

def identifier_sous_graphes(G):
    visites     = set()
    sous_graphes = []
    identifiant  = 0

    for depart in G.nodes():
        if depart in visites:
            continue

        # Parcours en largeur depuis ce sommet
        composante = set()
        file       = [depart]

        while file:
            sommet = file.pop(0)

            if sommet in visites:
                continue

            visites.add(sommet)
            composante.add(sommet)

            for voisin in G.neighbors(sommet):
                if voisin not in visites:
                    file.append(voisin)

        # Stocker les infos de cette composante
        sous_graphes.append({
            "id"       : identifiant,
            "noeuds"   : sorted(composante),
            "taille"   : len(composante),
            "nb_aretes": G.subgraph(composante).number_of_edges()
        })
        identifiant += 1

    return sous_graphes

def detecter_cliques(G, taille_min=3):

    toutes_cliques = []

    def bron_kerbosch(en_cours, candidats, exclus):

        # Si plus aucun candidat ni exclu alors clique maximale trouvée
        if not candidats and not exclus:
            if len(en_cours) >= taille_min:
                toutes_cliques.append(sorted(en_cours))
            return

        for sommet in list(candidats):

            # Voisins de ce sommet
            voisins = set(G.neighbors(sommet))

            # On approfondit avec ce sommet dans la clique
            bron_kerbosch(
                en_cours  | {sommet},      # on ajoute le sommet
                candidats & voisins,       # candidats = voisins communs
                exclus    & voisins        # exclus    = voisins communs
            )

            # Ce sommet est traité : on le déplace dans exclus
            candidats = candidats - {sommet}
            exclus    = exclus    | {sommet}

    # Lancement initial : clique vide, tous les sommets candidats
    bron_kerbosch(
        en_cours  = set(),
        candidats = set(G.nodes()),
        exclus    = set()
    )

    # Trier les cliques par taille décroissante
    cliques = sorted(toutes_cliques, key=len, reverse=True)

    # Index inverse : à quelles cliques appartient chaque sommet ?
    appartenance = {n: [] for n in G.nodes()}
    for i, c in enumerate(cliques):
        for n in c:
            appartenance[n].append(i)

    return cliques, appartenance