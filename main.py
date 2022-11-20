

import BinanceClient
import datetime
import time
import numpy as np
import logging
import httpx
def logg(msg):
    # basic logging 
    logging.basicConfig(level=logging.INFO, filename="output.log", format='%(asctime)s %(message)s') # include timestamp
    logging.info(msg)


DATASIZE = 10
TIMEFRAME = 3 #15min

CH3_2_200 = -1001871978999
CH3_2_100 = -1001663202161
CH3_2_50 = -1001778894869
CH3_5_50 = -1001826966465
CH3_5_100 = -1001884354061
CH3_5_200 = -1001608393477
CH3_10_50 = -1001868265527
CH3_10_100 = -1001897906322
CH3_10_200 = -1001625854593
CH15_2_50 = -1001810084713
CH15_2_100 = -1001850449145
CH15_2_200 = -1001848064130

#CHANNEL:1
CH15_5_50 = -1001588512131


CH15_5_100 = -1001557080577
CH15_5_200 = -1001820263196
CH15_10_50 = -1001589191495
CH15_10_100 = -1001877398816
CH15_10_200 = -1001809890013
CH60_2_50 = -1001438184580
CH60_2_100 = -1001722467003
CH60_2_200 = -1001664761082

#CHANNE:2
CH60_5_50 = -1001502951580

CH60_5_100 = -1001883990428
CH60_5_200 = -1001718297642
CH60_10_50 = -1001794592023
CH60_10_100 = -1001877974586
CH60_10_200 = -1001620928540

CHANNEL = CH60_5_50

URL = 'https://api.telegram.org/bot5417356609:AAGfuePUntAH1_Zwdf0h3V7OHrbTOAdSkEc/sendMessage?chat_id={}&text={}&parse_mode=markdown'


trading = False
trades = []

successful_trades = 0
failed_trades = 0

RETRACEMENT = 0.33
MARGIN_RATIO = 0.33
LEVERAGE = 1
MIN_PROFITS = 1.003 #0.3% profits


coins_list = []
API_KEY = "WnfYqPmGnnRYVkZKMkmSGC6v3w7NfQI36qbn8QcKV79s6tS0eMryWvr8c62gO7iT"
API_SECRET = "s9b6YNprpqlTjdLjm6Jv7bCWN0WMiy23cW38sYecbYiuovbZIUmYnt56wtNGjgzX"


current_time = datetime.datetime.now()
day = current_time.day
print("today is {}".format(current_time))
bc = BinanceClient.BinanceClient(API_KEY, API_SECRET)
client = bc.get_client()
intervals = [client.KLINE_INTERVAL_1MINUTE, client.KLINE_INTERVAL_3MINUTE, client.KLINE_INTERVAL_5MINUTE, client.KLINE_INTERVAL_15MINUTE, client.KLINE_INTERVAL_30MINUTE, client.KLINE_INTERVAL_1HOUR, client.KLINE_INTERVAL_2HOUR, client.KLINE_INTERVAL_4HOUR, client.KLINE_INTERVAL_6HOUR, client.KLINE_INTERVAL_8HOUR, client.KLINE_INTERVAL_12HOUR, client.KLINE_INTERVAL_1DAY, client.KLINE_INTERVAL_3DAY, client.KLINE_INTERVAL_1WEEK, client.KLINE_INTERVAL_1MONTH]
intervals_min = [1, 3, 5, 15, 30, 60, 120, 240, 360, 480, 720, 1440, 4320, 10080, 43200]

top_score = 0

LAST_OPEN = 0

pairs = bc.getPairs(ASSET_BASE=True)
client = bc.get_client()

#futures = bc.getFutures(ASSET_BASE=True)
#print(futures)
#print(len(futures))

#print(bc.get_futures_account_usdt())

msg_ctr = 0

max_ = len(pairs)
i = 0
DATA = []
sorted_coins = []


MIN_MC = 75000000 #75M
MAX_MC = 3000000000 #3B

#coin = 'ETH'
#coin = input("Enter coin:")
#coins = ['BTC', 'ETH', 'BNB', 'NEO', 'LTC', 'QTUM', 'ADA', 'XRP', 'EOS', 'IOTA', 'XLM', 'ONT', 'TRX', 'ETC', 'ICX', 'NULS', 'VET', 'LINK', 'WAVES', 'ONG', 'HOT', 'ZIL', 'ZRX', 'FET', 'BAT', 'XMR', 'ZEC', 'IOST', 'CELR', 'DASH', 'OMG', 'THETA', 'ENJ', 'MITH', 'MATIC', 'ATOM', 'TFUEL', 'ONE', 'FTM', 'ALGO', 'GTO', 'DOGE', 'DUSK', 'ANKR', 'WIN', 'COS', 'MTL', 'TOMO']
#coins = [coin]
#coins = coins[5:15]
'''
f = open('coins.txt', 'r')
data = f.read()
coins = data.split(',')
coins = coins[:-20]
'''
#no.send_message("Bot started (v1.2)")
            
def test_trade():
    global trading
    blc = bc.getAssetBalance('USDT')
    print("You currently have {} USDT in your account".format(blc))
    total = 0
    for info in coins_list:
        amount = float(info[1])
        total += amount
    print("Total investment: {} USDT".format(total))
    if total > blc:
        print("You currently don't have enough USDT to start your bot, add more USDT or reduce your investment size to get started")
        trading = False

coins = pairs

def get_bear_coins():
    futures = bc.getFutures(ASSET_BASE=True)
    coins = futures
    final_list = []
    for coin in coins:
        try:
            df = bc.getHistoricalData(coin, intervals[11], intervals_min[11], datapoints=220)

            High = np.array(df.High)
            Low = np.array(df.Low)
            Close = np.array(df.Close)
            Open = np.array(df.Open)
            MA200 = np.array(df.MA200)
            MA50 = np.array(df.MA50)
            Upper = np.array(df.Upper)

            if MA50[-1] < MA200[-1]:
                final_list.append(coin)
        except Exception as e:
            pass
            #print(e)
            #print("coin failed..")
    return final_list

#fl = get_bear_coins()
#print("Bear coins:")
#print(fl)  
#print(len(fl))

#print("{}% of the futures coins are bearish".format(100*len(fl)/len(futures)))

acc_balance = float(bc.get_futures_account_usdt())
#bc.enter_short(asset="QNT", leverage=1, pctg=0.2)
#bc.exit_short(asset="SFP", qty=19)

#to calculate liquidation price: 1/pctg + 1
in_trade = False
initial_time = time.time()

while trading:
    in_trade = False
    status, error = bc.get_connection_status()
    if status == False:
        while status == False:
            print("Connection failed to establish...reseting the connection")
            print(error)
            print("current time: {}".format(datetime.datetime.now()))
            time.sleep(20)
            status, error = bc.get_connection_status()
        bc.deleteClient()
        del bc
        bc = BinanceClient.BinanceClient(API_KEY, API_SECRET)

    msg_ctr += 1
    string_array = []
    cc_copy = []
    print(datetime.datetime.now())
    #refresh the list every 24h
    if time.time() - initial_time > 60*60*24:
        print("refreshing the list")
        httpx.get(URL.format(CHANNEL, "refreshing the list"))
        fl = get_bear_coins()
        initial_time = time.time()
    t1 = time.time()
    for coin in fl:
        t2 = time.time()
        _coin = coin
        if str(coin).startswith('1000'):
            _coin = coin[4:]
        try:
            df = bc.getHistoricalData(_coin, intervals[TIMEFRAME], intervals_min[TIMEFRAME], datapoints=DATASIZE)

            High = np.array(df.High)
            Low = np.array(df.Low)
            Close = np.array(df.Close)
            Open = np.array(df.Open)
            Volume = np.array(df.Volume)
            mean_vol = Volume.mean()

            high = High[-1]
            close_ = Close[-1]
            open_ = Open[-1]

            entry = close_

            diff_ =  close_ / open_
            if mean_vol == 0:
                vdiff_ = 0
            else:
                vdiff_ = Volume[-1]/mean_vol
            
            if diff_ > 1.002 and vdiff_ > 1.005 :
                message = "Signal for {}. Current price is {}$. Price increase of {}% and volume increase of {}% so far.".format(coin, close_, 100*(diff_-1), 100*(vdiff_-1))
                print(message)
                httpx.get(URL.format(CH3_2_50, message))
            '''
            '''
            if diff_ > 1.05:
                _df = bc.getHistoricalData(_coin, intervals[11], intervals_min[11], datapoints=220)
                _Close = np.array(_df.Close)
                _High = np.array(df.High)
                _Low = np.array(df.Low)
                _Close = np.array(df.Close)
                _Open = np.array(df.Open)
                _Upper = np.array(_df.Upper)
                if _Close[-1] > _Upper[-1]:
                    message = "Signal for {}. Current price is {}$. Price increase of {}% and volume increase of {}% so far.".format(coin, close_, 100*(diff_-1), 100*(vdiff_-1))
                    message += "\n Coin is unusually high, this is a good sign for an entry"
                    print(message)
                    httpx.get(URL.format(CHANNEL, message))
                    #calculate a suggested exit price
                    mean_open = _Open[-10:-1].mean()
                    mean_close = _Close[-10: -1].mean()
                    mean_price =  (mean_open + mean_close)/2

                    price_diff = entry - mean_price
                    close_trade = entry - RETRACEMENT*price_diff

                    expected_profits = (LEVERAGE * (entry/close_trade-1)) + 1
                    print("Expected Profits: {}".format(expected_profits))
                    if expected_profits > MIN_PROFITS:
                        print("Entering short trade..")
                        acc_balance = float(bc.get_futures_account_usdt())
                        print("Account balance: {}".format(acc_balance))
                        httpx.get(URL.format(CHANNEL, "Entering short trade.."))
                        httpx.get(URL.format(CHANNEL, "Account balance: {}".format(acc_balance)))
                        message = "Price is {}$ above it's normal value. 10% retracement: {}$ 25% retracement: {}$ 33% retracement: {}$ 50% retracement: {}$".format(price_diff, entry - 0.1*price_diff, entry - 0.25*price_diff, entry - 0.33*price_diff, entry - 0.5*price_diff)
                        httpx.get(URL.format(CHANNEL, message))
                        in_trade = True
                        trade_qty = bc.enter_short(asset=_coin, leverage=LEVERAGE, pctg=MARGIN_RATIO)
                        while in_trade:
                            time.sleep(1)
                            asset_price = bc.getPrice(_coin)
                            print("date: {} price: {}".format(datetime.datetime.now(), asset_price))
                            if asset_price < close_trade:
                                bc.exit_short(asset=_coin, qty=trade_qty)
                                in_trade = False
                                httpx.get(URL.format(CHANNEL, "Exiting short trade.."))
                                acc_balance = float(bc.get_futures_account_usdt())
                                print("Account balance: {}".format(acc_balance))
                                httpx.get(URL.format(CHANNEL, "Account balance: {}".format(acc_balance)))            
                else:
                    pass
                    #message = "Coin isnt at a particularly high point, trade should be avoided!"
                    #httpx.get(URL.format(CHANNEL, message))
        except Exception as e:
            print("error")
            print(e)
        print("time taken: {}s".format(time.time() - t2))
    print("finished looping in {}s".format(time.time() - t1))
    

