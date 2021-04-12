from flask import Flask, render_template, request, session
from webexteamssdk import WebexTeamsAPI, Webhook
import utils.webex_utils as wbxu
import os

EXTERNAL_WEBHOOK_URL = 'http://ea6a010a828e.ngrok.io'
MESSAGE_WEBHOOK_RESOURCE = "messages"
MESSAGE_WEBHOOK_EVENT = "created"
CARDS_WEBHOOK_RESOURCE = "attachmentActions"
CARDS_WEBHOOK_EVENT = "created"

app = Flask(__name__)
app.secret_key = "sachal"

@app.route("/home", methods=["GET"])
def home_page():
	return "okay"

@app.route("/", methods=["POST", "DELETE"])
def webex_teams_webhook_events():
    """Respond to inbound webhook JSON HTTP POST from Webex Teams."""
    # Create a Webhook object from the JSON data
    webhook_obj = Webhook(request.json)
    print(webhook_obj)
    if(webhook_obj.resource == MESSAGE_WEBHOOK_RESOURCE
            and webhook_obj.event == MESSAGE_WEBHOOK_EVENT):
        wbxu.respond_to_message_event(webhook_obj)
    elif(webhook_obj.resource == CARDS_WEBHOOK_RESOURCE
          and webhook_obj.event == CARDS_WEBHOOK_EVENT):
        pass
    else:
        print(f"IGNORING UNEXPECTED WEBHOOK:\n{webhook_obj}")
    return "OK"
    
def main():
    webhook_url = EXTERNAL_WEBHOOK_URL
    wbxu.delete_webhooks_with_name()
    wbxu.create_webhooks(webhook_url)
    port = int(os.environ.get("PORT", 7001))
    try:
        app.run(host="localhost", port=port, debug=True)

    finally:
        print("Cleaning up webhooks...")
        wbxu.delete_webhooks_with_name()

if __name__ == "__main__":
    main()
    
