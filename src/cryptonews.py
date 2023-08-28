import os, json, time
from datetime import datetime
from datetime import date
from datetime import timedelta
from dotenv import load_dotenv
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import pandas as pd
import utils as u

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


load_dotenv('../config_files/.env')


def get_cryptonews(ticker, sd, ed):
    """Retrieves all news related to the ticker in CSV format.
    You must have an environ variable containing the token.

    Args:
        ticker (str): crypto ticker
    """

    from_date = sd
    TOKEN = os.getenv('CRYPTONEWS_API_TOKEN')
    days =  ed - sd
    session = requests.Session()
    retry = Retry(connect=10, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    while True:

        data = sd.strftime('%m%d%Y')
        
        url = \
            f"""
            https://cryptonews-api.com/api/v1?tickers={ticker}&sortby=rank&extra-fields=id,eventid,rankscore&items=100&page=1&date={data}-{data}&token={TOKEN}
            """
        
        api_return = session.get(url).text
        pydict = json.loads(api_return)
        # Request Error Handling
        # if the request is not sucessful, 3 extra attempts will be made with pauses
        # tries = 5
        # while tries>=0:
        #     try:
        #         pydict = json.loads(api_return)
        #         break
        #     except requests.exceptions.ConnectionError:
        #         r.status_code = "Connection refused"
        #         if tries == 0:
        #             # Quits and saves data as json file
        #             with open('cryptonews.json', 'w', encoding='utf-8') as f:
        #                 json.dump(x, f, ensure_ascii=False, indent=4)
        #             raise
        #         else:
        #             time.sleep(4)
        #             tries -= 1
        #             continue
            

        try:
            # print(f"Loading 100 top news at {dt}...")
            pass
        except:
            break
        
        if 'message' not in pydict and ed>=sd:        
            try:
                x['data'].extend(pydict['data'])
            except:
                x = pydict
            
            sd = sd + timedelta(days=1)

        else:

            with open(f"../data/raw_cryptonews_{ticker}_from_{from_date.strftime('%Y%m%d')}_to_{ed.strftime('%Y%m%d')}.json", 'w', encoding='utf-8') as f:
                json.dump(x, f, ensure_ascii=False, indent=4)

            with open(f"../data/raw_cryptonews_{ticker}_from_{from_date.strftime('%Y%m%d')}_to_{ed.strftime('%Y%m%d')}.json", 'r') as f:
                dict_data = json.load(f)
            df_raw_crypto_news = pd.DataFrame(dict_data ['data'])
            
            df_formatted_crypto_news = u.create_utc_date_column(df_raw_crypto_news)

            df_formatted_crypto_news.to_csv(f"../data/formatted_cryptonews_{ticker}_from_{from_date.strftime('%Y%m%d')}_to_{ed.strftime('%Y%m%d')}.csv", index=False)

            break

    return print("Done")


# if __name__ == '__main__':
#     get_cryptonews('BTC', date(2021,1,1))