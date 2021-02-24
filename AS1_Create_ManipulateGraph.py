# Nhu Duong
# # Assignment 1 - Creating and Manipulating Graphs
#
# Eight employees at a small company were asked to choose 3 movies that they would most enjoy watching for the upcoming company movie night. These choices are stored in the file `Employee_Movie_Choices.txt`.
#
# A second file, `Employee_Relationships.txt`, has data on the relationships between different coworkers.
#
# The relationship score has value of `-100` (Enemies) to `+100` (Best Friends). A value of zero means the two employees haven't interacted or are indifferent.
#
# Both files are tab delimited.
#
import networkx as nx
import pandas as pd
import numpy as np
import pprint
from networkx.algorithms import bipartite

#pp = pprint.PrettyPrinter(width=5, compact=True)
# This is the set of employees
employees = set(['Pablo',
                 'Lee',
                 'Georgia',
                 'Vincent',
                 'Andy',
                 'Frida',
                 'Joan',
                 'Claude'])

# This is the set of movies
movies = set(['The Shawshank Redemption',
              'Forrest Gump',
              'The Matrix',
              'Anaconda',
              'The Social Network',
              'The Godfather',
              'Monty Python and the Holy Grail',
              'Snakes on a Plane',
              'Kung Fu Panda',
              'The Dark Knight',
              'Mean Girls'])


# you can use the following function to plot graphs
# make sure to comment it out before submitting to the autograder
def plot_graph(G, weight_name=None):
    '''
    G: a networkx G
    weight_name: name of the attribute for plotting edge weights (if G is weighted)
    '''
    %matplotlib notebook
    import matplotlib.pyplot as plt

    plt.figure()
    pos = nx.spring_layout(G)
    edges = G.edges()
    weights = None

    if weight_name:
        weights = [int(G[u][v][weight_name]) for u, v in edges]
        labels = nx.get_edge_attributes(G, weight_name)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        nx.draw_networkx(G, pos, edges=edges, width=weights)
    else:
        nx.draw_networkx(G, pos, edges=edges)

# Playing around to see the data look like
# #!cat Employee_Relationships.txt
# G_emprela = nx.read_edgelist('Employee_Relationships.txt', data=[('Relationship', int)], create_using=nx.MultiDiGraph())
# G_emprela.edges(data=True)
# #nx.set_edge_attributes(G_emprela, values = data, name = 'Relationship')

# df = pd.DataFrame(G_emprela.edges(data=True), columns=['Name1', 'Name2', 'Relationship'])
# df['Relationship'] = df['Relationship'].map(lambda x: x['Relationship'])
# df.set_index(['Name1','Name2'], inplace = True)
# # nx.draw_networkx(G_emprela)
# pos = nx.spring_layout(G_emprela)
# labels = nx.get_edge_attributes(G_emprela,'Relationship')
# nx.draw_networkx_edge_labels(G_emprela,pos,edge_labels=labels)
###
# Question 1

# Using NetworkX, load in the bipartite graph from `Employee_Movie_Choices.txt` and return that graph.
#
# *This function should return a networkx graph with 19 nodes and 24 edges*


def answer_one():

    G_empC = pd.read_csv('Employee_Movie_Choices.txt', sep='\t',
                         names=['Employee', 'Movie'], skiprows=1)
    # For older networkx, use
    #G_empC = nx.from_pandas_dataframe(G_empC, 'Employee', 'Movie')

    # check number of nodes and edges
    # print(G_empC.number_of_nodes(),G_empC.number_of_edges())
    # pprint.pprint(list(G_empC.edges))
    return G_empC


answer_one()

# Question 2

# Using the graph from the previous question, add nodes attributes named `'type'` where movies have the value `'movie'` and employees have the value `'employee'` and return that graph.
#
# *This function should return a networkx graph with node attributes `{'type': 'movie'}` or `{'type': 'employee'}`*


def answer_two():

    # Your Code Here
    G_empC_type = answer_one()
    G_empC_type.add_nodes_from(employees, bipartite=0, type='employee')
    G_empC_type.add_nodes_from(movies, bipartite=1, type='movie')

    # verify type
    # pprint.pprint(list(G_empC_type.edges))
    return G_empC_type


answer_two()
# Question 3
#
# Find a weighted projection of the graph from `answer_two` which tells us how many movies different pairs of employees have in common.
#
# *This function should return a weighted projected graph.*


def answer_three():
    G_projected = answer_two()
    #G_projected = bipartite.collaboration_weighted_projected_graph(G_projected, G_projected.edges())
    G_projected = bipartite.weighted_projected_graph(G_projected, employees, ratio=False)

    return G_projected


answer_three()

# Check the answer
for edge in sorted(answer_three().edges(data=True)):
    print(edge)
# Question 4
# Suppose you'd like to find out if people that have a high relationship score also like the same types of movies.
#
# Find the Pearson correlation ( using `DataFrame.corr()` ) between employee relationship scores and the number of movies they have in common. If two employees have no movies in common it should be treated as a 0, not a missing value, and should be included in the correlation calculation.
#
# *This function should return a float.*


def answer_four():
    # Get employee relationship and employee corlaboration weight
    df_emprela = pd.read_csv('Employee_Relationships.txt', sep='\t',
                             names=['From', 'To', 'Rela_Score'])
    df_emprela.set_index(['From', 'To'], inplace=True)
    G = answer_three()
    df_colab = pd.DataFrame(G.edges(data=True), columns=['From', 'To', 'Colab_Weight'])
    df_colab['Colab_Weight'] = df_colab['Colab_Weight'].map(lambda x: x['weight'])

    # create corlaboration weight copy to later make a 2 way Colab_Weight between employee
    # For example Andy vs Claude has the same Colab_weight as Claude vs Andy
    df_colab_c = df_colab.copy()
    df_colab_c = df_colab_c[['To', 'From', 'Colab_Weight']]
    df_colab_c.rename(columns={"To": "From", "From": "To"}, inplace=True)
    # storage 2 way Colab_Weight to df_colab_final DataFrame
    df_colab_final = pd.concat([df_colab, df_colab_c])
    df_colab_final.set_index(['From', 'To'], inplace=True)

    df = pd.merge(df_emprela, df_colab_final, how='left', left_index=True, right_index=True)
    df['Colab_Weight'].fillna(value=0, inplace=True)

    # Grapph correaltion matrix for visualization
    #corr = df.corr()
    # corr.style.background_gradient(cmap='coolwarm')
    return df.corr().iloc[0, 1]


    # return list(G.nodes(data=True))
answer_four()
