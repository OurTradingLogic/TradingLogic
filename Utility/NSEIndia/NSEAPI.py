#https://github.com/pratik141/nsedt/blob/29-dates-not-working-well-on-index-data/nsedt/resources/constants.py
#https://github.com/swapniljariwala/nsepy/blob/master/nsepy/live.py
#https://github.com/aeron7/nsepython/blob/master/nsepython/rahu.py
from collections import defaultdict
from datetime import datetime, timedelta
from Utility import NSEIndia
from Utility.NSEIndia import Constant as cns
import concurrent
import logging
import urllib
from concurrent.futures import ALL_COMPLETED
import pandas as pd
from Utility.NSEIndia import CustomFormat

#logger = logging.getLogger(__name__)

class NSEAPI:  
    def __amdentMarketSuffix(self, stocklist):
        tickersresult = []
        for stock in stocklist:
            if stock['exchange'] == 'NSE':
                tickersresult.append(stock['tradingsymbol'] + ".NS") 
            elif stock['exchange'] == 'BSE':
                tickersresult.append(stock['tradingsymbol'] + ".BO") 

        return tickersresult 
    
    def get_companyinfo(self,
        symbol,
        response_type="panda_df",
    ):
        """
        Args:
            symbol (str): stock symbol.
            response_type (str, Optional): define the response type panda_df | json. Default panda_df

        Returns:
            Pandas DataFrame: df containing company info
        or
            Json: json containing company info

        """
        params = {}
        cookies = NSEIndia.get_cookies()
        base_url = cns.BASE_URL
        event_api = cns.EQUITY_INFO

        params["symbol"] = symbol

        url = base_url + event_api + urllib.parse.urlencode(params)
        data = NSEIndia.fetch_url(
            url,
            cookies,
            key=None,
            response_type=response_type,
        )

        return data

    def get_symbols_list(self):
        """
        Args:
            No arguments needed

        Returns:
            List of stock or equity symbols

        """
        cookies = NSEIndia.get_cookies()
        base_url = cns.BASE_URL
        event_api = cns.EQUITY_LIST

        url = base_url + event_api
        data = NSEIndia.fetch_url(url, cookies)
        f_dict = data.to_dict()
        eq_list = []
        for i in range(len(f_dict["data"])):
            eq_list.append(f_dict["data"][i]["metadata"]["symbol"])

        return eq_list
    
    def get_price(self,
        start_date,
        end_date,
        symbol=None,
        input_type="stock",
        series="EQ",
    ):
        """
        Create threads for different requests, parses data, combines them and returns dataframe
        Args:
            start_date (datetime): start date
            end_date (datetime): end date
            input_type (str): Either 'stock' or 'index'
            symbol (str, optional): stock symbol. Defaults to None. TODO: implement for index`
        Returns:
            Pandas DataFrame: df containing data for symbol of provided date range
        """
        cookies = NSEIndia.get_cookies()
        base_url = cns.BASE_URL
        price_api = cns.EQUITY_PRICE_HISTORY
        url_list = []

        # set the window size to one year
        window_size = timedelta(days=cns.WINDOW_SIZE)

        current_window_start = start_date
        while current_window_start < end_date:
            current_window_end = current_window_start + window_size

            # check if the current window extends beyond the end_date
            current_window_end = min(current_window_end, end_date)

            if input_type == "stock":
                params = {
                    "symbol": symbol,
                    "from": current_window_start.strftime("%d-%m-%Y"),
                    "to": current_window_end.strftime("%d-%m-%Y"),
                    "dataType": "priceVolumeDeliverable",
                    "series": series,
                }
                url = base_url + price_api + urllib.parse.urlencode(params)
                url_list.append(url)

            # move the window start to the next day after the current window end
            current_window_start = current_window_end + timedelta(days=1)

        result = pd.DataFrame()
        with concurrent.futures.ThreadPoolExecutor(max_workers=cns.MAX_WORKERS) as executor:
            future_to_url = {
                executor.submit(NSEIndia.fetch_url, url, cookies, "data"): url
                for url in url_list
            }
            concurrent.futures.wait(future_to_url, return_when=ALL_COMPLETED)
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    dataframe = future.result()
                    result = pd.concat([result, dataframe])
                except Exception as exc:
                    logging.error("%s got exception: %s. Please try again later.", url, exc)
                    raise exc
        return CustomFormat.price(result)
