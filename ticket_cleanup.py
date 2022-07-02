
import csv 
def read_escape_chars():
    with open('output_quotes.csv', 'r', encoding='unicode_escape') as escaped_csv:
        tickets = escaped_csv.readlines()
        with open('output_final.csv', 'w', encoding='utf-8') as fout:
            fout.writelines(tickets)
            fout.close()

def format_headers():
    with open('tickets.csv', 'r', encoding='utf-8') as fin:
        data = fin.read().splitlines(True)
    with open('output.csv', 'w', encoding='utf-8') as fout:
        fout.writelines("TicketID,Assignee,Reporter,Due Date,Status,Summary,Description\n")
        fout.writelines(data[2:])
        fout.close()
        fin.close()

format_headers()

# I WANT MY QUOTES BACK! too busy to mess around with this stuff - i'm doing another read and write to csv
with open('output_quotes.csv', 'w', encoding='utf-8') as quote_write:
    with open('output.csv', 'r', encoding='utf-8') as quote_read:
        quote_reader = csv.reader(quote_read, delimiter=',')
        for qr in quote_reader:
            replace_email = qr[2]
            empty_description = qr[6]
            if replace_email in ('bwilson@ideaexchange.org','mcleversey@ideaexchange.org'):
                replace_email='ghilker@ideaexchange.org'
            if empty_description == " ":
                empty_description="No Description"
            quote_write.write(qr[1]+","+replace_email+","+qr[3]+","+qr[4]+",\""+qr[5]+"\",\""+str(empty_description).replace("@"," at ")+"\""+"\n")
read_escape_chars()