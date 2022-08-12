
import csv
import pandas as pd
def read_escape_chars():
    with open('output_quotes.csv', 'r', encoding='unicode_escape') as escaped_csv:
        tickets = escaped_csv.readlines()
        with open('output_final.csv', 'w', encoding='utf-8') as fout:
            fout.writelines(tickets)
            fout.close()

def format_headers(format_input, format_output):  
    with open(format_input, 'r', encoding='utf-8') as fin:
        data = fin.read().splitlines(True)
    with open(format_output, 'w', encoding='utf-8') as fout:
        fout.writelines("TicketID,Assignee,Reporter,Due Date,Status,Summary,Description\n")
        fout.writelines(data[1:])
        fout.close()
        fin.close()

def quotes_back(quotes_input, quotes_output):
    # I WANT MY QUOTES BACK! too busy to mess around with this stuff - i'm doing another read and write to csv
    with open(quotes_output, 'w', encoding='utf-8') as quote_write:
        with open(quotes_input, 'r', encoding='utf-8') as quote_read:
            quote_reader = csv.reader(quote_read, delimiter=',')
            for qr in quote_reader:
                replace_email = qr[2]
                empty_description = qr[6]
                '''
                if replace_email in ('bwilson@ideaexchange.org','mcleversey@ideaexchange.org'):
                    replace_email='ghilker@ideaexchange.org'
                '''
                if empty_description == " ":
                    empty_description="No Description"
                quote_write.write(qr[1]+","+qr[2]+","+qr[3]+","+qr[4]+",\""+qr[5]+"\",\""+str(empty_description).replace("@"," at ")+"\""+"\n")

def chunk_csv(csv_to_chunk):
    csvfile = open(csv_to_chunk, 'r').readlines()
    filename = 1
    for i in range(len(csvfile)):
        if i % 200 == 0:
            open(str(filename) + '.csv', 'w+').writelines(csvfile[i:i+200])
            filename += 1

format_headers('tickets.csv', 'tickets0.csv')
quotes_back('tickets0.csv','tickets1.csv')
format_headers('tickets1.csv', 'tickets2.csv')
'''
format_headers('output_quotes.csv','output_quotes.csv')
chunk_csv('output_quotes.csv')'''
