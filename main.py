import requests
import json
import datetime as dt

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

api_alphavantage = "1RW6YMYHZGZWPW62"

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": api_alphavantage
}

response = requests.get('https://www.alphavantage.co/query', params=parameters)
response.raise_for_status

# with open("data.json", "w") as json_file:
#     json.dump(response.json(), json_file)

yesterday = dt.date.today() - dt.timedelta(days = 1)
before_yesterday =dt.date.today() - dt.timedelta(days = 2)

yesterday_closing_price = float(response.json()['Time Series (Daily)'][str(yesterday)]["4. close"])
before_yesterday_closing_price = float(response.json()['Time Series (Daily)'][str(before_yesterday)]["4. close"])

increase = round(((yesterday_closing_price/before_yesterday_closing_price)*100),2)
print(increase)

if abs(100-increase) >=4:
    print("Print News")

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.



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

