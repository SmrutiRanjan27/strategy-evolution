import random
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def plot_lattice(G,ax):
    colors = ('blue','red','green','y')
    pos = nx.get_node_attributes(G,'pos')
    key = nx.get_node_attributes(G,'id')
    '''
    for i in G.edges():
        x = np.array([pos[i[0]][0], pos[i[1]][0]])
        y = np.array([pos[i[0]][1], pos[i[1]][1]])
        ax.plot(x,y,c = "yellow",alpha=0.3)
    '''
    x1, y1,c = [], [], []
    for i in G.nodes():
        x1.append(G.nodes[i]['pos'][0])
        y1.append(G.nodes[i]['pos'][1])
        c.append(colors[key[i]])
    ax.scatter(x1,y1,marker="s",c=c,s=100)
    ax.set_axis_off()
    plt.xlim(min(pos.values())[0]-2,max(pos.values())[0]+2)
    plt.ylim(min(pos.values())[1]-2,max(pos.values())[1]+2)

def plot_coop(frac_list,ax,TOT_POP,label,color):
    l = len(frac_list)
    gen_list = np.arange(0,l,1)
    gen_list = gen_list/TOT_POP
    ax.set_xscale('log')
    ax.plot(gen_list,frac_list,label=label,color=color,linestyle='dashed')

