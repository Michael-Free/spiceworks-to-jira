'''

░█▀▀▀█ █▀▀█ ─▀─ █▀▀ █▀▀ ░█──░█ █▀▀█ █▀▀█ █─█ █▀▀
─▀▀▀▄▄ █──█ ▀█▀ █── █▀▀ ░█░█░█ █──█ █▄▄▀ █▀▄ ▀▀█
░█▄▄▄█ █▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀ ░█▄▀▄█ ▀▀▀▀ ▀─▀▀ ▀─▀ ▀▀▀

Filename: spiceworks.py

Created By: Michael Free

Summary:
Simple module for parsing through exported json
files from spiceworks exports.

Description:

To Dos:
- proper code linting (9.0+/10 score)
- docstring documentation
- testing modules
- exception handling
'''
import json
from io import StringIO
from html.parser import HTMLParser
class MLStripper(HTMLParser):
    '''
    Inputs:
    Outputs:
    Summary:

    stripper class
    '''
    def __init__(self):
        '''
        Inputs:
        Outputs:
        Summary:
        '''
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, data):
        '''
        Inputs:
        Outputs:
        Summary:
        '''
        self.text.write(data)
    def get_data(self):
        '''
        Inputs:
        Outputs:
        Summary:
        '''
        return self.text.getvalue()

def strip_html_tags(ticket_object):
    '''
    Inputs:
    Outputs:
    Summary:
    '''
    strip_html = MLStripper()
    strip_html.feed(ticket_object)
    return repr(strip_html.get_data().replace("\'","’"))

def write_to_csv(csv_data, csv_file):
    '''
    Inputs:
    Outputs:
    Summary:
    '''
    with open(csv_file, "a+", encoding="utf-8") as write_data:
        write_data.write(csv_data)
        write_data.close()

def create_user_table(spiceworks_json, user_csvfile):
    '''
    Inputs:
    Outputs:
    Summary:
    '''
    with open(spiceworks_json, 'r', encoding='utf-8') as read_users:
        user_data = json.load(read_users)
        user_list = user_data["users"]
        for user_info in user_list:
            if user_info["role"] == "admin":
                csv_info = ("\n"+
                    str(user_info["import_id"])+
                    ","+user_info["email"]+
                    ","+user_info["first_name"]+
                    ","+user_info["first_name"]+
                    " "+user_info["last_name"]+
                    ","+"ADMIN"
                    )
                write_to_csv(csv_info, user_csvfile)
            elif user_info["role"] == "helpdesk_admin":
                csv_info = ("\n"+
                    str(user_info["import_id"])+
                    ","+user_info["email"]+
                    ","+user_info["first_name"]+
                    ","+user_info["first_name"]+
                    " "+user_info["last_name"]+
                    ","+"HELPDESK"
                )
                write_to_csv(csv_info, user_csvfile)
            else:
                csv_info = ("\n"+str(user_info["import_id"])+
                    ","+user_info["email"]+
                    ", "+
                    ", "+
                    ","+"SUBMITTER"
                )
                write_to_csv(csv_info, user_csvfile)


def create_ticket_table(spiceworks_json, ticket_csvfile):
    '''
    Inputs:
    Outputs:
    Summary: table
    '''
    def parse_comments(comment_list):
        '''
        Inputs:
        Outputs:
        Summary:
        '''
        comments_made = {}
        comment_index = 0
        for comment_content in comment_list:
            comment_index += 1
            comments_made['comment'+str(comment_index)] = strip_html_tags(comment_content["body"])
        all_comments = ""
        for each_comment in comments_made:
            all_comments += str(
                comments_made[each_comment]+repr("\n")
                ).replace("\'","").replace("\"","").replace(",","")
        return all_comments

    def ticket_review(ticket_data, ticket_status, ticket_statustime):
        '''
        Inputs:
        Outputs:
        Summary: review
        '''
        if "description" in ticket_data:
            if "assigned_to" in ticket_data:
                if "Comments" in ticket_data:
                    ticket_with_comments = (
                    "\n"+str(ticket_data["assigned_to"])+
                    ","+str(ticket_data["created_by"])+
                    ",\""+ticket_data["created_at"]+
                    "\",\""+ticket_statustime+
                    "\",\""+ticket_status+
                    "\",\""+str(ticket_data["summary"]).strip(",")+
                    "\",\""+strip_html_tags(ticket_data["description"]).strip(",")+
                    "\",\""+parse_comments(ticket_data["Comments"]).strip(",")+
                    "\""
                    )
                    write_to_csv(ticket_with_comments, ticket_csvfile)
                else:
                    ticket_no_comments = (
                    "\n"+str(ticket_data["assigned_to"])+
                    ","+str(ticket_data["created_by"])+
                    ",\""+ticket_data["created_at"]+
                    "\",\""+ticket_statustime+
                    "\",\""+ticket_status+
                    "\",\""+str(ticket_data["summary"]).strip(",")+
                    "\",\""+strip_html_tags(ticket_data["description"]).strip(",")+
                    "\",\""+"NOCOMMENTS"+
                    "\""
                    )
                    write_to_csv(ticket_no_comments, ticket_csvfile)
            else:
                ticket_no_assignee = (
                    "\n"+str("NOASSIGNEE")+
                    ","+str(ticket_data["created_by"])+
                    ",\""+ticket_data["created_at"]+
                    "\",\""+ticket_statustime+
                    "\",\""+ticket_status+
                    "\",\""+str(ticket_data["summary"]).strip(",")+
                    "\",\""+strip_html_tags(ticket_data["description"]).strip(",")+
                    "\",\""+parse_comments(ticket_data["Comments"]).strip(",")+
                    "\""
                    )
                write_to_csv(ticket_no_assignee, ticket_csvfile)
        else:
            ticket_no_description = (
                "\n"+str(ticket_data["assigned_to"])+
                ","+str(ticket_data["created_by"])+
                ",\""+ticket_data["created_at"]+
                "\",\""+ticket_statustime+
                "\",\""+ticket_status+
                "\",\""+str(ticket_data["summary"]).strip(",")+
                "\",\""+"(no description)"+
                "\",\""+parse_comments(ticket_data["Comments"]).strip(",")+
                "\""
            )
            write_to_csv(ticket_no_description, ticket_csvfile)

    with open(spiceworks_json, "r", encoding="utf-8") as read_tickets:
        ticket_data = json.load(read_tickets)
        ticket_list = ticket_data["tickets"]
        for ticket_info in ticket_list:
            if ticket_info["status"] == "closed":
                ticket_review(ticket_info, "CLOSED", ticket_info["closed_at"])
            elif ticket_info["status"] == "open":
                ticket_review(ticket_info, "OPEN", " ")
            else:
                print(ticket_info)

if __name__ == "__main__":
    #create_ticket_table(os.getcwd()+'/exported_data.json', os.getcwd()+'/tickets.csv')
    #print(search_user_table(os.getcwd()+'/users.csv', "200"))
    print()
