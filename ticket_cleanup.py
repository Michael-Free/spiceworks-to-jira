# cleanup tickets.csv
# the 7.2k lines is actually 20k lines--- now its 100k lines
import pandas as pd

def read_escape_chars():
    with open('output.csv', 'r', encoding='unicode_escape') as escaped_csv:
        tickets = escaped_csv.readlines()
        with open('output0.csv', 'w', encoding='utf-8') as fout:
            fout.writelines(tickets)
            fout.close()

def format_headers():
    with open('output.csv', 'r', encoding='utf-8') as fin:
        data = fin.read().splitlines(True)
    with open('output.csv', 'w', encoding='utf-8') as fout:
        fout.writelines("Assignee,Reporter,Due Date,Status,Summary,Description\n")
        fout.writelines(data[2:])
        fout.close()
        fin.close()

def replace_employees(): 
    # user lookups for meredith and betty and replace them with ghilker in assignees
    df = pd.read_csv("output.csv")#need utf-8 encoding
    df['Assignee'] = df['Assignee'].replace({'bwilson@ideaexchange.org': 'ghilker@ideaexchange.org'}).replace({'mcleversey@ideaexchange.org': 'ghilker@ideaexchange.org'})
    df.to_csv('output.csv', index=False)#need utf-8 encoding

format_headers()
replace_employees()
read_escape_chars()