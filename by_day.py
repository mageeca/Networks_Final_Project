#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import resample
import datetime
import seaborn as sns

import networkx as nx
import copy
import random
import getpass
#import psycopg2 as ps
import os
import re

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pandas.plotting import register_matplotlib_converters

#%%
df = pd.read_csv("/Users/carriemagee/Desktop/NETWORKS/influence_edges.csv")

# %%
## CC is the empty Dict for number of connected components at time T
CC = {}
## NN is the empty Dict for number of nodes in the largest connected component at time T
NN = {}
## Clus_c empty dictionary for clustering coefficient
Clus_C = {}
## NE empty dictionary for number of edges
NE = {}
## Num_N empty dictionary for max possible edges
Max_E = {}
## Density ...
Den = {}
## Number of nodes in the entire network
Nu_N = {}

## avg number of nodes in clusters except the largest
Avg_N= {}

## Largest sns in source
SNS_S = {}

## Largest sns in target
SNS_T = {}

## Dictionary for list of number of nodes in each connect cluster at time T

NN_C = {}

## Difference between the number of nodes in the largest cluster vs the second largest cluster
diff = {}

second_large_cluster_node = {}
# %%
for day, group_df in df.groupby(df['Genre'].dt.date): 
     
        try:
            Graph = nx.from_pandas_edgelist(group_df, 'Source', 'Target')
            Graph_D = nx.from_pandas_edgelist(group_df, 'Source', 'Target', create_using=nx.DiGraph()) ## This creates a directed Graph
        except:
            pass
        CC[day] = nx.number_connected_components(Graph) ## Number of connected clusters
        
        NN_C_List = []    #Dictionary for list of number of nodes in each connect cluster at time T

        for c in nx.connected_components(Graph):  ## Number of nodes in each connected cluster
            NN_C_List.append(len(c))
            
            
                

        ## Sorting in descending to get the largest cluster at the top
        NN_C_List = sorted(NN_C_List,reverse= True)
       
        NN_C[day] = NN_C_List  
        try:
            diff[day] = NN_C_List[0] - NN_C_List[1]  ## Difference between the number of nodes in the largest and second largest connected cluster
        except:
            diff[day] = 0  ## For when there is only one connected cluster

        NN[day] = NN_C_List[0]  ## Number of nodes in the largest connected cluster
        Clus_C[day] = nx.average_clustering(Graph) ## Cluster coefficient of the graph
        NE[day]  = Graph_D.number_of_edges() ## Number of Edges
        Max_E[day] = (Graph.number_of_nodes()*(Graph.number_of_nodes()-1))/2 ## Max possible number of edges
        
        Den[day] = nx.density(Graph_D) ## Density
        
        Nu_N[day] = Graph.number_of_nodes() ## Number of Nodes
        try:
            Avg_N[day] = (Nu_N[day] -NN[day])/(CC[day]-1)   ## Average number of nodes in the network except the largest connected component 
        except: 
            Avg_N[day] = 0
        
        try:
            second_large_cluster_node[day] = NN_C_List[1]   ## Number of nodes in the second largest cluster
        except:
            second_large_cluster_node[day] = 0
        

        in_degree_centrality = nx.in_degree_centrality(Graph_D) 
        out_degree_centrality = nx.out_degree_centrality(Graph_D)


# %%
