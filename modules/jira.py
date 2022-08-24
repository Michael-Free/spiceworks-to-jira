'''
░░░▒█ ░▀░ █▀▀█ █▀▀█ ▒█▀▀█ █▀▀ ▀█░█▀ 
░▄░▒█ ▀█▀ █▄▄▀ █▄▄█ ▒█░░░ ▀▀█ ░█▄█░ 
▒█▄▄█ ▀▀▀ ▀░▀▀ ▀░░▀ ▒█▄▄█ ▀▀▀ ░░▀░░

Filename: jira.py

Created By: Michael Free

Summary:
A framework for preparing spiceworks
csv data for importation into Jira
Service Management.

Description:

To Dos:
- code linting
- software tests
- exception handling
- merging comments: remove final \n escape char
'''
import csv
import os
import dateutil.parser

def search_user_table(users_csvfile, user_idnumber):
    '''
    - receives users.csv file location and user ID number
    - searches the user table for the ID number
    - returns the associated email with the ID number
    '''
    with open(users_csvfile,"r", encoding="utf-8") as user_lookup:
        user_email = ""
        user_table = csv.DictReader(user_lookup, delimiter=",")
        for table_column in user_table:
            if table_column["USERID"] == user_idnumber:
                user_email = table_column["EMAIL"]
    user_lookup.close()
    return user_email

def format_datetime(current_format):
    '''
    - receives a date/timestamp
    - interprets spiceworks format
    - returns jira-friendly format
    '''
    if current_format == " ":
        new_format = " "
    else:
        d_t = dateutil.parser.parse(current_format)
        new_format = d_t.strftime("%m/%d/%Y %H:%M")
    return new_format

def map_user_ids(user_csvfile, ticket_csvfile, csv_directory):
    '''
    - receives users file location, ticket file location
    - receives the working directory for csv files
    - creates a new csv file for working
    - iterates through ticket csv file
    - calls search_user_table and replaces user ID numbers
      and replaces them with email addresses returned.
    - writes to the new csv file.
    - old tickets file is deleted
    - new tickets file is renamed ot the one deleted.
    '''
    with open(ticket_csvfile, "r", encoding="utf-8") as ticket_lookup:
        ticket_table = csv.DictReader(ticket_lookup, delimiter=",")
        new_tickets_csv = str(csv_directory+"/new_tickets.csv")
        with open(new_tickets_csv, "w", encoding="utf-8") as new_tickets:
            new_tickets.write("ASSIGNED_ID,CREATED_ID,CREATED_AT,CLOSED_AT,STATUS,SUMMARY,DESCRIPTION,COMMENTS")
            new_tickets.close()
            with open(new_tickets_csv,"a", encoding="utf-8") as write_newtickets:
                for table_column in ticket_table:
                    write_newtickets.write(
                        "\n\""+search_user_table(user_csvfile, table_column["ASSIGNED_ID"])+"\""+
                        ","+"\""+search_user_table(user_csvfile, table_column["CREATED_ID"])+"\""+
                        ",\""+format_datetime(table_column["CREATED_AT"])+"\""+
                        ",\""+format_datetime(table_column["CLOSED_AT"])+"\""+
                        ",\""+table_column["STATUS"]+"\""+
                        ",\""+str(table_column["SUMMARY"]).replace("\'","’").replace("\"","").replace(",","")+"\""+
                        ",\""+str(table_column["DESCRIPTION"]).replace("\'","").replace(",","")+"\""+
                        ",\""+str(table_column["COMMENTS"]).replace(",","").replace("\'","")+"\""
                    )
            write_newtickets.close()
    ticket_lookup.close()
    os.remove(ticket_csvfile)
    os.rename(new_tickets_csv, ticket_csvfile)

def merge_comments(ticket_csvfile, csv_directory):
    '''
    - Receives ticket csvfile and the working directory
    - creates a new csv file
    - iterates through the ticket csv file
    - merges the description and comments columns
    - deletes the old ticket csv file
    - renames the new csv file to the old ticket csv
    - jira doesn't support importation of comments:
      https://community.atlassian.com/t5/Jira-Service-
      Management/How-to-import-Comments-amp-Attachments-
      using-the-CSV-Importer/qaq-p/1921044
    '''
    with open(ticket_csvfile, "r", encoding="utf-8") as old_ticketfile:
        reader = csv.DictReader(old_ticketfile)
        with open(csv_directory+"/new_tickets.csv", "w", encoding="utf-8") as new_ticketfile:
            new_ticketfile.write("Summary, Assignee, Reporter, Status, Description")
            new_ticketfile.close()
            with open(csv_directory+"/new_tickets.csv", "a", encoding="utf-8") as populate_ticketfile:
                for row in reader:
                    populate_ticketfile.write(
                        "\n"+row["SUMMARY"]+", "
                        ""+row["ASSIGNED_ID"]+", "
                        ""+row["CREATED_ID"]+", "
                        ""+row["STATUS"]+", "
                        ""+row["DESCRIPTION"]+repr("\n").strip("\'")
                        +str(row["COMMENTS"])+""
                )
    os.remove(ticket_csvfile)
    os.rename(csv_directory+"/new_tickets.csv", ticket_csvfile)

def format_csvfile(ticket_csvfile, csv_directory):
    '''
    - receives the ticket csv file and working directory
    - creates a new csv file
    - iterates through the old csv file
    - interprets all unicode escape characters literally
      in the description section
    - writes that to the new csv file
    - deletes the old csv file, renames the new one to
      the old one.
    - referencing jira's documentation here on multi-line data:
      https://support.atlassian.com/jira-service-management-
      cloud/docs/import-a-csv-file-into-insight/
    '''
    with open(ticket_csvfile, "r", encoding="utf-8") as new_tix:
        reader_csv = csv.DictReader(new_tix)
        count_parsed = 0
        count_problems = 0
        with open(csv_directory+"/new_tickets.csv", "a", encoding="utf-8") as formatted_ticket:
            for csv_line in reader_csv:
                if isinstance(csv_line[" Description"], str):
                    decoded_string = bytes(csv_line[" Description"], "utf-8").decode("unicode_escape").replace("\"","")
                    formatted_ticket.write(
                        "\n"+csv_line["Summary"]+", "
                        ""+csv_line[" Assignee"]+", "
                        ""+csv_line[" Reporter"]+", "
                        ""+csv_line[" Status"]+", "
                        "\""+decoded_string+"\""
                    )
                    count_parsed += 1
            else:
                print(csv_line)
                count_problems += 1
        formatted_ticket.close()
    new_tix.close()
    os.remove(ticket_csvfile)
    os.rename(csv_directory+"/new_tickets.csv", ticket_csvfile)

if __name__ == "__main__":
    print()
    merge_comments(os.getcwd()+'/tickets.csv', os.getcwd())
    format_csvfile(os.getcwd()+'/tickets.csv', os.getcwd())
