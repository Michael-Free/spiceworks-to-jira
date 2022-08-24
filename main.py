'''
▒█▀▀▀█ █▀▀█ ░▀░ █▀▀ █▀▀ █▀█ ░░░▒█ ▀█▀ ▒█▀▀█ ░█▀▀█ 
░▀▀▀▄▄ █░░█ ▀█▀ █░░ █▀▀ ░▄▀ ░▄░▒█ ▒█░ ▒█▄▄▀ ▒█▄▄█ 
▒█▄▄▄█ █▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀ █▄▄ ▒█▄▄█ ▄█▄ ▒█░▒█ ▒█░▒█

Filename:
Created By:
Description:
Summary:
To Dos:

'''
import os
import json
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk
from jira import map_user_ids, merge_comments
from tkinter.filedialog import askopenfile, askdirectory
from spiceworks import create_user_table, create_ticket_table

json_data = ''
csv_data = ''

def open_jsonfile():
    '''
    Inputs:
    Outputs:
    Summary:

    Opens a JSON file
    Verifies that it's JSON format
    (it doesn't verify it's correct spiceworks format)
    '''
    global json_data
    json_button.set("loading...")
    json_file = askopenfile(parent=root, title='Choose Spiceworks JSON Datafile:', filetypes = (('json files','*.json'),('all files','*.*')))
    if json_file:
        try:
            with open(json_file.name, 'r', encoding='utf-8') as json_verify:
                json.load(json_verify)
                json_button.set("JSON Verified!")
                json_data = json_file.name
            json_verify.close()
        except ValueError:
            json_button.set("Bad JSON Format!")

def open_csvdir():
    '''
    Inputs:
    Outputs:
    Summary:

    Choose the directory where csv files will be written
    '''
    global csv_data
    def write_csv(file_path, headers):
        '''
        Inputs:
        Outputs:
        Summary:
        Writes data to a csv file
        '''
        with open(file_path,'w',encoding='utf-8') as csv_write:
            csv_write.write(headers)
            csv_write.close()

    def create_csvfiles(file_path):
        '''
        Inputs:
        Outputs:
        Summary:
        creates csv files with headers needed later on
        '''
        csv_button.set("loading...")

        users_csv = file_path+"/users.csv"
        tickets_csv = file_path+"/tickets.csv"

        if Path(users_csv).is_file():
            os.remove(users_csv)
            write_csv(users_csv, "USERID,EMAIL,NAME,FULLNAME,ROLE")
        else:
            write_csv(users_csv, "USERID,EMAIL,NAME,FULLNAME,ROLE")

        if Path(tickets_csv).is_file():
            os.remove(tickets_csv)
            write_csv(tickets_csv, "ASSIGNED_ID,CREATED_ID,CREATED_AT,CLOSED_AT,STATUS,SUMMARY,DESCRIPTION,COMMENTS")
        else:
            write_csv(tickets_csv, "ASSIGNED_ID,CREATED_ID,CREATED_AT,CLOSED_AT,STATUS,SUMMARY,DESCRIPTION,COMMENTS")
        csv_button.set("CSV Files Created!")
    
    csv_dir = askdirectory(parent=root, title='Choose CSV Output Directory:')
    if csv_dir:
        create_csvfiles(csv_dir)
        csv_data = csv_dir

def user_tables():
    '''
    Inputs:
    Outputs:
    Summary:

    calls create_user_table and populates the users.csv file
    '''
    user_table_button.set("loading...")
    create_user_table(json_data, csv_data+'/users.csv')
    user_table_button.set("User Table Created!")

def ticket_tables():
    '''
    Inputs:
    Outputs:
    Summary:

    calls create_user_table and populates the tickets.csv file
    '''
    ticket_table_button.set("loading...")
    create_ticket_table(json_data, csv_data+'/tickets.csv')
    ticket_table_button.set("Ticket Table Created!")

def assign_userids():
    '''
    Inputs:
    Outputs:
    Summary:
    '''
    change_userid_button.set("parsing...")
    map_user_ids(csv_data+'/users.csv',csv_data+'/tickets.csv', csv_data)
    change_userid_button.set("Assigned User IDs!")

def merge_columns():
    '''
    Inputs:
    Outputs:
    Summary:
    '''
    merge_comments_csv_button.set("merging...")
    merge_comments(csv_data+"/tickets.csv", csv_data)
    merge_comments_csv_button.set("Columns Merged!")
    return

root = tk.Tk()

canvas = tk.Canvas(root, width=600, height=200, bg='white')
canvas.grid(columnspan=3)

#logo
logo = Image.open('spice2jira-logo.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=1, row=0)

#labels
json_filelabel = tk.Label(root, text="Choose a JSON File")
json_filelabel.grid(column=0, row=1)

csv_outputlabel = tk.Label(root, text="Choose CSV Directory")
csv_outputlabel.grid(column=0, row=2)

user_outputlabel = tk.Label(root, text="Create User Table")
user_outputlabel.grid(column=0, row=3)

ticket_outputlabel = tk.Label(root, text="Create Ticket Table")
ticket_outputlabel.grid(column=0, row=4)

change_user_id_email = tk.Label(root, text="Change User IDs to Emails")
change_user_id_email.grid(column=0, row=5)

merge_comments_csv = tk.Label(root, text="Merge Desc. & Comments")
merge_comments_csv.grid(column=0, row=6)

#buttons
json_button = tk.StringVar()
json_btn = tk.Button(root, textvariable=json_button, command=lambda:open_jsonfile(), width=15)
json_button.set("Select JSON File")
json_btn.grid(column=2, row=1)

csv_button = tk.StringVar()
csv_btn = tk.Button(root, textvariable=csv_button, command=lambda:open_csvdir(), width=15)
csv_button.set("Select CSV Dir")
csv_btn.grid(column=2, row=2)

user_table_button = tk.StringVar()
user_table_btn = tk.Button(root, textvariable=user_table_button, command=lambda:user_tables(), width=15)
user_table_button.set("Create User Table")
user_table_btn.grid(column=2,row=3) 

ticket_table_button = tk.StringVar()
ticket_table_btn = tk.Button(root, textvariable=ticket_table_button, command=lambda:ticket_tables(), width=15)
ticket_table_button.set("Create Ticket Table")
ticket_table_btn.grid(column=2,row=4)

change_userid_button = tk.StringVar()
change_userid_btn = tk.Button(root, textvariable=change_userid_button, command=lambda:assign_userids(), width=15)
change_userid_button.set("Change User IDs")
change_userid_btn.grid(column=2, row=5)

merge_comments_csv_button = tk.StringVar()
merge_comments_csv_btn = tk.Button(root, textvariable=merge_comments_csv_button, command=lambda:merge_columns(), width=15)
merge_comments_csv_button.set("Merge Columns")
merge_comments_csv_btn.grid(column=2, row=6)

root.mainloop()