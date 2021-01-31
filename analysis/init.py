import pandas as pd

# Ensure the output directory exists
import os
if not os.path.exists('output'):
    os.makedirs('output')

#Read in data file
df = pd.read_csv('../data/responses-processed.csv')
df_count = len(df)

# Discover questions and options
questions = {}
for col in df.columns:
    if col.startswith('Q'):
        question, response = col.split('-')
        if not question in questions:
            questions[question] = []
        questions[question].append(response)

# Get overall answer counts
with open('output/answered.csv', 'w') as answered:
    for question in questions:
        count = df[[col for col in df if col.startswith(f'{question}-')]].any(axis=1).sum()
        answered.write(f'{question},{df_count},{count}\n')

# Analyze data based on two splits of the data, creating a CSV used by the python notebooks.
def analyze_split(split1, split2, filename_percent):
    with open(filename_percent, 'w') as percent:
        for question in questions:
            split1_count = split1[[col for col in split1 if col.startswith(f'{question}-')]].any(axis=1).sum()
            split2_count = split2[[col for col in split2 if col.startswith(f'{question}-')]].any(axis=1).sum()
            for response in questions[question]:
                count1 = split1[f'{question}-{response}'].sum()
                count2 = split2[f'{question}-{response}'].sum()
                percent.write(f'{question}-{response},{round(count1/split1_count, 2)},{round(count2/split2_count, 2)},{round((count1+count2)/(split1_count+split2_count), 2)}\n')


analyze_split(df[df['Region-0']==1], df[df['Region-1']==1], 'output/percentages_country.csv')         # UK, US
analyze_split(df[df['Q39-0']==1], df[df['Q39-2']==1], 'output/percentages_malefemale.csv')             # Female, Male

# <35, >=35
analyze_split( df[(df['Q38-0'] == 1) | (df['Q38-6'] == 1)], \
    df[(df['Q38-1'] == 1) | (df['Q38-2'] == 1) | (df['Q38-3'] == 1) | (df['Q38-4'] == 1)], \
    'output/percentages_age.csv')
    
# <35, >=35
analyze_split( df[(df['Q38-0'] == 1) | (df['Q38-6'] == 1)], \
    df[(df['Q38-1'] == 1) | (df['Q38-2'] == 1) | (df['Q38-3'] == 1) | (df['Q38-4'] == 1)], \
    'output/percentages_age.csv')

# Rarely, 1+ times a week
analyze_split( df[(df['Q2-3'] == 1) | (df['Q2-5'] == 1)], \
    df[(df['Q2-0'] == 1) | (df['Q2-1'] == 1) | (df['Q2-2'] == 1) | (df['Q2-4'] == 1)], \
    'output/percentages_usage.csv')
