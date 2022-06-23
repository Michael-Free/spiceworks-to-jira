import json
from multiprocessing.pool import TERMINATE
import threading
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
            tickets_write.write("\n"+str(count_tickets)+","+str(swt["assigned_to"])+","+str(swt["created_by"])+","+swt["created_at"]+","+swt["status"]+","+str(swt["summary"]).replace(',','.')+","+description_content+","+comment_log)
            tickets_write.close()
        else:
            print(swt.keys())
def user_lookup(user_id):
    users_csv = pd.read_csv(current_directory+"/users.csv", index_col=False)
    if user_id in users_csv.USERID:
        user_row = users_csv.loc[users_csv['USERID'] == user_id]
        ## add in if userid doesn't exist
        if user_row.FULLNAME.to_string(index=False) == 'NaN':
            print(user_row.EMAIL.to_string(index=False))
        else:
            print(user_row.FULLNAME.to_string(index=False))

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

user_lookup(100)
