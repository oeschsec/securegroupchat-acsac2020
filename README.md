# Group Chat Survey
This repository contains the data and analysis for the paper "Understanding User Perceptions of Security and Privacy for Group Chat: A Survey of Users in the US and UK".

## Data Files

| Filename | Contents |
| -------- | -------- |
| responses (raw).xlsx | Raw responses gathered from participants. Human readable. |
| responses (coded).xlsx | Responses along with open coding results. Human readable. |
| coding-report.txt | A high-level analysis of coded responses. |
| responses-processed.csv | Participant multiple choice responses coded as a large array of boolean values. Used by the analysis scripts. |
| question_mapping.cvs | Mapping between question Ids in response-processed.csv and question text. Used by the analysis scripts. |

## Data Analysis

To run the data analysis scripts, you will need to have `python` >=3.8 and the `pipenv` package installed. Pipenv is used to handle all the dependencies. Once it is isntalled, do the following:

* Open the analysis directory
* `pipenv install`
* `pipenv run python init.py`

You can then run the various analysis scripts using `pipenv run python script.py`. Output will be stored to `analysis/output`. The scripts include:

| Filename | Contents |
| -------- | -------- |
| init.py | Will regenerate csv files used by other analysis scripts. |
| basic-overview.py | Script that looks at various splits (country, gender, age, usage) within the data. |
| chi-squared.py | Script that looks at various non-parametric correlations. |
| data-driving.py | Script exploring correlations within the data. |
| k-means.py | script with k-means and k-modes analysis scripts. |
