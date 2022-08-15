'''
spiceworks
parse out commas in summary and descriptions!
if not quote them out
'''
import json
import os
from io import StringIO
from html.parser import HTMLParser
class MLStripper(HTMLParser):
    '''
    stripper class
    '''
    def __init__(self):
        '''
        bs
        '''
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        '''
        more bs
        '''
        self.text.write(d)
    def get_data(self):
        '''
        best bs
        '''
        return self.text.getvalue()

def strip_html_tags(ticket_object):
    '''
    strip
    '''
    strip_html = MLStripper()
    strip_html.feed(ticket_object)
    return repr(strip_html.get_data())

def write_to_csv(csv_data, csv_file):
    '''
    write
    '''
    with open(csv_file, "a+", encoding="utf-8") as write_data:
        write_data.write(csv_data)
        write_data.close()

def create_user_table(spiceworks_json, user_csvfile):
    '''
    user table
    '''
    with open(spiceworks_json, 'r', encoding='utf-8') as read_users:
        user_data = json.load(read_users)
        user_list = user_data["users"]
        for user_info in user_list:
            if user_info["role"] == "admin":
                # append to csv function:
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

def search_user_table():
    '''
    search
    '''
    return

def create_ticket_table(spiceworks_json, ticket_csvfile):
    '''
    ticket table
    '''
    def parse_comments(comment_list):
        '''
        parse
        '''
        comments_made = {}
        comment_index = 0
        for comment_content in comment_list:
            comment_index += 1
            comments_made['comment'+str(comment_index)] = comment_content["body"]
            comments_made['created_at'] = comment_content["created_at"]
        return comments_made

    def ticket_review(ticket_data):
        '''
        ticket review
        '''
        if "description" in ticket_data:
            if "assigned_to" in ticket_data:
                if "Comments" in ticket_data:
                    ticket_with_comments = (
                    "\n"+str(ticket_data["assigned_to"])+
                    ","+str(ticket_data["created_by"])+
                    ","+ticket_data["created_at"]+
                    ","+ticket_data["closed_at"]+
                    ","+"CLOSED"+
                    ","+ticket_data["summary"]+
                    ","+strip_html_tags(ticket_data["description"])+
                    ","+str(parse_comments(ticket_data["Comments"]))
                    )
                    write_to_csv(ticket_with_comments, ticket_csvfile)
                else:
                    ticket_no_comments = (
                    "\n"+str(ticket_data["assigned_to"])+
                    ","+str(ticket_data["created_by"])+
                    ","+ticket_data["created_at"]+
                    ","+ticket_data["closed_at"]+
                    ","+"CLOSED"+
                    ","+ticket_data["summary"]+
                    ","+strip_html_tags(ticket_data["description"])+
                    ","+"NOCOMMENTS"
                    )
                    write_to_csv(ticket_no_comments, ticket_csvfile)
            else:
                ticket_no_assignee = (
                    "\n"+str("NOASSIGNEE")+
                    ","+str(ticket_data["created_by"])+
                    ","+ticket_data["created_at"]+
                    ","+ticket_data["closed_at"]+
                    ","+"CLOSED"+
                    ","+ticket_data["summary"]+
                    ","+strip_html_tags(ticket_data["description"])+
                    ","+str(parse_comments(ticket_data["Comments"]))
                    )
                write_to_csv(ticket_no_assignee, ticket_csvfile)
        else:
            ticket_no_description = (
                "\n"+str(ticket_data["assigned_to"])+
                ","+str(ticket_data["created_by"])+
                ","+ticket_data["created_at"]+
                ","+ticket_data["closed_at"]+
                ","+"CLOSED"+
                ","+ticket_data["summary"]+
                ","+"(no description)"+
                ","+str(parse_comments(ticket_data["Comments"]))
            )
            write_to_csv(ticket_no_description, ticket_csvfile)

    with open(spiceworks_json, "r", encoding="utf-8") as read_tickets:
        ticket_data = json.load(read_tickets)
        ticket_list = ticket_data["tickets"]
        for ticket_info in ticket_list:
            if ticket_info["status"] == "closed":
                ticket_review(ticket_info)
            elif ticket_info["status"] == "open":
                ticket_review(ticket_info)
            else:
                print(ticket_info)

if __name__ == "__main__":
    create_ticket_table(os.getcwd()+'/exported_data.json', os.getcwd()+'/tickets.csv')
