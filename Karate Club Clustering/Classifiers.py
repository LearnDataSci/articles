from sklearn import cluster
import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics.cluster import normalized_mutual_info_score
from sklearn.metrics.cluster import adjusted_rand_score


# Declaration of functions
def drawCommunities(G, partition, pos):
    # G is graph in networkx form
    # Partition is a dict containing info on clusters
    # Pos is base on networkx spring layout (nx.spring_layout(G))

    # For separating communities colors
    dictList = defaultdict(list)
    nodelist = []
    for node, com in partition.items():
        dictList[com].append(node)

    # Get size of Communities
    size = len(set(partition.values()))

    # For loop to assign communities colors
    for i in range(size):

        amplifier = i % 3
        multi = (i / 3) * 0.3

        red = green = blue = 0

        if amplifier == 0:
            red = 0.1 + multi
        elif amplifier == 1:
            green = 0.1 + multi
        else:
            blue = 0.1 + multi

        # Draw Nodes
        nx.draw_networkx_nodes(G, pos,
                               nodelist=dictList[i],
                               node_color=[0.0 + red, 0.0 + green, 0.0 + blue],
                               node_size=500,
                               alpha=0.8)

    # Draw edges and final plot
    plt.title("Zachary's Karate Club")
    nx.draw_networkx_edges(G, pos, alpha=0.5)


def listToDict(list):
    listdict = {}

    for i in range(len(list)):
        listdict[i] = list[i]

    return listdict


def graphToEdgeMatrix(G):
    # Initialize Edge Matrix
    edgeMat = [[0 for x in range(len(G))] for y in range(len(G))]

    # For loop to set 0 or 1 ( diagonal elements are set to 1)
    for node in G:
        tempNeighList = G.neighbors(node)
        for neighbor in tempNeighList:
            edgeMat[node][neighbor] = 1
        edgeMat[node][node] = 1

    return edgeMat


# Initialize some variables to help us with the generalization of the program
kClusters = 2
results = []
nmiResults = []
arsResults = []

# Load and Store both data and groundtruth of Zachary's Karate Club
G = nx.karate_club_graph()
groundTruth = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# Transform our graph data into matrix form
edgeMat = graphToEdgeMatrix(G)

# Positions the nodes using Fruchterman-Reingold force-directed algorithm
# Too technical to discuss right now, just go with it
pos = nx.spring_layout(G)
drawCommunities(G, listToDict(groundTruth), pos)

# -----------------------------------------

# Spectral Clustering Model
spectral = cluster.SpectralClustering(n_clusters=kClusters, affinity="precomputed", n_init=200)
spectral.fit(edgeMat)

# Transform our data to list form and store them in results list
results.append(list(spectral.labels_))

# -----------------------------------------

# Agglomerative Clustering Model
agglomerative = cluster.AgglomerativeClustering(n_clusters=kClusters, linkage="ward")
agglomerative.fit(edgeMat)

# Transform our data to list form and store them in results list
results.append(list(agglomerative.labels_))

# -----------------------------------------

# K-means Clustering Model
kmeans = cluster.KMeans(n_clusters=kClusters, n_init=200)
kmeans.fit(edgeMat)

# Transform our data to list form and store them in results list
results.append(list(kmeans.labels_))

# -----------------------------------------

# Affinity Propagation Clustering Model
affinity = cluster.affinity_propagation(S=edgeMat, max_iter=200, damping=0.6)

# Transform our data to list form and store them in results list
results.append(list(affinity[1]))

# Append the results into lists
for x in results:
    nmiResults.append(normalized_mutual_info_score(groundTruth, x))
    arsResults.append(adjusted_rand_score(groundTruth, x))

# -----------------------------------------


# Code for plotting results

# Average of NMI and ARS
y = [sum(x) / 2 for x in zip(nmiResults, arsResults)]

xlabels = ['Spectral', 'Agglomerative', 'Kmeans', 'Affinity Propagation']

fig = plt.figure()
ax = fig.add_subplot(111)

# Set parameters for plotting
ind = np.arange(len(y))
width = 0.35

# Create barchart and set the axis limits and titles
ax.bar(ind, y, width, color='blue', error_kw=dict(elinewidth=2, ecolor='red'))
ax.set_xlim(-width, len(ind) + width)
ax.set_ylim(0, 2)
ax.set_ylabel('Average Score (NMI,ARS)')
ax.set_title('Score Evaluation')

# Add the xlabels to the chart
ax.set_xticks(ind + width / 2)
xtickNames = ax.set_xticklabels(xlabels)
plt.setp(xtickNames, fontsize=12)

# Add the actual value on top of each chart
for i, v in enumerate(y):
    ax.text(i, v, str(round(v, 2)), color='blue', fontweight='bold')

# Show the final plot
plt.show()
