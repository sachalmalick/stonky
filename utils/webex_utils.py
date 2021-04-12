import utils.stock_utils as stocks
from webexteamssdk import WebexTeamsAPI, Webhook
import json

BOTNAME = "Stocks "
PRICE_CARD = "data/pricecard.json"

WEBEX_TEAMS_ACCESS_TOKEN = str(open("atoke").read())

WEBHOOK_NAME = "Stocks Bot"
MESSAGE_WEBHOOK_RESOURCE = "messages"
MESSAGE_WEBHOOK_EVENT = "created"
CARDS_WEBHOOK_RESOURCE = "attachmentActions"
CARDS_WEBHOOK_EVENT = "created"


api = WebexTeamsAPI(WEBEX_TEAMS_ACCESS_TOKEN)
bot = api.people.me()

def get_element(title, url, source, datetime, image, summary):
    return {'speak': 'Stock News', 'type': 'ColumnSet', 'columns': [{'type': 'Column', 'width': 2, 'items': [{'type': 'TextBlock', 'text': source, 'wrap': True}, {'type': 'Image', 'url': image, 'altText': '{imageAlt}', 'size': 'Large', 'spacing': 'Medium', 'horizontalAlignment': 'Center'}, {'type': 'TextBlock', 'text': title, 'weight': 'Bolder', 'size': 'ExtraLarge', 'spacing': 'None', 'wrap': True}, {'type': 'TextBlock', '$when': datetime, 'text': datetime, 'isSubtle': True, 'spacing': 'None', 'wrap': True}, {'type': 'TextBlock', 'text': summary, 'size': 'Small', 'wrap': True, 'maxLines': 3}, {'type': 'TextBlock', 'text': '[View Full Article](' + url + ')', 'wrap': True, 'fontType': 'Default', 'size': 'Medium', 'horizontalAlignment': 'Center'}]}]}
    
def get_news_card(data):
    card = {'$schema': 'http://adaptivecards.io/schemas/adaptive-card.json', 'type': 'AdaptiveCard', 'version': '1.2', 'body': []}
    for article in data:
        card["body"].append(get_element(article["title"], article["url"], article["source"], article["timestamp"], article["image"], article["summary"]))
    return card


def get_summary_element(logo, title, description, ceo):
    return {'$schema': 'http://adaptivecards.io/schemas/adaptive-card.json', 'type': 'AdaptiveCard', 'version': '1.2', 'body': [{'speak': 'Stock News', 'type': 'ColumnSet', 'columns': [{'type': 'Column', 'width': 2, 'items': [{'type': 'Image', 'url': logo, 'altText': '{imageAlt}', 'size': 'Large', 'spacing': 'Medium', 'horizontalAlignment': 'Center'}, {'type': 'TextBlock', 'text': title, 'weight': 'Bolder', 'size': 'ExtraLarge', 'spacing': 'None', 'wrap': True, 'horizontalAlignment': 'Center'}, {'type': 'TextBlock', '$when': '2020-03-27T09:41:00.000Z', 'text': ceo, 'isSubtle': True, 'spacing': 'None', 'wrap': True, 'horizontalAlignment': 'Center'}, {"type": "TextBlock","text": description,"wrap": True},{'type': 'FactSet', 'facts': []}]}]}]}


SUMMARY_CARD_FIELDS = {"country": "Country",
 "industry": "Industry",
 "sector": "Sector",
 "marketcap": "Market Cap",
 "employees": "Employees",
 "phone": "Phone",
 "url": "URL",
 "exchange": "Exchange",
 "name": "Cisco Systems Inc.",
 "symbol": "CSCO",
 "hq_address": "Headquarters"}

def get_summary_card(data):
    logo, title, description, ceo = "","","",""
    logo = data.get("logo") if data.get("logo") != None else ""
    title = data.get("name") if data.get("name") != None else ""
    description = data.get("description") if data.get("description") != None else ""
    ceo = data.get("ceo") if data.get("ceo") != None else ""
    base_card = get_summary_element(logo, title, description, ceo)
    for key,value in data.items():
        if(key in SUMMARY_CARD_FIELDS):
            dic = {"title" : SUMMARY_CARD_FIELDS[key], "value" : str(value)}
            base_card["body"][0]["columns"][0]["items"][4]["facts"].append(dic)
    return base_card

def get_change_string(open_price, close_price):
    diff = close_price - open_price
    perc = diff/open_price
    up_symbol,down_symbol = '▲', '▼'
    symbol = up_symbol
    color = "good"
    if(diff < 0):
        symbol = down_symbol
        color = "attention"
    perc_str = "%.2f" % perc
    change = "%.2f" % diff
    change_str = symbol + " " + change + " USD (" + perc_str + "%)"
    return change_str, color

def update_price_card(json_card, ticker, latestPrice, changeString, color, facts):
    json_card["body"][0]["items"][0]["text"] = ticker
    json_card["body"][1]["items"][0]["columns"][0]["items"][0]["text"] = str(latestPrice)
    json_card["body"][1]["items"][0]["columns"][0]["items"][1]["text"] = changeString
    json_card["body"][1]["items"][0]["columns"][0]["items"][1]["color"] = color
    json_card["body"][1]["items"][0]["columns"][1]["items"][0]["facts"] = facts
    
def get_price_card(data):
    f = open(PRICE_CARD, "r")
    json_card = json.loads(f.read())
    results = data["results"]
    ticker = data["ticker"]
    open_dic = {"title": "Open","value": str(results["o"])}
    high_dic = {"title": "High","value": str(results["h"])}
    low_dic = {"title": "Low","value": str(results["l"])}
    facts = [open_dic,high_dic,low_dic]
    changeString,color = get_change_string(results["c"], results["pc"])
    update_price_card(json_card, ticker, results["c"], changeString, color, facts)
    return json_card

def send_price_card(room_id, data):
    card = get_price_card(data)
    attachments={"contentType": "application/vnd.microsoft.card.adaptive", "content": card}
    api.messages.create(room_id, text='Price Update', attachments=[attachments])

def show_last_price(data):
    split_text = data["message"].text.split(" ")
    if(len(split_text) < 3):
        msg = f"please include the stock ticker: '{BOTNAME} Prices <TICKER>'"
        return api.messages.create(data["room"].id, markdown=msg)
    ticker = split_text[2]
    error, result = stocks.get_previous_price(ticker)
    if(error == False):
        if(result["resultsCount"] == 0):
            msg = f"could not find any data for the ticker '{ticker}'"
            return api.messages.create(data["room"].id, markdown=msg)
        return send_price_card(data["room"].id, result)
    if(error == "API_REQUEST_LIMIT"):
        msg = f"I've reached my limit for the stocks api.  Please give me a minute to regain access and try again"
        return api.messages.create(data["room"].id, markdown=msg)
    unkown_msg = f"This is an embarassing. A weird error occurred.  Please try again!"
    return api.messages.create(data["room"].id, markdown=unkown_msg)

def send_news(data):
    split_text = data["message"].text.split(" ")
    if(len(split_text) < 3):
        msg = f"please include the stock ticker: '{BOTNAME} News <TICKER>'"
        return api.messages.create(data["room"].id, markdown=msg)
    ticker = split_text[2]
    result = stocks.get_news(ticker)
    if(result == "API_REQUEST_LIMIT"):
        msg = f"I've reached my limit for the stocks api.  Please give me a minute to regain access and try again"
        return api.messages.create(data["room"].id, markdown=msg)
    if(result == "UNKOWN_ERROR"):
        unkown_msg = f"This is an embarassing. A weird error occurred.  Please try again!"
        return api.messages.create(data["room"].id, markdown=unkown_msg)
    if(len(result) == 0):
        msg = f"No news found for {ticker}"
        return api.messages.create(data["room"].id, markdown=msg)
    card = get_news_card(result)
    print(json.dumps(card))
    attachments={"contentType": "application/vnd.microsoft.card.adaptive", "content": card}
    api.messages.create(data["room"].id, text='Company News', attachments=[attachments])
    
    
def send_info(data):
    split_text = data["message"].text.split(" ")
    if(len(split_text) < 3):
        msg = f"please include the stock ticker: '{BOTNAME} Profile <TICKER>'"
        return api.messages.create(data["room"].id, markdown=msg)
    ticker = split_text[2]
    result = stocks.get_info(ticker)
    if(result == "API_REQUEST_LIMIT"):
        msg = f"I've reached my limit for the stocks api.  Please give me a minute to regain access and try again"
        return api.messages.create(data["room"].id, markdown=msg)
    if(result == "UNKOWN"):
        unkown_msg = f"This is an embarassing. A weird error occurred.  Please try again!"
        return api.messages.create(data["room"].id, markdown=unkown_msg)
    if(result == "UNKOWN_TICKER"):
        msg = f"No info found for {ticker}"
        return api.messages.create(data["room"].id, markdown=msg)
    card = get_summary_card(result)
    attachments={"contentType": "application/vnd.microsoft.card.adaptive", "content": card}
    api.messages.create(data["room"].id, text='Company Info', attachments=[attachments])

    
def help_msg(data):
    help_message = open("README.md", "r").read()
    api.messages.create(data["room"].id,markdown=help_message)

MSG_RESPONSE_FUNS = {"prices" : show_last_price, "news" : send_news, "profile" : send_info, "help" : help_msg}

def respond_to_message_event(webhook):
    room = api.rooms.get(webhook.data.roomId)
    message = api.messages.get(webhook.data.id)
    print(message.text)
    person = api.people.get(message.personId)
    if(message.personId == bot.id):
        return
    data = {"room":room, "message" : message, "person" : person}
    response_function = None
    for identifier, func in MSG_RESPONSE_FUNS.items():
        print(BOTNAME + identifier)
        if(message.text.lower().startswith(BOTNAME.lower() + identifier)):
            response_function = func
            break
    if(response_function == None):
        response_message = f"I'm sorry, I don't understand '{message.text}'. For what I can do, type `{BOTNAME} help`."
        return api.messages.create(room.id, markdown=response_message)
    response_function(data)
    
def delete_webhooks_with_name():
    """List all webhooks and delete webhooks created by this script."""
    for webhook in api.webhooks.list():
        if webhook.name == WEBHOOK_NAME:
            print("Deleting Webhook:", webhook.name, webhook.targetUrl)
            api.webhooks.delete(webhook.id)



def create_webhooks(webhook_url):
    """Create the Webex Teams webhooks we need for our bot."""
    print("Creating Message Created Webhook...")
    webhook = api.webhooks.create(
        resource=MESSAGE_WEBHOOK_RESOURCE,
        event=MESSAGE_WEBHOOK_EVENT,
        name=WEBHOOK_NAME,
        targetUrl=webhook_url
    )
    print(webhook)
    print("Webhook successfully created.")

    print("Creating Attachment Actions Webhook...")
    webhook = api.webhooks.create(
        resource=CARDS_WEBHOOK_RESOURCE,
        event=CARDS_WEBHOOK_EVENT,
        name=WEBHOOK_NAME,
        targetUrl=webhook_url
    )
    print(webhook)
    print("Webhook successfully created.")

    
if __name__ == "__main__":
    print(send_price_card({'ticker': 'CSCO', 'queryCount': 1, 'resultsCount': 1, 'adjusted': False, 'results': [{'T': 'CSCO', 'v': 65366839.0, 'vw': 48.9485, 'o': 48.71, 'c': 48.98, 'h': 49.22, 'l': 48.32, 't': 1616184000000, 'n': 119534}], 'status': 'OK', 'request_id': 'ad45819a728a5be722b3ad8cb0b1d377', 'count': 1}))
    
    
    '''
    
    use a gif no computer frozen.
    
    '''