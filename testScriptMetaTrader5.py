from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import MetaTrader5 as mt5

path = r'c:\users\sophi\appdata\local\programs\python\python38\lib\site-packages'

# connect to MetaTrader 5
if not mt5.initialize(login=5461363, server="ActivTrades-Server", password="JAGMqzjh"):
    print("initialize() failed, error code =", mt5.last_error())
    quit()
 
 
# print(mt5.terminal_info())
# print(mt5.version())

symbol = "UsaTecDec20"
symbol_info = mt5.symbol_info(symbol)


if not symbol_info.visible:
    print(symbol, "is not visible, trying to switch on")
    if not mt5.symbol_select(symbol,True):
        print("symbol_select({}}) failed, exit",symbol)
        mt5.shutdown()
        quit()

lot = 0.1
point = mt5.symbol_info(symbol).point
price = mt5.symbol_info_tick(symbol).ask
deviation = 20
request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_BUY,
    "price": price,
    "sl": price - 100 * point,
    "tp": price + 100 * point,
    "deviation": deviation,
    "magic": 234000,
    "comment": "python script open",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_RETURN,
}


result = mt5.order_send(request)

# request 1000 ticks from EURAUD
UsaTec_ticks = mt5.copy_ticks_from(symbol, datetime(2020,1,28,13), 1000, mt5.COPY_TICKS_ALL)
 
# get bars from different symbols in a number of ways
UsaTec_rates = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M1, datetime(2020,1,28,13), 1000)

lot = 0.1
point = mt5.symbol_info(symbol).point
price = mt5.symbol_info_tick(symbol).ask
deviation = 20

request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_BUY,
    "price": price,
    "sl": price - 100 * point,
    "tp": price + 100 * point,
    "deviation": deviation,
    "magic": 234000,
    "comment": "python script open",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_RETURN,
}

# shut down connection to MetaTrader 5
mt5.order_send(request)
print("1. order_send(): by {} {} lots at {} with deviation= {} points".format(symbol,lot,price,deviation));
if result.retcode != mt5.TRADE_RETCODE_DONE:
    print("2. order_send failed, retcode={}".format(result.retcode))
    # request the result as a dictionary and display it element by element
    result_dict=result._asdict()
    for field in result_dict.keys():
        print("   {}={}".format(field,result_dict[field]))
        # if this is a trading request structure, display it element by element as well
        if field=="request":
            traderequest_dict=result_dict[field]._asdict()
            for tradereq_filed in traderequest_dict:
                print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
    mt5.shutdown()
 
#DATA
print('UsaTec_ticks(', len(UsaTec_ticks), ')')
for val in UsaTec_ticks[:10]: print(val)

#PLOT
# create DataFrame out of the obtained data
ticks_frame = pd.DataFrame(UsaTec_ticks)
# convert time in seconds into the datetime format
ticks_frame['time']=pd.to_datetime(ticks_frame['time'], unit='s')
# display ticks on the chart
plt.plot(ticks_frame['time'], ticks_frame['ask'], 'r-', label='ask')
plt.plot(ticks_frame['time'], ticks_frame['bid'], 'b-', label='bid')
 
# display the legends
plt.legend(loc='upper left')
 
# add the header
plt.title('UsaTe ticks')
 
# display the chart
plt.show()
