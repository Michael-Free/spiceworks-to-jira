'''
▒█▀▀▀█ █▀▀█ ░▀░ █▀▀ █▀▀ █▀█ ░░░▒█ ▀█▀ ▒█▀▀█ ░█▀▀█ 
░▀▀▀▄▄ █░░█ ▀█▀ █░░ █▀▀ ░▄▀ ░▄░▒█ ▒█░ ▒█▄▄▀ ▒█▄▄█ 
▒█▄▄▄█ █▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀ █▄▄ ▒█▄▄█ ▄█▄ ▒█░▒█ ▒█░▒█

Filename: main.py

Created By: Michael Free

Summary:
GUI for prepping exported Spiceworks ticket data
for importation to Jira Service Management.

Description:


To Dos:
- Finalize Formatting for import to jira
- Code Linting
- some proper testing
- exception handling (goes with testing)
- arrange directory structure of repo
'''
import os
import json
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile, askdirectory
from modules.jira import map_user_ids, merge_comments, format_csvfile
from modules.spiceworks import create_user_table, create_ticket_table

json_data = ''
csv_data = ''

def open_jsonfile():
    '''
    - Open a json file
    - Verify Json Format
    - Doesn't verify if it's s.w. format
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
    - Select a directory
    - CSV files for users and tickets created
    - headers added to both CSV files.
    '''
    global csv_data
    def write_csv(file_path, headers):
        '''
        - receives path of file, and data
        - write data to the file
        '''
        with open(file_path,'w',encoding='utf-8') as csv_write:
            csv_write.write(headers)
            csv_write.close()

    def create_csvfiles(file_path):
        '''
        - creates a csv file on button press
        - users.csv and tickets.csv
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
    - populates the user table on button click
    - uses inputs from previous button presses
    '''
    user_table_button.set("loading...")
    create_user_table(json_data, csv_data+'/users.csv')
    user_table_button.set("User Table Created!")

def ticket_tables():
    '''
    - populates the tickets table on button click
    - uses inputs from previous button presses
    '''
    ticket_table_button.set("loading...")
    create_ticket_table(json_data, csv_data+'/tickets.csv')
    ticket_table_button.set("Ticket Table Created!")

def assign_userids():
    '''
    - on button press, user id numbers are looked up
    - email addresses are referenced to the user id
    - populates that data in the ticket table
    '''
    change_userid_button.set("parsing...")
    map_user_ids(csv_data+'/users.csv',csv_data+'/tickets.csv', csv_data)
    change_userid_button.set("Assigned User IDs!")

def merge_columns():
    '''
    - merges the description and comments column on button click
    - due to comment imports not supported for jira import
    - see jira.py for more information
    '''
    merge_comments_csv_button.set("merging...")
    merge_comments(csv_data+"/tickets.csv", csv_data)
    merge_comments_csv_button.set("Columns Merged!")

def final_format():
    '''
    - prepares tickets.csv for final formatting
    - interprets escape characters literally
    - see jira.py for mor information
    '''
    final_format_csv_button.set("formatting...")
    format_csvfile(csv_data+"/tickets.csv", csv_data)
    final_format_csv_button.set("Formatted!")

root = tk.Tk()
# set canvas size
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

final_format_csv = tk.Label(root, text="Interpret Escape Characters")
final_format_csv.grid(column=0, row=7)

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

final_format_csv_button = tk.StringVar()
final_format_csv_btn = tk.Button(root, textvariable=final_format_csv_button, command=lambda:final_format(), width=15)
final_format_csv_button.set("Final Formatting")
final_format_csv_btn.grid(column=2, row=7)

root.mainloop()