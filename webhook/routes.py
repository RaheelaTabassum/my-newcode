from flask import Flask,Blueprint,json,render_template,request
import sys
import pymongo
from pymongo import MongoClient
# __name__ is a special built-in variable that holds the name of the current module (or file) being executed. It helps you understand whether your code is being run as the main program or being imported into another module.

# MongoDB Connection
client = MongoClient('mongodb://localhost:27017/')
db = client['notification_DATABASE']
events_collection = db['nevents']


app =Flask(__name__)
# If the module is being run directly, __name__ will be set to '__main__'.
# If the module is being imported, __name__ will be set to the module's name.
webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/')
def ping():
    print(" checks the get for notification")
    return "ping received"

@webhook.route('/checkevents', methods=["POST"])
def checkevents():
    data = request.json # extracting the data from webhook by requesting request in json format
    # headers=request.headers # e
    # print ("headers")
    # sys.stdout.flush()
    # for key,value in headers.items():
    #     print(f"{key},{value}")
    # sys.stdout.flush()

    event_type = request.headers.get("X-GitHub-Event")
    print(f"event_type: {event_type}")
    sys.stdout.flush()
    # print(f"DATA:{json.dumps(data)}") #printing the data that we received from the webhook 
    # sys.stdout.flush()

   
    if event_type == 'push':
        author=data.get("pusher",{}).get("name")
        to_branch=data.get("ref").split("/")[-1]
        timestamp=data.get("head_commit",{}).get("timestamp")
        message=(f"{author} pushed to {to_branch} on {timestamp}")

        print(message)
        sys.stdout.flush()

        # Store in MongoDB
        events_collection.insert_one({
            "event_type": "push",
            "author": author,
            "to_branch": to_branch,
            "timestamp": timestamp,
            "data": data  # You can store the entire payload if needed
        })

    elif event_type =='pull_request':
        #

        action = data.get("action")
        print(f"ACTION: {action}")
        sys.stdout.flush()

        author = data.get("pull_request", {}).get("user", {}).get("login")
        from_branch = data.get("pull_request", {}).get("head", {}).get("ref")
        to_branch = data.get("pull_request", {}).get("base", {}).get("ref")
        timestamp = data.get("pull_request", {}).get("created_at")

        print(f"Pull   Request Data: author={author}, from_branch={from_branch}, to_branch={to_branch}, timestamp={timestamp}")
        sys.stdout.flush()

        if action == "opened":
            message = f'{author} submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp}'
        elif action == "closed" and data.get("pull_request", {}).get("merged"):
            message = f'{author} merged branch "{from_branch}" to "{to_branch}" on {timestamp}'
        else:
            message = "Unhandled pull request event"

        print(message)

        sys.stdout.flush()


        events_collection.insert_one({
            "event_type": "pull_request",
            "author": author,
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": timestamp,
            "data": data  # Store entire payload if needed
        })



    return " data is recieved",200



app.register_blueprint(webhook)

if __name__ == '__main__':
    app.run(port =5500,debug=True)





# \C:\Users\pc\Desktop\RAHEELA