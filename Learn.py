from Utility.NSEIndia import NSEAPI as nseIndia
from datetime import datetime, timedelta

nse = nseIndia.NSEAPI()
#company_info = nse.get_symbols_list()

end_date = datetime.now()

start_date = (datetime.now()- timedelta(days=65))

symbol = "SBIN"
series = "EQ"

price = nse.get_price(start_date, end_date, symbol)

print(price)
