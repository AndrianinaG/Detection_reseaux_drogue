# Détection de fraude par analyse de graphe

Projet Python de détection de comportements frauduleux ou délinquants à partir d'un graphe aléatoire G(N, P).  
Le pipeline transforme un graphe brut en graphe propre, puis l'analyse par coloration, identification de sous-graphes et détection de cliques.

---

## Structure du projet

```
Detection-fraude/
├── graphe.py                # Génération du graphe aléatoire brut G(N, P)
├── algo1_nettoyage.py       # Algorithme 1 : nettoyage G → G'
├── algo2_classification.py  # Algorithme 2 : coloration, sous-graphes, cliques
├── visualisation.py         # Affichage du graphe G' avec Matplotlib
├── main.py                  # Point d'entrée — orchestre tout le pipeline
└── README.md
```

---

## Prérequis

Python 3.10 ou supérieur.

Installer les dépendances :

```bash
pip install networkx matplotlib
```

---

## Lancement

```bash
python main.py
```

Le programme génère automatiquement un graphe de taille aléatoire entre 20 et 50 sommets, avec une probabilité d'arête calculée par `ceil(log(N)) / N` pour garantir un graphe suffisamment dense.

---

## Pipeline complet

```
G(N, P) brut  →  Algorithme 1  →  G' propre  →  Algorithme 2  →  Résultats
   graphe.py      algo1_...        connexe       algo2_...       + visualisation
```

### Étape 1 — `graphe.py`

Génère une liste brute d'arêtes `(u, v)` avec :
- des **boucles** possibles `(u, u)`
- des **multi-arêtes** possibles `(u, v)` en double
- des **composantes non connexes** possibles

```python
generate_random_graph(N, p)
# Retourne : liste de tuples [(u, v), ...]
```

### Étape 2 — `algo1_nettoyage.py`

Transforme la liste brute en graphe `G'` propre en 4 passes :

| Passe | Action | Mécanisme |
|---|---|---|
| 1 | Suppression des boucles | `if u != v` |
| 2 | Suppression des multi-arêtes | `nx.Graph` = unicité automatique |
| 3 | Non-orientation | `nx.Graph` = non orienté par défaut |
| 4 | Connexion des composantes | BFS maison + pont minimal |

Le BFS maison (`trouver_composantes`) parcourt le graphe sans utiliser `nx.connected_components`.

```python
nettoyage(aretes, N)
# Retourne : nx.Graph connexe, non orienté, sans boucle, arête unique
```

### Étape 3 — `algo2_classification.py`

Trois analyses sur G' :

**Coloration — `colorier_graphe(G)`**  
Algorithme Welsh-Powell : trie les sommets par degré décroissant, attribue la plus petite couleur non utilisée par les voisins. Deux sommets adjacents ont toujours des couleurs différentes.

**Sous-graphes — `identifier_sous_graphes(G)`**  
BFS maison qui identifie chaque composante connexe et retourne ses informations (noeuds, taille, nombre d'arêtes).

**Cliques — `detecter_cliques(G, taille_min=3)`**  
Algorithme de Bron-Kerbosch récursif. Une clique = groupe de sommets tous mutuellement connectés. Retourne les cliques et un index d'appartenance par sommet.

### Étape 4 — `visualisation.py`

Affiche G' avec trois encodages visuels simultanés :

| Encodage | Signification |
|---|---|
| Couleur du nœud | Classe de coloration |
| Bordure rouge épaisse | Sommet appartenant à une clique |
| Taille du nœud | Degré (plus connecté = plus grand) |
| Arête rouge | Relie deux membres d'une même clique |

---

## Paramètres ajustables

Dans `main.py` :

```python
N = random.randint(20, 50)          # Nombre de sommets
P = round(math.ceil(math.log(N)) / N, 3)  # Probabilité d'arête
```

Dans l'appel à `detecter_cliques` :

```python
cliques, appartenance = detecter_cliques(G_prime, taille_min=3)
# taille_min : taille minimale pour retenir une clique
```

---

## Exemple de sortie console

```
 Génération de G
  187 arêtes brutes générées

 Algorithme 1 : nettoyage
  Sommets : 35
  Arêtes  : 98

Algorithme 2 : classification
  Coloration : 4 couleur(s) utilisée(s)
  Cliques (taille >= 3) : 6 trouvée(s)

Visualisation
```

---

## Détail des fonctions

| Fichier | Fonction | Paramètres | Retour |
|---|---|---|---|
| `graphe.py` | `generate_random_graph(N, p)` | N sommets, p probabilité | `list[tuple]` |
| `algo1_nettoyage.py` | `trouver_composantes(G)` | nx.Graph | `list[set]` |
| `algo1_nettoyage.py` | `nettoyage(aretes, N)` | liste arêtes, nb sommets | `nx.Graph` |
| `algo2_classification.py` | `colorier_graphe(G)` | nx.Graph | `dict {sommet: couleur}` |
| `algo2_classification.py` | `identifier_sous_graphes(G)` | nx.Graph | `list[dict]` |
| `algo2_classification.py` | `detecter_cliques(G, taille_min)` | nx.Graph, int | `(list[list], dict)` |
| `visualisation.py` | `visualiser(G, couleurs, cliques, titre)` | nx.Graph, dicts | affichage Matplotlib |
