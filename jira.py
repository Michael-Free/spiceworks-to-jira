'''
prepping for jira import
'''
import csv
from re import search
import sys
import os
import pandas as pd


def search_user_table(users_csvfile, user_idnumber):
    '''
    search
    '''
    with open(users_csvfile,"r", encoding="utf-8") as user_lookup:
        user_email = ""
        user_table = csv.DictReader(user_lookup, delimiter=",")
        for table_column in user_table:
            if table_column["USERID"] == user_idnumber:
                user_email = table_column["EMAIL"]
    #user_lookup.close()
    return user_email

def map_user_ids(user_csvfile, ticket_csvfile):
    '''
    map user ids 
    '''
    assigned_user_list = []
    submitter_user_list = []
    with open(ticket_csvfile, "r", encoding="utf-8") as ticket_lookup:
        ticket_table = csv.DictReader(ticket_lookup, delimiter=",")
        with open(os.getcwd()+"/new_tickets.csv", "w", encoding="utf-8") as new_tickets:
            new_tickets.write("ASSIGNED_ID,CREATED_ID,CREATED_AT,CLOSED_AT,STATUS,SUMMARY,DESCRIPTION,COMMENTS")
            for table_column in ticket_table:
                # iterate through each column in a row of table column
                print(
                    #"\""+search_user_table(user_csvfile, table_column["ASSIGNED_ID"])+"\""+
                    #","+"\""+search_user_table(user_csvfile, table_column["CREATED_ID"])+"\""+
                    #","+table_column["CREATED_AT"]+
                    #","+table_column["CLOSED_AT"]+
                    #","+table_column["STATUS"]+
                    #",\""+str(table_column["SUMMARY"]).replace("\'","’").replace("\"","").replace(",","")+"\""+
                    #",\""+str(table_column["DESCRIPTION"]).replace("\'","").replace(",","")+"\""+
                    ",\""+str(table_column["COMMENTS"]).replace(",","").replace("\'","")+"\""
                )
                #new_line = search_user_table(user_csvfile, table_column["ASSIGNED_ID"])+","
                #+search_user_table(user_csvfile, table_column["CREATED_ID"])+","
                #+str(table_column["CREATED_AT"])+","
                #+str(table_column["CLOSED_AT"])+","
                #+str(table_column["STATUS"])+","
                #+str(table_column["SUMMARY"])+","
                #+str(table_column["DESCRIPTION"])+","
                #+str(table_column["COMMENTS"])
                #print(new_line)
                # write it
    ticket_lookup.close()

    return

if __name__ == "__main__":
    print()
    map_user_ids(os.getcwd()+'/users.csv', os.getcwd()+'/tickets.csv')
