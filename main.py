
import json
import os
import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path
from tkinter.filedialog import askopenfile, askdirectory
from spiceworks import create_user_table

json_data = ''
csv_data = ''

def open_jsonfile():
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
    global csv_data
    def write_csv(file_path, headers):
        with open(file_path,'w',encoding='utf-8') as csv_write:
            csv_write.write(headers)
            csv_write.close()

    def create_csvfiles(file_path):
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
    
    csv_button.set("loading...")
    csv_dir = askdirectory(parent=root, title='Choose CSV Output Directory:')
    if csv_dir:
        create_csvfiles(csv_dir)
        csv_data = csv_dir

def user_tables():
    user_table_button.set("loading...")
    create_user_table(json_data, csv_data+'/users.csv')
    user_table_button.set("User Table Created!")
    #return



root = tk.Tk()

canvas = tk.Canvas(root, width=600, height=300, bg='white')
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
user_outputlabel = tk.Label(root, text="Create User Tables")
user_outputlabel.grid(column=0, row=3)

#buttons
json_button = tk.StringVar()
json_btn = tk.Button(root, textvariable=json_button, command=lambda:open_jsonfile())
json_button.set("Select JSON File")
json_btn.grid(column=2, row=1)

csv_button = tk.StringVar()
csv_btn = tk.Button(root, textvariable=csv_button, command=lambda:open_csvdir())
csv_button.set("Select CSV Dir")
csv_btn.grid(column=2, row=2)

user_table_button = tk.StringVar()
user_table_btn = tk.Button(root, textvariable=user_table_button, command=lambda:user_tables())
user_table_button.set("Create Table")
user_table_btn.grid(column=2,row=3) 

#ticket_table_button = tk.StringVar()
#ticket_table_btn = tk.Button(root, textvariable=ticket_table_button, command=lambda:open_csvdir())
#ticket_table_button.set("Create Table")
#ticket_table_btn.grid(column=2,row=3)

root.mainloop()