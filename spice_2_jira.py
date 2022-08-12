'''
        ███████╗██████╗ ██╗ ██████╗███████╗        ██████╗              ██╗██╗██████╗  █████╗
        ██╔════╝██╔══██╗██║██╔════╝██╔════╝        ╚════██╗             ██║██║██╔══██╗██╔══██╗
        ███████╗██████╔╝██║██║     █████╗           █████╔╝             ██║██║██████╔╝███████║
        ╚════██║██╔═══╝ ██║██║     ██╔══╝          ██╔═══╝         ██   ██║██║██╔══██╗██╔══██║
        ███████║██║     ██║╚██████╗███████╗███████╗███████╗███████╗╚█████╔╝██║██║  ██║██║  ██║
        ╚══════╝╚═╝     ╚═╝ ╚═════╝╚══════╝╚══════╝╚══════╝╚══════╝ ╚════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
          (A.K.A. I WAS GIVEN A 7200+ LINE JSON FILE AND EXPECTED TO DO SOMETHING WITH IT)

PROBLEM
    - Spiceworks is ending support of their free, ticketing software.
    - The organization has chosen to use JIRA Service Management as its new ticketing software.
    - This will be used by the IT Staff and the Facilities Staff.
    - IT Staff have moved to JIRA, but Facilities Staff need to access their old tickets.

CONSTRAINTS
    - Time is limited to get this done.
    - There isn't an option for importing this into a database to play with the data.
    - Will need to work with CSV files, especially since this is required for JIRA imports.

ISSUES
    - issues with concat long email addresses
    - no exception handling

REQUIREMENTS
    - Python 3.10.x
    - Pandas
'''
import json
import os
import pandas as pd
import re

current_directory=os.getcwd()
spiceworks_json=current_directory+'/exported_data.json'
user_csv=current_directory+'/users.csv'
tickets_csv=current_directory+'/tickets.csv'

def create_csvs(csv_file,csv_headers):
    '''
    Create a CSV file with the filename provided and the headers provided
    '''
    with open(csv_file,'w',encoding='utf-8') as csv_write:
        csv_write.write(csv_headers)
        csv_write.close()

def write_usercsv(userdata):
    '''
    Write all users from json to a users.csv file.
    '''
    with open(user_csv, 'a+', encoding='utf-8') as spiceworksusers_append:
        if userdata["role"] == "admin":
            spiceworksusers_append.write(
                "\n"+str(userdata["import_id"])+
                ","+userdata["email"]+
                ","+userdata["first_name"]+
                ","+userdata["first_name"]+
                " "+userdata["last_name"]
                )
        elif userdata["role"] == "helpdesk_admin":
            spiceworksusers_append.write(
                "\n"+str(userdata["import_id"])+
                ","+userdata["email"]+
                ","+userdata["first_name"]+
                ","+userdata["first_name"]+
                " "+userdata["last_name"]
                )
        else:
            spiceworksusers_append.write("\n"+
                str(userdata["import_id"])+
                ","+userdata["email"]+", ,"
                )
    return spiceworksusers_append.close()

def write_ticketcsv(ticketdata):
    '''
    - receive all data in a spiceworks ticket
    - count all tickets with an "assigned_to" header.
    - grab the content of the description of that ticket.
    - parse all the json data into tickets.csv
    '''
    count_tickets = 0
    for swt in ticketdata:
        if 'assigned_to' in swt:
            count_tickets +=1
            if 'description' in swt:
                description_content = repr(swt["description"]+'\n').replace(',','.').replace('\'','')
            elif 'description' not in swt:
                description_content = ' '
            else:
                print(swt.keys())
            with open(tickets_csv,'a+',encoding='utf-8') as tickets_write:
                tickets_write.write(
                    "\n"+str(count_tickets)+
                    ","+str(swt["assigned_to"])+
                    ","+str(swt["created_by"])+
                    ","+re.search(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}', swt["created_at"]).group(0)+
                    ","+swt["status"]+
                    ","+str(swt["summary"]).replace(',','.').replace('\n',' ')+
                    ","+description_content.replace('\'','').replace('\"','')+
                    ","+str(format_comments(swt["Comments"]))
                    )
            tickets_write.close()
        else:
            '''
            - For tickets that aren't formatting properly this is the output i'm getting:
                    ASSIGNED TO ISSUE
                    dict_keys(['category', 'created_at', 'created_by',
                    'description', 'email_message_id', 'first_response_secs',
                    'priority', 'site_id', 'status',
                    'status_updated_at', 'summary', 'updated_at',
                    'viewed_at', 'import_id', 'Comments'])
            '''
            print("ASSIGNED TO ISSUE")
            print(swt.keys())

def user_lookup(user_id):
    '''
    - Look up a user id number from spiceworks, return the email address to attach to a JIRA account
    '''
    users_csv = pd.read_csv(user_csv, index_col=False)
    user_row = users_csv.loc[users_csv['USERID'] == user_id]
    user_email= user_row.EMAIL.to_string(index=False)
    return user_email

def format_comments(commentdata):
    '''
    - iterate through all comments in a ticket.
    - return the time the ticket was updated at, who updated it,
      and the content of the comment for each ticket
    - strip out anything that can mess up the csv file at this point.
    - record all escape characters as plain text for now.
    '''
    for comments in range(len(commentdata)):
        comment_dict = commentdata[comments]
        ticket_comments = str(
            "UPDATED AT "+
            comment_dict['updated_at']+
            " BY "+user_lookup(comment_dict['created_by'])+
            repr("\n").replace('\'','')+
            repr(comment_dict['body']).replace(',','.')
                .replace('\'','').replace('\"','').replace('\'','')
            )
    return re.sub('@', ' at ', ticket_comments)

def assign_userids():
    '''
    - Read the UserID number in assigned ticket users from the spiceworks tickets.csv file
    - Look up that UserID number in users.csv, return a corresponding email address
    - write that into the tickets_excelview.csv
    '''
    read_tickets = pd.read_csv(tickets_csv, dtype={'DESCRIPTION':str,'COMMENTS':str})
    a_id = read_tickets['ASSIGNED_ID']
    assignees = []
    for assign_id in a_id:
        assignees.append(user_lookup(int(assign_id)))
    read_tickets.drop(columns='ASSIGNED_ID', inplace=True)
    read_tickets.insert(loc=1, column="ASSIGNED_ID", value=assignees)
    c_id = read_tickets['CREATED_ID']
    creators = []
    for create_id in c_id:
        creators.append(user_lookup(int(create_id)))
    read_tickets.drop(columns='CREATED_ID', inplace=True)
    read_tickets.insert(loc=2, column="CREATED_ID", value=creators)
    return read_tickets.to_csv(tickets_csv, index=False)

def create_ticketdata():
    '''
    docstring
    '''
    with open(spiceworks_json, 'r',encoding='utf-8') as spiceworks_data:
        swd = json.load(spiceworks_data)
        spiceworks_users = swd["users"]
        for swu in spiceworks_users:
            write_usercsv(swu)
        spiceworks_tickets = swd["tickets"]
        write_ticketcsv(spiceworks_tickets)
    return spiceworks_data.close()

if __name__ == "__main__":
    create_csvs(user_csv,
        'USERID,EMAIL,NAME,FULLNAME'
        )
    create_csvs(tickets_csv,
        'TICKET_NO,ASSIGNED_ID,CREATED_ID,CREATED_AT,STATUS,SUMMARY,DESCRIPTION,COMMENTS'
        )
    create_ticketdata()
    assign_userids()
