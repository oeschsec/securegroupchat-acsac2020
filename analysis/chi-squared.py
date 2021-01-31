#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import scipy.stats


# In[ ]:


#Read in data file
df = pd.read_csv('../data/responses-processed.csv')


# In[ ]:


def chi_square(Q1,Q2):
    temp = []
    for col in df.columns:
        temp.append(col)

    q1_headers = []
    q2_headers = []
    q1_prefix = 'Q' + str(Q1) + '-'
    q2_prefix = 'Q' + str(Q2) + '-'
    for val in temp:
        if q1_prefix in val:
            q1_headers.append(val)
        if q2_prefix in val:
            q2_headers.append(val)
            
    q_dict = {}
    for header in q1_headers:
        q_dict[header] = {}
        for header2 in q2_headers:
            q_dict[header][header2] = 0
      
    for index, row in df.iterrows(): 
        for header in q1_headers:
            if row[header] == 1:
                for header2 in q2_headers:
                    if row[header2] == 1:
                        q_dict[header][header2] += 1
    print(q_dict)
                        
    # Remove any headers with zero values
    toremove = {''}
    for header in q1_headers:
        for header2 in q2_headers:
            if q_dict[header][header2] == 0:
                toremove.add(header2)
    toremove.remove('')
    print(toremove)
    for h in toremove:
        q2_headers.remove(h)
    
    contingency_table = []
    for header in q1_headers:
        temp = []
        for header2 in q2_headers:
            temp.append(q_dict[header][header2])
        contingency_table.append(temp)
    
    print(contingency_table)
    chi2, p, dof, expctd = scipy.stats.chi2_contingency(np.array(contingency_table))

    print("chi2 - " + str(chi2) + ", p - " + str(p) + ", dof - " + str(dof))
    return p


# In[ ]:


def chi_square_headers(q1_headers,Q2):
    temp = []
    for col in df.columns:
        temp.append(col)

    q2_headers = []
    q2_prefix = 'Q' + str(Q2) + '-'
    for val in temp:
        if q2_prefix in val:
            q2_headers.append(val)
            
    q_dict = {}
    for header in q1_headers:
        q_dict[header] = {}
        for header2 in q2_headers:
            q_dict[header][header2] = 0
      
    for index, row in df.iterrows(): 
        for header in q1_headers:
            if row[header] == 1:
                for header2 in q2_headers:
                    if row[header2] == 1:
                        q_dict[header][header2] += 1
                        
    # Remove any headers with zero values
    toremove = {''}
    for header in q1_headers:
        for header2 in q2_headers:
            if q_dict[header][header2] == 0:
                toremove.add(header2)
    toremove.remove('')
    print(toremove)
    for h in toremove:
        q2_headers.remove(h)
    
    contingency_table = []
    for header in q1_headers:
        temp = []
        for header2 in q2_headers:
            temp.append(q_dict[header][header2])
        contingency_table.append(temp)
    
    chi2, p, dof, expctd = scipy.stats.chi2_contingency(np.array(contingency_table))

    print("chi2 - " + str(chi2) + ", p - " + str(p) + ", dof - " + str(dof))
    return p


# In[ ]:


# Male versus Female

print("Q25 - topics discussed")
chi_square_headers(['Q39-2','Q39-0'],'25')

print("Q29 - sensitive info shared")
chi_square_headers(['Q39-2','Q39-0'],'29')

print("Q3 - apps used")
chi_square_headers(['Q39-2','Q39-0'],'3')

print("Q2 - usage frequency")
chi_square_headers(['Q39-2','Q39-0'],'2')

print("Q32 - why choose a tool")
chi_square_headers(['Q39-2','Q39-0'],'32')

print("Q34 - which tools secure")
chi_square_headers(['Q39-2','Q39-0'],'34')

print("Q20 - uncomfortable topics")
chi_square_headers(['Q39-2','Q39-0'],'20')

print("Q19 - uncomfortable with sharing")
chi_square_headers(['Q39-2','Q39-0'],'19')

print("Q11 - booted from group")
chi_square_headers(['Q39-2','Q39-0'],'11')


# In[ ]:


# Nationality

print("Q3 - apps used")
chi_square_headers(['Region-0','Region-1'],'3')

print("Q20 - topics uncomfortable discussing")
chi_square_headers(['Region-0','Region-1'],'20')

print("Q25 - topics discussed")
chi_square_headers(['Region-0','Region-1'],'25')

print("Q2 - usage frequency")
chi_square_headers(['Region-0','Region-1'],'2')

print("Q38 - age")
chi_square_headers(['Region-0','Region-1'],'38')

print("Q29 - sensitive info")
chi_square_headers(['Region-0','Region-1'],'29')

print("Q19 - uncomfortable sharing")
chi_square_headers(['Region-0','Region-1'],'19')

print("Q11 - removed without permission")
chi_square_headers(['Region-0','Region-1'],'11')


# In[ ]:


# modifications to group ages together
def chi_square_ages(Q2):
    temp = []
    for col in df.columns:
        temp.append(col)

    q1_headers = ['millennial','nonmillennial']
    q2_headers = []
    q2_prefix = 'Q' + str(Q2) + '-'
    for val in temp:
        if q2_prefix in val:
            q2_headers.append(val)
            
    q_dict = {}
    for header in q1_headers:
        q_dict[header] = {}
        for header2 in q2_headers:
            q_dict[header][header2] = 0
      
    for index, row in df.iterrows(): 
        if row['Q38-0'] == 1 or row['Q38-6'] == 1:
            for header2 in q2_headers:
                if row[header2] == 1:
                    q_dict['millennial'][header2] += 1
                    
    for index, row in df.iterrows(): 
        if row['Q38-1'] == 1 or row['Q38-2'] == 1 or row['Q38-3'] == 1 or row['Q38-4'] == 1:
            for header2 in q2_headers:
                if row[header2] == 1:
                    q_dict['nonmillennial'][header2] += 1
                        
    # Remove any headers with zero values
    toremove = {''}
    for header in q1_headers:
        for header2 in q2_headers:
            if q_dict[header][header2] == 0:
                toremove.add(header2)
    toremove.remove('')
    print(toremove)
    for h in toremove:
        q2_headers.remove(h)
    
    contingency_table = []
    for header in q1_headers:
        temp = []
        for header2 in q2_headers:
            temp.append(q_dict[header][header2])
        contingency_table.append(temp)
    
    chi2, p, dof, expctd = scipy.stats.chi2_contingency(np.array(contingency_table))

    print("chi2 - " + str(chi2) + ", p - " + str(p) + ", dof - " + str(dof))
    return p


# In[ ]:


# Q2 - frequency usage
chi_square_ages("2")

# Q3 - what tools used
chi_square_ages("3")

# Q33 - believe secure tools exist - millennials more likely
chi_square_ages("33")

chi_square_ages("20")

chi_square_ages("25")

chi_square_ages("29")

chi_square_ages("19")

chi_square_ages("11")

