from flask import Flask, request
import json
import requests
import sys

import eliza

app = Flask(__name__)

# This needs to be filled with the Page Access Token that will be provided
# by the Facebook App that will be created.
PAT = 'EAAKlBTVgof8BAOmqh2lLJoRbnZAbO5uG2p0xe5MR8XjrOtDyogMxMabAs5XZCrthaqfpLeA1gYAn3dtJThtOUCMN1C2GVGAP8rjZADhY0mGqAoQvVphNPjT4GGjaVEkFbhKIcAKZATQTu7Bp73vBfZBQ5a77lWLuQzzVWM85FwgZDZD'

@app.route('/', methods=['GET'])
def handle_verification():
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
        print("handle_messages")
        payload = request.get_data()
        payload = payload.decode("utf-8")
        for sender, message in messaging_events(str(payload)):
            print("Incoming from %s: %s" % (sender, message))
            send_message(PAT, sender, message)
        sys.stdout.flush()
        return "ok"
    except Exception as err:
        print('Exception!')
        print(str(err))
    finally:
        print('Completed')
        sys.stdout.flush()


_elize = eliza.Eliza()
def messaging_events(payload):
    """Generate tuples of (sender_id, message_text) from the
    provided payload.
    """
    try:
        print("messaging_events")
        data = json.loads(payload)
        messaging_events = data["entry"][0]["messaging"]
        for event in messaging_events:
            if "message" in event and "text" in event["message"]:
                #yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
                s = event["message"]["text"].encode('unicode_escape')
                print("received: ", s)
                s = str(s.decode("utf-8"))
                response = _elize.analyze(s)
                yield event["sender"]["id"], response
            else:
                yield event["sender"]["id"], "I can't echo this"
    except Exception as err:
        print("Exception!")
        print(str(err))
        raise err
    finally:
        print('messaging_events completed')
        sys.stdout.flush()


def send_message(token, recipient, text):
    """Send the message text to recipient with id recipient.
    """
    try:
        print("send_message")
        r = requests.post("https://graph.facebook.com/v2.6/me/messages",
        params={"access_token": token},
        # data=json.dumps({
        #     "recipient": {"id": recipient},
        #     "message": {"text": text.decode('unicode_escape')}
        # }),
        data=json.dumps({
            "recipient": {"id": recipient},
            "message": {"text": text}
        }),
        headers={'Content-type': 'application/json'})
        if r.status_code != requests.codes.ok:
            print(r.text)
    except Exception as err:
        print("Exception!")
        print(str(err))
        raise err
    finally:
        print('send_message Completed')
        sys.stdout.flush()



if __name__ == '__main__':
    app.run()

