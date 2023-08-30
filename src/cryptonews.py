import os
import json
import time
from datetime import datetime
from datetime import date
from datetime import timedelta
from dotenv import load_dotenv, find_dotenv
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd
import utils as u
import os

load_dotenv(find_dotenv('../config_files/.env'))


def get_cryptonews(ticker, sd, ed):
    """Fetches News data from Crypto News API between the chosen dates. An API TOKEN is required!

    Args:
        ticker (string): Crypto Coin ticker
        sd (datetime): Starting Date
        ed (datetime): End Date

    Returns:
        _type_: _description_
    """

    # an .env with the crypto news token is required
    TOKEN = os.getenv('CRYPTONEWS_API_TOKEN')
    
    # Session config (necessary in case the first request attempt fails)
    session = requests.Session()
    retry = Retry(connect=10, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    print(os.getcwd())
    curr_date = sd  # current date
    end_date = sd  # end date
    while True:  # date loop

        data = curr_date.strftime('%m%d%Y')
        
        pg = 1
        while True:  # repeats until last page is reached
            data_ = curr_date.strftime('%d/%m/%Y')
            print(f"Fetching page {pg} for {data_}")
            url = \
                f"""
                https://cryptonews-api.com/api/v1?tickers={ticker}&sortby=rank&extra-fields=id,eventid,rankscore&items=100&page={pg}&date={data}-{data}&token={TOKEN}
                """
            print(url)
            api_return = session.get(url).text
            pydict = json.loads(api_return)

            # there is a message when the URL returned an error and data otherwise.
            if 'message' not in pydict and 'error' not in pydict:
                try:
                    # if x was already assembled
                    dict_data['data'].extend(pydict['data'])
                except:
                    dict_data = pydict  # creating the data cumulative dict

                pg += 1  # moving on to the next page

            # If there is an error we assume the amount of news in that day ended (= reached last page)
            else:
                # moving on to the next day!
                curr_date = curr_date + timedelta(days=1)
                break

        if curr_date > end_date:
            break

    # Creating JSON file:
    with open(f"../data/raw_cryptonews_{ticker}_from_{sd.strftime('%Y%m%d')}_to_{ed.strftime('%Y%m%d')}.json", 'w') as f:
        json.dump(dict_data, f, ensure_ascii=False)

    # Creating CSV file with UTC date adjustments:

    df_raw_crypto_news = pd.DataFrame(dict_data['data'])

    df_formatted_crypto_news = u.create_utc_date_column(
        df_raw_crypto_news)  # from utils.py

    df_formatted_crypto_news.to_csv(
        f"../data/formatted_cryptonews_{ticker}_from_{sd.strftime('%Y%m%d')}_to_{ed.strftime('%Y%m%d')}.csv", index=False)


    return print("Done")

# get_cryptonews('BTC',  date(2023, 8, 16), date(2023, 8, 18))
