#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import csv
import pandas as pd
import pingouin as pg
import numpy as np
import seaborn

import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams.update({'font.size': 18})


# In[ ]:


import os

dirs = ['USvsUK', 'pareto', 'perc', 'ages2', 'gender', 'usage']
for dir in dirs:
    if not os.path.exists(f'output/{dir}'):
        os.makedirs(f'output/{dir}')


# In[ ]:


mapping = {}
with open("../data/question_mapping.csv","r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader) # skip header
    for row in csv_reader:
        name = row[0] + "-" + row[2]
        mapping[name] = [row[1],row[3]]

for val in mapping:
    length = int(len(mapping[val][0]))
    iters = int(len(mapping[val][0]) / 60) + 1
    tmp = ""
    for i in range(1,iters+1):
        tmp += mapping[val][0][60*(i-1):60*i] + '\n' 
    mapping[val][0] = tmp


# In[ ]:


percentages = {}
with open("output/percentages_country.csv","r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        percentages[row[0]] = [float(row[1]),float(row[2]),float(row[3])]


# In[ ]:


font_size = 24
def graph_question(qnum):
    head = 'Q' + str(qnum) + '-'
    xvals = []
    for y in percentages:
        if head in y:
            xvals.append(y)

    bars = ['Region-0', 'Region-1']
    answers = []
    for val in xvals:
        answers.append(mapping[val][1])
        
    for i in range(0,len(answers)):
        if "Unsure" in answers[i]:
            answers[i] = "Unsure /\nNo Answer"
        
    barvals = {}
    
    barvals[bars[0]] = []
    barvals[bars[1]] = []
    for xval in xvals:
        barvals[bars[0]].append(percentages[xval][0])
        barvals[bars[1]].append(percentages[xval][1])
    
    barvals[bars[0]],barvals[bars[1]], answers = zip(*sorted(zip(barvals[bars[0]],barvals[bars[1]], answers),reverse=True))

    
    #xlabels = {}
    #for bar in bars:
    #    for xval in xvals:
    #        if bar in barvals:
    #            barvals[bar].append(float(percentages[bar][xval]))
    #            xlabels[bar].append(xval)
    #        else:
    #            barvals[bar] = [float(percentages[bar][xval])]
    #            xlabels[bar] = [xval]
    
    # Normalize for how many people actually answered the question
    #for bar in bars:
    #    total = sum(barvals[bar])
    #    for i in range(0,len(barvals[bar])):
    #        barvals[bar][i] = barvals[bar][i]/total

    x = np.arange(len(answers))  # the label locations
    width = 0.4  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, barvals[bars[0]], width, label='UK')
    rects2 = ax.bar(x + width/2, barvals[bars[1]], width, label='US')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Percentage Who Selected',fontsize=font_size)
    #ax.set_xlabel('Answers')
    #ax.set_title('Q' + str(qnum) + ": " + mapping[xvals[0]][0],fontsize=18,y=1.04)
    plt.xticks(rotation=90)
    ax.set_xticks(x)
    ax.set_xticklabels(answers,fontsize=font_size)
    
    locs=[]
    if qnum == 3:
        locs = [0,.1,.2,.3,.4,.5,.6,.7,.8]
    elif qnum == 20:
        locs = [0,.1,.2,.3,.4]
    elif qnum == 25:
        locs = [0,.1,.2,.3]
    if len(locs) > 0:
        plt.yticks(locs,[str(int(100*i)) for i in locs],fontsize=22)
    ax.legend(fontsize=font_size)

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    #autolabel(rects1)
    #autolabel(rects2)
    fig.set_size_inches(10, 10, forward=True)
    fig.tight_layout()

    plt.savefig('output/USvsUK/Q' + str(qnum) + '.pdf')
    plt.close(fig)


# In[ ]:


for i in range(2,44):
    try:
        graph_question(i)
    except:
        pass


# In[ ]:


def pareto_plot(df, x=None, y=None, title=None, num=None, show_pct_y=False, pct_format='{0:.0%}'):
    xlabel = x
    ylabel = y
    tmp = df.sort_values(y, ascending=False)
    x = tmp[x].values
    y = tmp[y].values
    weights = y / y.sum()
    cumsum = weights.cumsum()
    
    fig, ax1 = plt.subplots()
    ax1.bar(x, y)
    #ax1.set_xlabel(xlabel)
    #ax1.set_ylabel(ylabel)
    ax1.set_ylabel('Percentage Who Selected',fontsize=18)
    #ax.set_xlabel('Answers')
    ax1.set_title(title,fontsize=18,y=1.04)
    plt.xticks(rotation=90)
    ax1.set_xticks(x)
    ax1.set_xticklabels(x,fontsize=15)
    plt.yticks(fontsize=15)

    ax2 = ax1.twinx()
    ax2.plot(x, cumsum, '-ro', alpha=0.5)
    ax2.set_ylabel('', color='r')
    ax2.tick_params('y', colors='r')
    
    vals = ax2.get_yticks()
    ax2.set_yticklabels(['{:,.2%}'.format(x) for x in vals])

    # hide y-labels on right side
    if not show_pct_y:
        ax2.set_yticks([])
    
    formatted_weights = [pct_format.format(x) for x in cumsum]
    for i, txt in enumerate(formatted_weights):
        ax2.annotate(txt, (x[i], cumsum[i]), fontweight='heavy')    
        

    fig.set_size_inches(10, 10, forward=True)
    
    plt.tight_layout()
    plt.savefig('output/pareto/Q' + str(num) + '.png')
    plt.close(fig)
    
def pareto_graph(qnum):
    head = 'Q' + str(qnum) + '-'
    xvals = []
    for y in percentages:
        if head in y:
            xvals.append(y)

    bars = ['Region-0', 'Region-1']
    answers = []
    for val in xvals:
        answers.append(mapping[val][1])

    sumbar = []
    for val in xvals:
        sumbar.append(percentages[val][2]) 
                
    data = []
    for i in range(0,len(sumbar)):
        data.append([sumbar[i],answers[i]])
    df = pd.DataFrame(data, columns = ['Percent', 'Label']) 
        
    pareto_plot(df, x='Label', y='Percent', title='Q' + str(qnum) + ": " + mapping[xvals[0]][0],num=qnum)


# In[ ]:


for i in range(2,44):
    try:
        pareto_graph(i)
    except:
        pass


# In[ ]:


def bar_graph_perc(qnum):
    head = 'Q' + str(qnum) + '-'
    xvals = []
    for y in percentages:
        if head in y:
            xvals.append(y)

    bars = ['Region-0', 'Region-1']
    answers = []
    for val in xvals:
        answers.append(mapping[val][1])
        
    for i in range(0,len(answers)):
        if "everyone else" in answers[i]:
            answers[i] = "What others\n use"
        elif "work or school" in answers[i]:
            answers[i] = "For work /\n school"
        elif "associated" in answers[i]:
            answers[i] = "Association"
        elif "always" in answers[i]:
            answers[i] = "Past\nexperience"
        elif "Members" in answers[i]:
            answers[i] = "Don't Know Everyone"
        elif "Leaking" in answers[i]:
            answers[i] = "Leaking Persnal Info"
        elif "reviews" in answers[i]:
            answers[i] = "Based\non reviews"
        elif "features" in answers[i]:
            answers[i] = "Based\non features"
        elif "Usability" in answers[i]:
            answers[i] = "Usability"
            

    sumbar = []
    for val in xvals:
        sumbar.append(percentages[val][2]) 
        
    sumbar, answers = zip(*sorted(zip(sumbar, answers),reverse=True))
    
    print(sumbar)
    data = []
    for i in range(0,len(sumbar)):
        if sumbar[i] > 0:
            data.append([sumbar[i],answers[i]])
    df = pd.DataFrame(data, columns = ['Percent', 'Label']) 
    
    seaborn.set_palette("tab10")
    seaborn.set(font_scale=3.5)
    seaborn.set_style("white")
    #plt.figure(figsize=(10, 10))
    fig, ax = plt.subplots(1, 1, figsize = (20, 20), dpi=200)
    plt.xticks(rotation=60)
    if qnum == 7:
        ax.set(ylim=(0, .8))        
        #plt.yticks([0,.1,.2,.3,.4,.5,.6,.7,.8])
    else:
        ax.set(ylim=(0, .5))        
        #plt.yticks([0,.1,.2,.3,.4,.5])
    splot = seaborn.barplot(data=df, x = 'Label', y = 'Percent', ci = None)
    for p in splot.patches:
        #format(,'.2f')
        splot.annotate(str(round(p.get_height()*100,0)).replace(".0",''), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', va = 'center', xytext = (0, 15), textcoords = 'offset points')
    ax.set_xlabel('')
    #locs,labels = plt.yticks()
    #plt.yticks(locs,[str(int(100*i)) for i in locs])
    locs = [0,.1,.2,.3,.4,.5]
    plt.yticks(locs,[str(int(100*i)) for i in locs])

    # Don't mess with the limits!
    #plt.autoscale(False)
    #plt.tight_layout()
    plt.show()
    #plt.gcf().subplots_adjust(bottom=0.8)
    #plt.gcf().subplots_adjust(left=0.1)
    #plt.savefig('output/perc/Q' + str(qnum) + '.png')
    #plt.clf()
    #plt.close(fig)


# In[ ]:


bar_graph_perc(7)


# In[ ]:


percentagesmf = {}
with open("output/percentages_malefemale.csv","r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        percentagesmf[row[0]] = [float(row[1]),float(row[2]),float(row[3])]

def graph_mf(qnum):
    head = 'Q' + str(qnum) + '-'
    xvals = []
    for y in percentages:
        if head in y:
            xvals.append(y)

    bars = ['Q39-0', 'Q39-2']
    answers = []
    for val in xvals:
        answers.append(mapping[val][1])
        
    barvals = {}
    
    barvals[bars[0]] = []
    barvals[bars[1]] = []
    for xval in xvals:
        barvals[bars[0]].append(percentagesmf[xval][0])
        barvals[bars[1]].append(percentagesmf[xval][1])
    
    barvals[bars[0]],barvals[bars[1]], answers = zip(*sorted(zip(barvals[bars[0]],barvals[bars[1]], answers),reverse=True))


    x = np.arange(len(answers))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, barvals[bars[0]], width, label='female')
    rects2 = ax.bar(x + width/2, barvals[bars[1]], width, label='male')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Percentage Who Selected')
    #ax.set_xlabel('Answers')
    #ax.set_title('Q' + str(qnum) + ": " + mapping[xvals[0]][0],fontsize=18,y=1.04)
    plt.xticks(rotation=90)
    ax.set_xticks(x)
    ax.set_xticklabels(answers,fontsize=15)
    plt.yticks(fontsize=15)
    ax.legend(fontsize=18)


    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    fig.set_size_inches(10, 10, forward=True)
    fig.tight_layout()

    plt.savefig('output/gender/Q' + str(qnum) + '.png')
    plt.close(fig)


# In[ ]:


for i in range(2,44):
    try:
        graph_mf(i)
    except:
        pass


# In[ ]:


percentagesmf = {}
with open("output/percentages_age.csv","r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        percentagesmf[row[0]] = [float(row[1]),float(row[2]),float(row[3])]

def graph_age(qnum):
    head = 'Q' + str(qnum) + '-'
    xvals = []
    for y in percentages:
        if head in y:
            xvals.append(y)

    bars = ['Q39-0', 'Q39-2']
    answers = []
    for val in xvals:
        answers.append(mapping[val][1])
        
    barvals = {}
    
    barvals[bars[0]] = []
    barvals[bars[1]] = []
    for xval in xvals:
        barvals[bars[0]].append(percentagesmf[xval][0])
        barvals[bars[1]].append(percentagesmf[xval][1])
    
    barvals[bars[0]],barvals[bars[1]], answers = zip(*sorted(zip(barvals[bars[0]],barvals[bars[1]], answers),reverse=True))


    x = np.arange(len(answers))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, barvals[bars[0]], width, label='millennial')
    rects2 = ax.bar(x + width/2, barvals[bars[1]], width, label='nonmillennial')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Percentage Who Selected')
    #ax.set_xlabel('Answers')
    #ax.set_title('Q' + str(qnum) + ": " + mapping[xvals[0]][0],fontsize=18,y=1.04)
    plt.xticks(rotation=90)
    ax.set_xticks(x)
    ax.set_xticklabels(answers,fontsize=15)
    plt.yticks(fontsize=15)
    ax.legend(fontsize=18)


    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    fig.set_size_inches(10, 10, forward=True)
    fig.tight_layout()

    plt.savefig('output/ages2/Q' + str(qnum) + '.png')
    plt.close(fig)


# In[ ]:


for i in range(2,44):
    try:
        graph_age(i)
    except:
        pass


# In[ ]:


def bar_graph_perc(qnum):
    head = 'Q' + str(qnum) + '-'
    xvals = []
    for y in percentages:
        if head in y:
            xvals.append(y)

    bars = ['Region-0', 'Region-1']
    answers = []
    for val in xvals:
        answers.append(mapping[val][1])
        
    for i in range(0,len(answers)):
        if "everyone else" in answers[i]:
            answers[i] = "What others use"
        elif "work or school" in answers[i]:
            answers[i] = "For work / school"
        elif "associated" in answers[i]:
            answers[i] = "Association"
        elif "always" in answers[i]:
            answers[i] = "Past experience"
        elif "Members" in answers[i]:
            answers[i] = "Don't Know Everyone"
        elif "Leaking" in answers[i]:
            answers[i] = "Leaking Persnal Info"
        elif "reviews" in answers[i]:
            answers[i] = "Based on reviews"
        elif "features" in answers[i]:
            answers[i] = "Based on features"
        elif "Usability" in answers[i]:
            answers[i] = "Usability"
            

    sumbar = []
    for val in xvals:
        sumbar.append(percentages[val][2]) 
        
    sumbar, answers = zip(*sorted(zip(sumbar, answers),reverse=True))
            
    print(sumbar)
    data = []
    for i in range(0,len(sumbar)):
        if sumbar[i] > 0:
            data.append([sumbar[i],answers[i]])
    df = pd.DataFrame(data, columns = ['Percent', 'Label']) 
    

    
    seaborn.set_palette("tab10")
    seaborn.set(font_scale=3.5)
    seaborn.set_style("white")
    #plt.figure(figsize=(10, 10))
    fig, ax = plt.subplots(1, 1, figsize = (20, 20), dpi=200)
    #plt.xticks(rotation=60)
    if qnum == 7:
        ax.set(xlim=(0, .8))        
        #plt.yticks([0,.1,.2,.3,.4,.5,.6,.7,.8])
    else:
        ax.set(ylim=(0, .5))        
        #plt.yticks([0,.1,.2,.3,.4,.5])
    splot = seaborn.barplot(data=df, x = 'Percent', y = 'Label',orient="h", ci = None)
    for p in splot.patches:
        width = p.get_width()
        splot.text(width+.04,
            p.get_y()+p.get_height()/2. + 0.15,
            str(round(width*100,0)).replace(".0",'%'),
            ha="center")        #format(,'.2f')
    #locs,labels = plt.yticks()
    #plt.yticks(locs,[str(int(100*i)) for i in locs])
    locs = [0,.1,.2,.3,.4,.5]
    plt.xticks(locs,[str(int(100*i)) for i in locs])
    ax.set_ylabel("")

    # Don't mess with the limits!
    #plt.autoscale(False)
    #plt.tight_layout()
    plt.show()
    #plt.gcf().subplots_adjust(bottom=0.8)
    #plt.gcf().subplots_adjust(left=0.1)
    #plt.savefig('output/perc/Q' + str(qnum) + '.png')
    #plt.clf()
    #plt.close(fig)


# In[ ]:


bar_graph_perc(27)


# In[ ]:


percentagesmf = {}
with open("output/percentages_usage.csv","r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        percentagesmf[row[0]] = [float(row[1]),float(row[2]),float(row[3])]

def graph_usage(qnum):
    head = 'Q' + str(qnum) + '-'
    xvals = []
    for y in percentages:
        if head in y:
            xvals.append(y)

    bars = ['Q39-0', 'Q39-2']
    answers = []
    for val in xvals:
        answers.append(mapping[val][1])
        
    barvals = {}
    
    barvals[bars[0]] = []
    barvals[bars[1]] = []
    for xval in xvals:
        barvals[bars[0]].append(percentagesmf[xval][0])
        barvals[bars[1]].append(percentagesmf[xval][1])
    
    barvals[bars[0]],barvals[bars[1]], answers = zip(*sorted(zip(barvals[bars[0]],barvals[bars[1]], answers),reverse=True))


    x = np.arange(len(answers))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, barvals[bars[0]], width, label='users')
    rects2 = ax.bar(x + width/2, barvals[bars[1]], width, label='nonusers')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Percentage Who Selected')
    #ax.set_xlabel('Answers')
    #ax.set_title('Q' + str(qnum) + ": " + mapping[xvals[0]][0],fontsize=18,y=1.04)
    plt.xticks(rotation=90)
    ax.set_xticks(x)
    ax.set_xticklabels(answers,fontsize=15)
    plt.yticks(fontsize=15)
    ax.legend(fontsize=18)


    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    fig.set_size_inches(10, 10, forward=True)
    fig.tight_layout()

    plt.savefig('output/usage/Q' + str(qnum) + '.png')
    plt.close(fig)


# In[ ]:


for i in range(2,44):
    try:
        graph_usage(i)
    except:
        pass


# In[ ]:




