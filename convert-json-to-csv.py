import json
from multiprocessing.pool import TERMINATE
import os
import pandas as pd

current_directory=os.getcwd()
spiceworks_json=current_directory+"/exported_data.json"

def create_usercsv():
    spiceworks_users_write = open(current_directory+'/users.csv', 'w', encoding='utf-8')
    spiceworks_users_write.write("USERID,EMAIL,NAME,FULLNAME")
    spiceworks_users_write.close()

def write_usercsv(userdata):
    spiceworksusers_append = open(current_directory+'/users.csv', 'a+', encoding='utf-8')
    if userdata["role"] == "admin":
        spiceworksusers_append.write("\n"+str(userdata["import_id"])+","+userdata["email"]+","+userdata["first_name"]+","+userdata["first_name"]+" "+userdata["last_name"])
    elif userdata["role"] == "helpdesk_admin":
        spiceworksusers_append.write("\n"+str(userdata["import_id"])+","+userdata["email"]+","+userdata["first_name"]+","+userdata["first_name"]+" "+userdata["last_name"])
    else:
        spiceworksusers_append.write("\n"+str(userdata["import_id"])+","+userdata["email"]+",,")
    spiceworksusers_append.close()

def create_ticketcsv():
    spiceworks_tickets_write = open(current_directory+'/tickets.csv', 'w', encoding='utf-8')
    spiceworks_tickets_write.write("TICKET_NO,ASSIGNED_ID,CREATED_ID,CREATED_AT,STATUS,SUMMARY,DESCRIPTION,COMMENTS")
    spiceworks_tickets_write.close()

def write_ticketcsv(ticketdata):
    count_tickets = 0
    for swt in ticketdata:
        if 'assigned_to' in swt:
            count_tickets +=1
            # ticket description dump
            if 'description' in swt:
                description_content = repr(swt["description"]).replace(',','.')
            elif 'description' not in swt:
                description_content = ''
            else:
                print(swt.keys())
            # write to comments txt file
            comment_log=current_directory+"/comments/"+str(count_tickets)+".txt"
            comment_write=open(comment_log,'w', encoding='utf-8')
            comment_write.write(str(swt["Comments"]))
            comment_write.close()
            #write to tickets.csv
            tickets_write = open(current_directory+"/tickets.csv",'a+',encoding='utf-8')
            tickets_write.write("\n"+str(count_tickets)+","+str(swt["assigned_to"])+","+str(swt["created_by"])+","+swt["created_at"]+","+swt["status"]+","+str(swt["summary"]).replace(',','.').replace('\n','')+","+description_content+","+comment_log)
            tickets_write.close()
        else:
            print(swt.keys())

def user_lookup(user_id):
    users_csv = pd.read_csv(current_directory+"/users.csv", index_col=False)
    user_row = users_csv.loc[users_csv['USERID'] == user_id]
    user_email= user_row.EMAIL.to_string(index=False)
    return user_email

with open(spiceworks_json, 'r',encoding='utf-8') as spiceworks_data:
    swd = json.load(spiceworks_data)
    spiceworks_users = swd["users"]
    # maybe do some threading here
    create_usercsv()
    for swu in spiceworks_users:
        write_usercsv(swu)
    spiceworks_tickets = swd["tickets"]
    create_ticketcsv()
    # maybe do some threading here
    write_ticketcsv(spiceworks_tickets)
    spiceworks_data.close()

# look up assigned_to value in user_lookup write it to a list
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
print(read_tickets)
read_tickets.to_csv('tickets_sofar.csv', index=False)
#print(creators)
'''
#if user_id in users_csv.USERID:
        #user_row = users_csv.loc[users_csv['USERID'] == user_id]
'''