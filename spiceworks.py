import json
import os
from io import StringIO
from html.parser import HTMLParser
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def write_to_csv(csv_data, csv_file):
    with open(csv_file, "a+", encoding="utf-8") as write_data:
        write_data.write(csv_data)
        write_data.close()

def create_user_table(spiceworks_json, user_csvfile):
    with open(spiceworks_json, 'r', encoding='utf-8') as read_users:
        user_data = json.load(read_users)
        user_list = user_data["users"]
        for user_info in user_list:
            if user_info["role"] == "admin":
                # append to csv function:
                csv_info = ("\n"+str(user_info["import_id"])+
                    ","+user_info["email"]+
                    ","+user_info["first_name"]+
                    ","+user_info["first_name"]+
                    " "+user_info["last_name"]+
                    ","+"ADMIN"
                    )
                write_to_csv(csv_info, user_csvfile)
            elif user_info["role"] == "helpdesk_admin":
                csv_info = ("\n"+str(user_info["import_id"])+
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
    return

def create_ticket_table(spiceworks_json):
    def strip_html_tags(ticket_object):
        s = MLStripper()
        s.feed(ticket_object)
        return repr(s.get_data())
    
    def parse_comments(comment_list):
        comments_made = {}
        comment_index = 0
        for comment_content in comment_list:
            comment_index += 1
            comments_made['comment'+str(comment_index)] = comment_content["body"]
            comments_made['created_at'] = comment_content["created_at"]
        return comments_made

    #ticket_data = json.load(spiceworks_json)
    with open(spiceworks_json, "r", encoding="utf-8") as read_tickets:
        ticket_data = json.load(read_tickets)
        ticket_list = ticket_data["tickets"]
        for ticket_info in ticket_list:
            if ticket_info["status"] == "closed":
                # if key description exists
                if "description" in ticket_info:
                    if "assigned_to" in ticket_info:
                        # if comments exist
                        if "Comments" in ticket_info:
                            ticket_with_comments = (str(ticket_info["assigned_to"])+
                            ","+str(ticket_info["created_by"])+
                            ","+ticket_info["created_at"]+
                            ","+ticket_info["closed_at"]+
                            ","+ticket_info["summary"]+
                            # need summary here of ticket
                            ","+strip_html_tags(ticket_info["description"])+
                            ","+str(parse_comments(ticket_info["Comments"]))
                            )
                            #print(ticket_with_comments)                          
                        else:
                            # tickets with no comments
                            ticket_no_comments = "no comment"
                            print(ticket_no_comments)
                    else:
                        # tickets with no assignees
                        ticket_no_assignee = (str("NOASSIGNEE")+
                            ","+str(ticket_info["created_by"])+
                            ","+ticket_info["created_at"]+
                            ","+ticket_info["closed_at"]+
                            ","+ticket_info["summary"]+
                            ","+strip_html_tags(ticket_info["description"])+
                            ","+str(parse_comments(ticket_info["Comments"]))
                            )
                        #print(ticket_no_assignee)
                else:
                    #if no description, print keys
                    nodesc="nodesc"
                    #print(ticket_info)
                    #input()
            else:
                print("ticket is open") #print(ticket_info)

    #return

if __name__ == "__main__":
    create_ticket_table(os.getcwd()+'/exported_data.json')