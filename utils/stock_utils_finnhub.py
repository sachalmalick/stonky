import requests
import datetime as dt
import json

API_KEY = "c1cclov48v6scqmqrcd0"
BASE_URL = "https://finnhub.io/api/v1"

exceeded_message = "You've exceeded the maximum requests per minute"

def format_request_url(url, arguments):
    first = True
    for k,v in arguments.items():
        if(first):
            first = False
            url = url + "?"
        else:
            url = url + "&"
        url = url + str(k) + "=" + str(v)
    return url

def get_request(url, headers={}, **kwargs):
    url = format_request_url(url, dict(kwargs))
    print(url)
    response = requests.get(url, headers=headers)
    return response

def check_error(result):
    if(result.get("status") == "ERROR"):
        if(exceeded_message in result.get("error")):
            return "API_REQUEST_LIMIT"
        return "UNKOWN_ERROR"
    return False

def get_price(ticker):
    url = BASE_URL + "/quote?symbol={}&token={}".format(ticker, API_KEY)
    response = get_request(url)
    result = dict(json.loads(response.text))
    return result

def get_news(ticker, pages=1, numperpage=5):
    url = "https://api.polygon.io/v1/meta/symbols/{}/news?perpage={}&page={}&apiKey={}".format(ticker, numperpage, pages, API_KEY)
    response = json.loads(get_request(url).text)
    if(isinstance(response, list)):
        return response
    if(response.get("status") == "ERROR"):
        if(exceeded_message in response.get("error")):
            return "API_REQUEST_LIMIT"
    return "UNKOWN_ERROR"

def get_info(ticker):
    url = "https://api.polygon.io/v1/meta/symbols/{}/company?&apiKey={}".format(ticker, API_KEY)
    response = json.loads(get_request(url).text)
    if(response.get("error") != None):
        if(exceeded_message in response.get("error")):
            return "API_REQUEST_LIMIT"
        if(response.get("error") == "Not Found"):
            return "UNKOWN_TICKER"
        print(response)
        return "UNKOWN"
    return response

print(get_price("efef"))