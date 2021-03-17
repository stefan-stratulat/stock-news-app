import requests
import json
import datetime as dt
import os

STOCK = "TSLA"
COMPANY_NAME = "Tesla"

## STEP 1: Use https://www.alphavantage.co to gather data for yesterday and day before.

#parameters for stock API
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": os.environ["API_ALPHAVANTAGE"]
}

stock_response = requests.get('https://www.alphavantage.co/query', params=stock_parameters)
stock_response.raise_for_status

#write data to json for analysis
with open("stock_data.json", "w") as json_file:
     json.dump(stock_response.json(), json_file)

#calculate the date for yesterday and day before yesterday
yesterday = dt.date.today() - dt.timedelta(days = 1)
before_yesterday = dt.date.today() - dt.timedelta(days = 2)

#getting the closing prices for each day we need
yesterday_closing_price = float(stock_response.json()['Time Series (Daily)'][str(yesterday)]["4. close"])
before_yesterday_closing_price = float(stock_response.json()['Time Series (Daily)'][str(before_yesterday)]["4. close"])

#calculate the price difference between the days as percentage, up to the 2 decimals
price_diff = round(((yesterday_closing_price/before_yesterday_closing_price)*100),2)

## STEP 2: Use https://newsapi.org get the first 3 news pieces for the COMPANY_NAME
# if the price difference is higher than 4.

news_parameters = {
    'apiKey': os.environ["API_NEWS"],
    "q": (COMPANY_NAME, STOCK)
}

news_response = requests.get("https://newsapi.org/v2/top-headlines", params=news_parameters)
news_response.raise_for_status

with open("news_data.json", "w") as json_file:
     json.dump(news_response.json(), json_file)

top_news = news_response.json()["articles"][:3]

if abs(100-price_diff) >=4:
    for news in top_news:
        title = news["title"]
        source_name = news["source"]["name"]
        print(f"{source_name}: {title}")


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

