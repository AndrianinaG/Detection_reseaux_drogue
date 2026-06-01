import random
import math
from graphe import generate_random_graph
from algo1_nettoyage import nettoyage
from algo2_classification import (
    colorier_graphe,
    identifier_sous_graphes,
    detecter_cliques
)
from visualisation import visualiser

if __name__ == "__main__":

    N = random.randint(20, 50)
    P = round(math.ceil(math.log(N)) / N, 3)

    #Étape 1 : génération
    print(" Génération de G ")
    aretes = generate_random_graph(N, P)
    print(f"  {len(aretes)} arêtes brutes générées")

    # Étape 2 : nettoyage
    print("\n Algorithme 1 : nettoyage")
    G_prime = nettoyage(aretes, N)
    print(f"  Sommets : {G_prime.number_of_nodes()}")
    print(f"  Arêtes  : {G_prime.number_of_edges()}")

    #Étape 3 : classification
    print("\nAlgorithme 2 : classification")
    couleurs              = colorier_graphe(G_prime)
    sous_graphes          = identifier_sous_graphes(G_prime)
    cliques, appartenance = detecter_cliques(G_prime, taille_min=3)

    #Etape 4 : visualisation
    print("\nVisualisation")
    visualiser(
        G_prime,
        couleurs,
        cliques,
        titre=f"G'({N}, {P}) — coloration + cliques"
    )