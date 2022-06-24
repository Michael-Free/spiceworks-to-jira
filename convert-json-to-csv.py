import json
import os
import pandas as pd

current_directory=os.getcwd()
spiceworks_json=current_directory+'/exported_data.json'
users_csv=current_directory+'/users.csv'
tickets_csv=current_directory+'/tickets.csv'

def create_csvs(csv_file,csv_headers):
    csv_write = open(csv_file,'w',encoding='utf-8')
    csv_write.write(csv_headers)
    csv_write.close()
    
def create_usercsv():
    spiceworks_users_write = open(current_directory+'/users.csv', 'w', encoding='utf-8')
    spiceworks_users_write.write("USERID,EMAIL,NAME,FULLNAME")
    spiceworks_users_write.close()

def write_usercsv(userdata):
    spiceworksusers_append = open(current_directory+'/users.csv', 'a+', encoding='utf-8')
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
        spiceworksusers_append.write("\n"+str(userdata["import_id"])+","+userdata["email"]+", ,")
    spiceworksusers_append.close()

def write_ticketcsv(ticketdata):
    count_tickets = 0
    for swt in ticketdata:
        if 'assigned_to' in swt:
            count_tickets +=1
            if 'description' in swt:
                description_content = repr(swt["description"]).replace(',','.')
            elif 'description' not in swt:
                description_content = ' '
            else:
                print(swt.keys())
            tickets_write = open(current_directory+"/tickets.csv",'a+',encoding='utf-8')
            tickets_write.write(
                "\n"+str(count_tickets)+
                ","+str(swt["assigned_to"])+
                ","+str(swt["created_by"])+
                ","+swt["created_at"]+
                ","+swt["status"]+
                ","+str(swt["summary"]).replace(',','.').replace('\n',' ')+
                ","+description_content.replace('\'','').replace('\"','')+
                ","+format_comments(swt["Comments"])
                )
            tickets_write.close()
        else:
            print("ASSIGNED TO ISSUE")
            print(swt.keys())

def user_lookup(user_id):
    users_csv = pd.read_csv(current_directory+"/users.csv", index_col=False)
    user_row = users_csv.loc[users_csv['USERID'] == user_id]
    user_email= user_row.EMAIL.to_string(index=False)
    return user_email

def format_comments(commentdata):
    for comments in range(len(commentdata)):
        comment_dict = commentdata[comments]
        ticket_comments = str(
            "UPDATED AT: "+
            comment_dict['updated_at']+
            " BY: "+user_lookup(comment_dict['created_by'])+
            repr("\n")+
            repr(comment_dict['body']).replace(',','.').replace('\'','').replace('\"','').replace('\'','')
            )
    return ticket_comments

def assign_userids():
    read_tickets = pd.read_csv(current_directory+"/tickets.csv")
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
    read_tickets.to_csv(current_directory+'/tickets_excelview.csv', index=False)

def create_ticketdata():
    with open(spiceworks_json, 'r',encoding='utf-8') as spiceworks_data:
        swd = json.load(spiceworks_data)
        spiceworks_users = swd["users"]
        create_usercsv()
        for swu in spiceworks_users:
            write_usercsv(swu)
        spiceworks_tickets = swd["tickets"]
        write_ticketcsv(spiceworks_tickets)
        spiceworks_data.close()

create_csvs(users_csv, 'USERID,EMAIL,NAME,FULLNAME')
create_csvs(tickets_csv,'TICKET_NO,ASSIGNED_ID,CREATED_ID,CREATED_AT,STATUS,SUMMARY,DESCRIPTION,COMMENTS')
create_ticketdata()
assign_userids()
#codecs.open(file, 'r', encoding='unicode_escape')
