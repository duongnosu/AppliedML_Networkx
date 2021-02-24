# Nhu Duong
# Assignment 2 - Network Connectivity

# In this assignment you will go through the process of importing
# and analyzing an internal email communication network between employees of a mid-sized manufacturing company.
# Each node represents an employee and
#  each directed edge between two nodes represents an individual email.
#  The left node represents the sender and the right node represents the recipient.
import networkx as nx
import pandas as pd
# Question 1
#
# Using networkx, load up the directed multigraph from `email_network.txt`. Make sure the node names are strings.
#
# *This function should return a directed multigraph networkx graph.*


def answer_one():

    G = nx.read_edgelist('email_network.txt', delimiter='\t', data=[
                         ('time', int)], create_using=nx.MultiDiGraph())

    return G


answer_one()
# Question 2

# How many employees and emails are represented in the graph from Question 1?
#
# *This function should return a tuple (#employees, #emails).*


def answer_two():

    # Your Code Here
    G = answer_one()
    num_emp = nx.number_of_nodes(G)
    num_email = nx.number_of_edges(G)

    return (num_emp, num_email)


answer_two()
# Question 3
#
# * Part 1. Assume that information in this company can only be exchanged through email.
#
#     When an employee sends an email to another employee, a communication channel has been created, allowing the sender to provide information to the receiver, but not vice versa.
#
#     Based on the emails sent in the data, is it possible for information to go from every employee to every other employee?
#
#
# * Part 2. Now assume that a communication channel established by an email allows information to be exchanged both ways.
#
#     Based on the emails sent in the data, is it possible for information to go from every employee to every other employee?
#
#
# *This function should return a tuple of bools (part1, part2).*


def answer_three():

    # Note: strongly_connected needs direction, weakly_connected needs only connections
    G = answer_one()
    s_con = nx.is_strongly_connected(G)
    w_con = nx.is_weakly_connected(G)
    return (s_con, w_con)


answer_three()
# Question 4

# How many nodes are in the largest (in terms of nodes) weakly connected component?
#
# *This function should return an int.*


def answer_four():

    # Your Code Here
    G = answer_one()
    # most efficient way
# https://networkx.org/documentation/networkx-1.10/reference/generated/networkx.algorithms.components.weakly_connected.weakly_connected_components.html
    return len(max(nx.weakly_connected_components(G), key=len))


answer_four()
# Question 5

# How many nodes are in the largest (in terms of nodes) strongly connected component?
#
# *This function should return an int*


def answer_five():

    # Your Code Here
    G = answer_one()
    # most efficient way
    return len(max(nx.strongly_connected_components(G), key=len))


answer_five()
# Question 6
#
# Using the NetworkX function strongly_connected_component_subgraphs, find the subgraph of nodes in a largest strongly connected component.
# Call this graph G_sc.
#
# *This function should return a networkx MultiDiGraph named G_sc.*


def answer_six():

    # Your Code Here
    G = answer_one()

    #G_sc = nx.strongly_connected_component_subgraphs(G, copy = True)
    G_sc = max(nx.strongly_connected_component_subgraphs(G), key=len)

    return G_sc


answer_six()


def answer_seven():

    # Your Code Here
    G_sc = answer_six()

    return nx.average_shortest_path_length(G_sc)


answer_seven()


def answer_eight():

    G_sc = answer_six()

    return nx.diameter(G_sc)


answer_eight()


def answer_nine():
    #periphery = (eccentricity == diameter)
    G_sc = answer_six()

    return set(nx.periphery(G_sc))


answer_nine()


def answer_ten():

    # center = (eccentricity == radius)
    G_sc = answer_six()

    return set(nx.center(G_sc))


answer_ten()
# Question 11
#
# Which node in G_sc is connected to the most other nodes by a shortest path of length equal to the diameter of G_sc?
#
# How many nodes are connected to this node?
#
#
# *This function should return a tuple (name of node, number of satisfied connected nodes).*


def answer_eleven():

    G_sc = answer_six()

    diameter = nx.diameter(G_sc)
    peripheries = nx.periphery(G_sc)

    answ = []
    # go through al lthe nodes in peripheries set, get the shortest_path, then add them to a set if their diamter = 3
    for node in peripheries:
        shortest_path = nx.shortest_path_length(G_sc, node).values()

        answ.append((node, len([val for val in shortest_path if val == diameter])))

    return max(answ)


answer_eleven()
# Question 12

# Suppose you want to prevent communication from flowing to the node that you found in the previous question from any node in the center of G_sc, what is the smallest number of nodes you would need to remove from the graph (you're not allowed to remove the node from the previous question or the center nodes)?
#
# *This function should return an integer.*


def answer_twelve():

    G_sc = answer_six()
    center = nx.center(G_sc)[0]
    mynode = answer_eleven()[0]

    return len(nx.minimum_node_cut(G_sc, center, mynode))


answer_twelve()


def answer_thirteen():

    G_sc = answer_six()

    G_un_sub = G_sc.to_undirected()

    G_un = nx.Graph(G_un_sub)
    return G_un


answer_thirteen()


def answer_fourteen():

    G_un = answer_thirteen()

    return (nx.transitivity(G_un), nx.average_clustering(G_un))


answer_fourteen()
