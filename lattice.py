import networkx as nx 
import random
import numpy as np

#creating square lattice
def square_lattice(L):
    G = nx.Graph()
    POP = int(L**2)
    G.add_nodes_from([n for n in range(POP)])
    pos = {}
    for i in range(POP):
        pos[i] = ((i+1)%L, int(i/L))
        if (i+1)%L != 0:
            G.add_edge(i,i+1)
        else:
            G.add_edge(i,i-L+1)
        if i<(L-1)*L:
            G.add_edge(i,i+L)
        else:
            G.add_edge(i,i%L)
    nx.set_node_attributes(G,pos,'pos')
    return G

def set_population(G,category_list):
    node_list = [n for n in G.nodes()]
    for ind,category in enumerate(category_list):
        for _ in range(category):
            node = node_list.pop(random.randint(0,len(node_list)-1))
            G.nodes[node]['id'] = ind
            if ind%2 == 0:
                G.nodes[node]['nature'] = 1
            else:
                G.nodes[node]['nature'] = 0
            if ind == 2 or ind == 3:
                G.nodes[node]['punish'] = 1
            else:
                G.nodes[node]['punish'] = 0
    for i in G.nodes():
        G.nodes[i]['payoff'] = 0

def set_population_scalefree(G,portion,ind,pop_size,ind_0):
    nodes_degree = [G.degree(node) for node in G.nodes()]
    nodes_sort = np.argsort(nodes_degree)[::-1]
    n_size = int(pop_size*portion)
    rest_ind = [0,1,2,3]
    rest_ind.remove(ind)
    rest_ind.remove(ind_0)
    for i in range(pop_size):
        node = nodes_sort[i]
        if i <= n_size:
            G.nodes[node]['id'] = ind
        else:
            G.nodes[node]['id'] = random.choice(rest_ind)
        if G.nodes[node]['id']%2 == 0:
            G.nodes[node]['nature'] = 1
        else:
            G.nodes[node]['nature'] = 0
        if G.nodes[node]['id'] == 2 or G.nodes[node]['id'] == 3:
            G.nodes[node]['punish'] = 1
        else:
            G.nodes[node]['punish'] = 0
        G.nodes[node]['payoff'] = 0