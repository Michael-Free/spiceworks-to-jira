'''
░░░▒█ ░▀░ █▀▀█ █▀▀█ ▒█▀▀█ █▀▀ ▀█░█▀ 
░▄░▒█ ▀█▀ █▄▄▀ █▄▄█ ▒█░░░ ▀▀█ ░█▄█░ 
▒█▄▄█ ▀▀▀ ▀░▀▀ ▀░░▀ ▒█▄▄█ ▀▀▀ ░░▀░░

Filename:
Created By:
Summary:
To Dos:

'''
import csv
import os
import codecs
import dateutil.parser

def search_user_table(users_csvfile, user_idnumber):
    '''
    Inputs:
    Ouputs:
    Summary:
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
    Inputs:
    Ouputs:
    Summary:
    Format the date/time for JIRA
    '''
    if current_format == " ":
        new_format = " "
    else:
        d_t = dateutil.parser.parse(current_format)
        new_format = d_t.strftime("%m/%d/%Y %H:%M")
    return new_format

def map_user_ids(user_csvfile, ticket_csvfile, csv_directory):
    '''
    Inputs:
    Ouputs:
    Summary: user ids
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
    Inputs:
    Ouputs:
    Summary:

    JIRA doesn't support importing of comments
    https://community.atlassian.com/t5/Jira-Service-Management/How-to-import-Comments-amp-Attachments-using-the-CSV-Importer/qaq-p/1921044
    
    Add comments to ticket description
    Do some reformatting for the JIRA import
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

def format_csvfile(ticket_csvfile):
    '''
    Inputs:
    Ouputs:
    Summary:
    format for jira
    '''
    with open(ticket_csvfile, "r", encoding="utf-8") as new_tix:
        reader_csv = csv.DictReader(new_tix)
        count_me = 0
        for csv_line in reader_csv:
            if isinstance(csv_line[" Description"], str):
                decoded_string = bytes(csv_line[" Description"], "utf-8").decode("unicode_escape").replace("\"","")
                count_me += 1
            else:
                print(csv_line)
    print(count_me)

if __name__ == "__main__":
    print()
    #merge_comments(os.getcwd()+'/tickets.csv', os.getcwd())
    #format_csvfile(os.getcwd()+'/tickets.csv')
