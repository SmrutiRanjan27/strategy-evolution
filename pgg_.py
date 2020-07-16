import networkx as nx 
import numpy as np
import random   

def createGroup(Graph,node):
    group = []
    group.append(node)
    for neighbor in Graph.neighbors(node):
        group.append(neighbor)
    return group

def group_payoff(Graph,node,node_center,a,cost,fine,r,groups,coop_no, punish_no):
    pay = 0
    sub_group = groups[node_center]
    nature = Graph.nodes[node]['nature']
    punish = Graph.nodes[node]['punish']
    G = len(sub_group)
    if G > 1:
        cooperators, punishers = coop_no[node_center], punish_no[node_center]
        defectors = G - cooperators
        pay += cooperators*r*a/G
        if nature:
            pay -= a
            pay -= punish*cost*defectors/(G-1)
        else:
            pay -= fine*(punishers-punish)/(G-1)
            pay -= punish*cost*(defectors-1)/(G-1)
    return pay

def payoff(Graph, node, a, cost, fine,r,groups,coop_no, punish_no):
    group = groups[node]
    pay_list = {}
    for member in group:
        pay_list[member] = group_payoff(Graph,node,member,a,cost,fine,r,groups,coop_no, punish_no)
    return pay_list

def change(id_list):
    if not id_list[0]%2 and id_list[1]%2:
        c_value = -1
    elif id_list[0]%2 and not id_list[1]%2:
        c_value = 1
    else:
        c_value = 0
    if id_list[0] in [0,1] and id_list[1] in [2,3]:
        p_value = 1
    elif id_list[0] in [2,3] and id_list[1] in [0,1]:
        p_value = -1
    else:
        p_value = 0
    return c_value, p_value

def playPGG(Graph, a, cost, fine,r,groups,coop_no, punish_no, id_list, ch=True,node = 'all'):
    if node == 'all':
        for node_ in Graph.nodes():
            pay_list = payoff(Graph,node_, a, cost, fine,r,groups,coop_no, punish_no)
            Graph.nodes[node_]['pay_list'] = pay_list
            Graph.nodes[node_]['payoff'] = sum(pay_list.values())
    else:
        if ch:
            group = groups[node]
            node_list = []
            c_value, p_value = change(id_list)
            for member in group:
                coop_no[member] += c_value
                punish_no[member] += p_value
                sub_group = groups[member]
                for member_ in sub_group:
                    Graph.nodes[member_]['pay_list'][member] = group_payoff(Graph,member_,member,a,cost,fine,r,groups,coop_no, punish_no)
                    node_list.append(member_)
            for node in np.unique(node_list):
                Graph.nodes[node]['payoff'] = sum(Graph.nodes[node]['pay_list'].values())
    return coop_no, punish_no

def update_strategy(Graph,K,pop,nodes,neighbors):
    x = random.choice(nodes)
    y = random.choice(neighbors[x])
    Px = Graph.nodes[x]['payoff']
    Py = Graph.nodes[y]['payoff']
    W = 1./(1+np.exp((Py-Px)/K))
    change = False
    id_list = []
    if random.random()<W:
        if Graph.nodes[y]['id'] != Graph.nodes[x]['id']:
            id_list = [Graph.nodes[y]['id'],Graph.nodes[x]['id']]
            Graph.nodes[y]['nature'] = Graph.nodes[x]['nature']
            Graph.nodes[y]['punish'] = Graph.nodes[x]['punish']
            pop[Graph.nodes[y]['id']] -= 1
            pop[Graph.nodes[x]['id']] += 1
            Graph.nodes[y]['id'] = Graph.nodes[x]['id']
            change = True
    return pop,y, change, id_list