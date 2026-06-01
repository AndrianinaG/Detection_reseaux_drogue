import random
import networkx as nx
import matplotlib.pyplot as plt
def generate_random_graph(N,p):
    aretes = []
    for u in range(N):
        for v in range(N):
            if random.random() < p:
                aretes.append((u,v))
    return aretes
