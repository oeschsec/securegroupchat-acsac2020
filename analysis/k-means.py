#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import csv
import numpy as np

from kmodes.kmodes import KModes
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams.update({'font.size': 18})


# In[ ]:


#Read in data file
df = pd.read_csv('../data/responses-processed.csv')
df_means = df.drop(['Id'], axis=1).transpose()


# In[ ]:


mapping = {}
with open("../data/question_mapping.csv","r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader) # skip header
    for row in csv_reader:
        name = row[0] + "-" + row[2]
        mapping[name] = [row[1],row[3]]


# In[ ]:


temp = []
for col in df.columns:
    temp.append(col)

questions = [3,4]
headers = ['Id']
for q in questions:
    head = 'Q' + str(q) + '-'
    for val in temp:
        if head in val:
            headers.append(val)
sil = []
Sum_of_squared_distances = []
K = range(2,30)
for k in K:
    km = KMeans(n_clusters=k)
    km = km.fit(df_means.values)
    Sum_of_squared_distances.append(km.inertia_)
    sil.append(silhouette_score(df_means.values, km.labels_, metric = 'euclidean'))

    
plt.plot(K, Sum_of_squared_distances, 'bx-')
plt.xlabel('K',labelpad=10)
plt.ylabel('Sum Squared Distance',labelpad=10)
#plt.title('Elbow Method For Optimal k')
#plt.show()
ticks = [16000,18000,20000,22000,24000,26000]
plt.yticks(ticks,[str(i) for i in ticks])
plt.savefig("output/elbow.pdf", bbox_inches='tight')

plt.cla()
plt.plot(K, sil, 'bx-')
plt.xlabel('K',labelpad=10)
plt.ylabel('Silhouette Score',labelpad=10)
#plt.title('Silhouette Score')
#plt.show()
plt.savefig("output/silhouette.pdf", bbox_inches='tight')


# In[ ]:

# https://shapeofdata.wordpress.com/2014/03/04/k-modes/
# Mapping categorical data to 0/1 cannot generate quality clusters for high dimensional data using K-Means
# https://www.youtube.com/watch?v=cu0AZ8QX0os
# Use K-Modes
km = KModes(n_clusters=4)

df_copy = df.copy()
df_copy = df_copy.drop(['Id'], axis=1)

clusters = km.fit_predict(df_copy)

# Print the cluster centroids
#print(km.cluster_centroids_)

headers = []
for col in df.columns: 
    headers.append(col)
headers.remove('Id')

columns = []
for centroid in km.cluster_centroids_:
    temp = []
    for i in range(0,len(centroid)):
        if centroid[i] == 1:
            temp.append(headers[i])
    columns.append(temp)

for column in columns:
    l = [mapping[i][1] for i in column]
    #print(column)
    #print(l)
    
count = 0
for column in columns:
    print(count)
    for val in column:
        print(mapping[val][0] + ": " + mapping[val][1])
    print("\n\n")


for i in range(0,len(columns)):
    for k in range(0,len(columns)):
        temp = []
        for val in columns[i]:
            if val not in columns[k]:
                temp.append(val)
        print(str(i) + "," + str(k) + "," + str(temp))


# In[ ]:

# https://shapeofdata.wordpress.com/2014/03/04/k-modes/
def k_modes(questions):
    temp = []
    for col in df.columns:
        temp.append(col)

    for val in questions:
        foo = 'Q' + str(val) + '-0'
        print(str(val) + ' - ' + mapping[foo][0])
    headers = []
    for q in questions:
        head = 'Q' + str(q) + '-'
        for val in temp:
            if head in val:
                headers.append(val)

    km = KModes(n_clusters=2)

    clusters = km.fit_predict(df[headers])

    columns = []
    for centroid in km.cluster_centroids_:
        temp = []
        for i in range(0,len(centroid)):
            if centroid[i] == 1:
                temp.append(headers[i])
        columns.append(temp)

    for column in columns:
        l = [mapping[i][1] for i in column]
        print(column)
        print(l)
        
# Hypothesis: 
k_modes([11,21,28,35])

