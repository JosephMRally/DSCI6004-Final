import json
import sys
import urllib.parse as urllib
from collections import OrderedDict
import requests
from flask import Flask, request

import Mongo
from engines import eliza
from engines import mrrogers_tfidf

app = Flask(__name__)
_engine = None
_db = Mongo.DB()

# This needs to be filled with the Page Access Token that will be provided
# by the Facebook App that will be created.
PAT = 'EAAKlBTVgof8BAOmqh2lLJoRbnZAbO5uG2p0xe5MR8XjrOtDyogMxMabAs5XZCrthaqfpLeA1gYAn3dtJThtOUCMN1C2GVGAP8rjZADhY0mGqAoQvVphNPjT4GGjaVEkFbhKIcAKZATQTu7Bp73vBfZBQ5a77lWLuQzzVWM85FwgZDZD'
APP_ID = 744391742366207

# TODO: research whether flask can do classes?


# TODO: factory pattern here to determine which engine to use
_engine = mrrogers_tfidf.Mrrogers_Tfidf()



@app.route('/', methods=['GET'])
def handle_verification():
    # http://localhost:5000?hub.verify_token=my_voice_is_my_password_verify_me&
    print("Handling Verification.")
    if request.args.get('hub.verify_token', '') == 'my_voice_is_my_password_verify_me':
        print("Verification successful!")
        return request.args.get('hub.challenge', '')
    else:
        print("Verification failed!")
        return "Error, wrong validation token"


@app.route('/', methods=['POST'])
def handle_messages():
    try:
        print("METHOD: handle_messages")
        payload = request.get_data()
        payload = payload.decode("utf-8")
        print("Payload: ", payload)
        for sender, message in messaging_events(str(payload)):
            print("Response to %s: %s" % (sender, message))
            send_message(PAT, sender, message)
        sys.stdout.flush()
        return "ok"
    except Exception as err:
        print('Exception!')
        print(str(err))
        # dont ever throw errors up the stack from hereon, don't crash the app domain
    finally:
        print('Completed')
        sys.stdout.flush()


def messaging_events(payload):
    """Generate tuples of (sender_id, message_text) from the
    provided payload.
    """
    try:
        print("METHOD messaging_events")
        data = json.loads(payload)
        _db.record_incoming_message(data) # record to the database
        messaging_events = data["entry"][0]["messaging"]
        for event in messaging_events:
            if "message" in event and "text" in event["message"]:
                #print(type(event["message"]["text"])) #str
                s = event["message"]["text"].encode('unicode_escape')
                #print(type(s)) #byte?
                s = str(s.decode("utf-8"))
                #print("received: ", s)
                response = _engine.analyze(s)
                yield event["sender"]["id"], response
            else:
                yield event["sender"]["id"], "I can't echo this"
    except Exception as err:
        print("Exception!")
        print(str(err))
        #raise err  # dont ever throw errors up the stack from hereon, don't crash the app domain
    finally:
        print('messaging_events completed')
        sys.stdout.flush()


def send_message(token, recipient, text):
    """Send the message text to recipient with id recipient.
    """
    try:
        print("send_message")

        text = text[:640] # TODO: wrong place for this

        #make the request to facebook

        # data = json.dumps({
        #     "recipient": {"id": recipient},
        #     "message": {"text": text}
        # })

        data = OrderedDict()
        data['sender'] = {"id": APP_ID}
        data['recipient'] = {"id": recipient}
        data['message'] = {
                "attachment": {
                    "type": "video",
                    "payload": {"url": "https://www.youtube.com/watch?v=XwvjMg_O_Wg"}
                }
            }

        data = json.dumps(data)
        print("data: ", data)

        r = requests.post("https://graph.facebook.com/v2.6/me/messages",
            params={"access_token": token},
            data=data,
            headers={'Content-type': 'application/json'})
        if r.status_code != requests.codes.ok:
            print(r.text)

        #record to database
        # data = {
        #     "recipient": {"id": recipient},
        #     "message": {"text": text}
        # }

        _db.record_outgoing_message(dict(data)) # record message to the database
    except Exception as err:
        print("Exception! method: send_message")
        print(str(err))
        #raise err # dont ever throw errors up the stack from hereon, don't crash the app domain
    finally:
        print('send_message Completed')
        sys.stdout.flush()


if __name__ == '__main__':
    app.run()

