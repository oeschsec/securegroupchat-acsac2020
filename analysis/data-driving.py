#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import pingouin as pg


# In[ ]:


#Read in data file
df = pd.read_csv('../data/responses-processed.csv')


# In[ ]:


#Do people who use Signal use security in choosing 
#instant messaging tools?
#Simple row-to-row correlation
pg.corr(x=df['Q3-17'], y=df['Q34-31'])


# In[ ]:


pg.corr(x=df['Q40-0'], y=df['Q3-16'])


# In[ ]:


corr = pg.pairwise_corr(df, columns=[['Q7-7'],['Q3-0', 'Q3-1', 'Q3-2', 'Q3-3', 'Q3-4', 'Q3-5', 'Q3-6', 'Q3-7', 'Q3-8', 'Q3-9', 'Q3-10', 'Q3-11', 'Q3-12', 'Q3-13', 'Q3-14', 'Q3-15', 'Q3-16', 'Q3-17', 'Q3-18']
], method='pearson')
corr.sort_values(by=['p-unc'])[['X', 'Y', 'n', 'r', 'p-unc']].head()
# shows that Signal, IMO and Telegram are associated with users who choose baesd on security


# In[ ]:


# It appears largest correlations between tool usage and why it was selected are for security, features and work/school
corr = pg.pairwise_corr(df, columns=[['Q7-0', 'Q7-1', 'Q7-2', 'Q7-3', 'Q7-4', 'Q7-5', 'Q7-6', 'Q7-7', 'Q7-8', 'Q7-9', 'Q7-10']
,['Q3-0', 'Q3-1', 'Q3-2', 'Q3-3', 'Q3-4', 'Q3-5', 'Q3-6', 'Q3-7', 'Q3-8', 'Q3-9', 'Q3-10', 'Q3-11', 'Q3-12', 'Q3-13', 'Q3-14', 'Q3-15', 'Q3-16', 'Q3-17', 'Q3-18']
], method='pearson')
corr.sort_values(by=['p-unc'])[['X', 'Y', 'n', 'r', 'p-unc']].head()
#Security-Signal
#Work/School usage-Slack
#Features-Discord
#Security-IMO
#Work/School-Skype


# In[ ]:


# People who answered they use it daily tend to use 3 apps - Snapchat, WhatsApp, Instagram direct
corr = pg.pairwise_corr(df, columns=[['Q2-0', 'Q2-1', 'Q2-2', 'Q2-3', 'Q2-4', 'Q2-5']
,['Q3-0', 'Q3-1', 'Q3-2', 'Q3-3', 'Q3-4', 'Q3-5', 'Q3-6', 'Q3-7', 'Q3-8', 'Q3-9', 'Q3-10', 'Q3-11', 'Q3-12', 'Q3-13', 'Q3-14', 'Q3-15', 'Q3-16', 'Q3-17', 'Q3-18']
], method='pearson')
corr.sort_values(by=['p-unc'])[['X', 'Y', 'n', 'r', 'p-unc']].head()
# Daily - Snapchat, Instagram direct, WhatsApp


# In[ ]:


# Weak correlation between those who like privacy and those who use Telegram
corr = pg.pairwise_corr(df, columns=[['Q5-0', 'Q5-1', 'Q5-2', 'Q5-3', 'Q5-4', 'Q5-5', 'Q5-6', 'Q5-7', 'Q5-8', 'Q5-9', 'Q5-10']

,['Q3-0', 'Q3-1', 'Q3-2', 'Q3-3', 'Q3-4', 'Q3-5', 'Q3-6', 'Q3-7', 'Q3-8', 'Q3-9', 'Q3-10', 'Q3-11', 'Q3-12', 'Q3-13', 'Q3-14', 'Q3-15', 'Q3-16', 'Q3-17', 'Q3-18']
], method='pearson')
corr.sort_values(by=['p-unc'])[['X', 'Y', 'n', 'r', 'p-unc']].head()


# In[ ]:


#Trying to find clusters with KMeans for all data
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

df_copy = df.copy()
df_copy = df_copy.drop(['Region-0','Region-1'], axis=1)
dataset_array = df_copy.values

Sum_of_squared_distances = []
K = range(1,15)
for k in K:
    km = KMeans(n_clusters=k)
    km = km.fit(df_copy)
    Sum_of_squared_distances.append(km.inertia_)
    
plt.plot(K, Sum_of_squared_distances, 'bx-')
plt.xlabel('k')
plt.ylabel('Sum_of_squared_distances')
plt.title('Elbow Method For Optimal k')
plt.show()


# In[ ]:


#Trying to find clusters with KMeans for two questions
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

Sum_of_squared_distances = []
K = range(1,15)
for k in K:
    km = KMeans(n_clusters=k)
    km = km.fit(df[['Id','Region-0','Region-1','Q5-0', 'Q5-1', 'Q5-2', 'Q5-3', 'Q5-4', 'Q5-5', 'Q5-6', 'Q5-7', 'Q5-8', 'Q5-9', 'Q5-10']])
    Sum_of_squared_distances.append(km.inertia_)
    
plt.plot(K, Sum_of_squared_distances, 'bx-')
plt.xlabel('k')
plt.ylabel('Sum_of_squared_distances')
plt.title('Elbow Method For Optimal k')
plt.show()


# In[ ]:


#Trying to find clusters with KMeans for two questions
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import scipy
import math

df_copy = df.copy()
df_copy = df_copy.drop(['Region-0','Region-1','Id'], axis=1)

headers = []
for col in df.columns: 
    headers.append(col)
headers.remove('Region-0')
headers.remove('Region-1')


km = KMeans(n_clusters=3)
km = km.fit(df_copy)

print(scipy.spatial.distance.euclidean(km.cluster_centers_[0],km.cluster_centers_[1]))
print(scipy.spatial.distance.euclidean(km.cluster_centers_[0],km.cluster_centers_[2]))
print(scipy.spatial.distance.euclidean(km.cluster_centers_[1],km.cluster_centers_[2]))

transformed = []
def get_diff(one,two):
    diff = []
    for i in range(0,len(one)):
        diff.append(abs(one[i]-two[i]))
    transformed.append(diff)
    
get_diff(km.cluster_centers_[0],km.cluster_centers_[1])
get_diff(km.cluster_centers_[0],km.cluster_centers_[2])
get_diff(km.cluster_centers_[1],km.cluster_centers_[2])

count = 0
headers1 = []
headers2 = []
headers3 = []
for center in transformed:
    for i in range(0,len(center)):
        if center[i] > .3:
            if count == 0:
                headers1.append(headers[i])
            elif count == 1:
                headers2.append(headers[i])
            else:
                headers3.append(headers[i])
                
    count += 1
    
questions = []
headers = [headers1,headers2,headers3]
for header in headers:
    for val in header:
        if int(val[1:-2].replace('-','')) not in questions:
            questions.append(int(val[1:-2].replace('-','')))

        
print(sorted(questions))
    
#def Diff(li1, li2): 
#    return (list(set(li1) - set(li2)))

#print(Diff(headers1,headers3))
#print(Diff(headers1,headers2))
#print(Diff(headers2,headers3))

# it's gravitating towards yes/no data or extremes in the multiselect data

