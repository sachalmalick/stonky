import json

dic = {
 "logo": "https://s3.polygon.io/logos/csco/logo.png",
 "listdate": "1994-01-03",
 "cik": "858877",
 "bloomberg": "EQ0010171100001000",
 "figi": None,
 "lei": "8E6NF1YAL0WT6CWXXV93",
 "sic": 3577,
 "country": "usa",
 "industry": "Communication Equipment",
 "sector": "Technology",
 "marketcap": 211876802073,
 "employees": 74200,
 "phone": "+1 408 526-4000",
 "ceo": "Charles H. Robbins",
 "url": "http://www.cisco.com",
 "description": "Cisco Systems Inc is a supplier of data networking equipment and software. Its products include routers, switches, access equipment, and security and network management software which allow data communication among dispersed computer networks.",
 "exchange": "Nasdaq Global Select",
 "name": "Cisco Systems Inc.",
 "symbol": "CSCO",
 "exchangeSymbol": "NGS",
 "hq_address": "170 West Tasman Drive San Jose CA, 95134-1706",
 "hq_state": "CA",
 "hq_country": "USA",
 "type": "CS",
 "updated": "11/16/2018",
 "tags": [
  "Technology",
  "Communication Equipment"
 ],
 "similar": [
  "MSFT",
  "CTXS",
  "FFIV",
  "NTGR",
  "ERIC",
  "JNPR",
  "IBM",
  "VMW",
  "MSI",
  "HPQ",
  "XLK"
 ],
 "active": True
}

def get_summary_element(logo, title, description, ceo):
    return {'$schema': 'http://adaptivecards.io/schemas/adaptive-card.json', 'type': 'AdaptiveCard', 'version': '1.3', 'body': [{'speak': 'Stock News', 'type': 'ColumnSet', 'columns': [{'type': 'Column', 'width': 2, 'items': [{'type': 'Image', 'url': logo, 'altText': '{imageAlt}', 'size': 'Large', 'spacing': 'Medium', 'horizontalAlignment': 'Center'}, {'type': 'TextBlock', 'text': title, 'weight': 'Bolder', 'size': 'ExtraLarge', 'spacing': 'None', 'wrap': True, 'horizontalAlignment': 'Center'}, {'type': 'TextBlock', '$when': '2020-03-27T09:41:00.000Z', 'text': ceo, 'isSubtle': True, 'spacing': 'None', 'wrap': True, 'horizontalAlignment': 'Center'}, {"type": "TextBlock","text": description,"wrap": True},{'type': 'FactSet', 'facts': []}]}]}]}


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

print(json.dumps(get_summary_card(dic)))