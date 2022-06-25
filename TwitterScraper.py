import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime as dt
from datetime import timedelta
from termcolor import colored
import pickle
import matplotlib.pyplot as plt
import cryptocompare


money=10000
filename="tweets"
amount_per_round=100
keywords=["bitcoin", "btc"]
# taker_fee=0.0007500
# maker_fee=0.0007500
taker_fee=0
maker_fee=0


gainc=0
lossc=0


def get_hourly_prices(date, n):
    dt1=cryptocompare.get_historical_price_hour('BTC', 'USD', limit=n+5, exchange='CCCAGG', toTs=date+dt.timedelta(hours=n))

    data = pd.DataFrame.from_dict(dt1)
    data['date'] = pd.to_datetime(data['time'], unit='s')
    data=data.set_index(['date'])
    return data


def remove_tagged(text):
    parts = text.split()
    newtext=[]
    for part in parts:
        if "@" not in part:
            newtext.append(part)
    return " ".join(newtext)



def download_tweets(user, n):
    print('Starting download of', n, 'tweets from @'+user)
    progress=0
    data=[]
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:'+user).get_items()):
        if i>n-1: break
        data.append([tweet.date, tweet.id, tweet.content, tweet.user.username])

        if round((i/n)*100)>progress:
            progress=round((i/n)*100)
            print(progress, '%')

    with open(filename, 'wb') as fp:
        pickle.dump(data, fp)
    print('Done!')


def read_tweets():
    with open (filename, 'rb') as fp:
         return pickle.load(fp)[::-1]


def shouldbuy(tweet):
    buy=False
    tweet[2]=remove_tagged(tweet[2]).lower()
    for word in keywords:
        if word in tweet[2]: buy=True
    return buy


def col(a):
    if a==0: return 'grey'
    elif a>0: return 'green'
    else: return 'red'


def buy(date, money, x, method='fixedtime', x2=2):
    money=money*(1-maker_fee)
    initial_prices=get_hourly_prices(date, 20)
    initial_price_index=initial_prices.index.get_loc(date, method='nearest')
    initial_price=initial_prices['close'].iloc[initial_price_index]
    initial_price_date=initial_prices.index.values[initial_price_index]

    amount_bought=money/initial_price

    print('\nBought '+str(round(amount_bought,3))+' BTC for '+str(money)+'$ on '+pd.to_datetime(initial_price_date).strftime("%d/%m/%Y, %H:%M:%S"))



    # Sell after x% loss from max or %up from buying
    sold, rounds, max, selling_price, selling_time, selling_date = False, 0, initial_price, 0, 0, initial_price_date

    if method in ['percentdown', 'percentup', 'percentupdown']:

        while sold==False:
            prices = get_hourly_prices(date + dt.timedelta(hours=rounds+initial_price_index), amount_per_round)
            rounds+=amount_per_round
            for i in range(amount_per_round):
                price=prices['close'].iloc[i]
                selling_time+=1

                if method=='percentdown':
                    sell=price<=(1-(x/100))*max
                elif method=='percentup':
                    sell=price>=(1+(x/100))*initial_price or i==amount_per_round-1
                elif method=='percentupdown':
                    sell=price>=(1+(x/100))*initial_price or price<=(1-(x2/100))*max

                if sell:
                    sold=True
                    selling_price=price
                    selling_date=prices.index.values[i]
                    break
                elif price>max: max=price

        selling_sum=(amount_bought*selling_price)*(1-maker_fee)

        print('Selling when price down more than '+str(x)+'% from max.')
        print('Reached max price of '+str(round(max,2))+' ('+str(round((max/initial_price)*100, 2))+'% of buying price).')
        print('Sold at '+str(round(selling_price, 2))+' ('+str(round((selling_price/initial_price)*100, 2))+'% of buying price) after '+str(selling_time)+' hours, on '+pd.to_datetime(selling_date).strftime("%d/%m/%Y, %H:%M:%S")+'.')
        print(colored('Gain: '+str(selling_sum-money), col(selling_sum-money)))


    # Sell after x hours
    if method=='fixedtime':
        prices = get_hourly_prices(date + dt.timedelta(hours=initial_price_index+x), 1)
        selling_price=prices["close"].iloc[0]
        selling_date=prices.index.values[0]
        selling_sum=(amount_bought*selling_price)*(1-maker_fee)

        print('Sold at '+str(round(selling_price, 2))+' ('+str(round((selling_price/initial_price)*100, 2))+'% of buying price) after '+str(x)+' hours, on '+pd.to_datetime(selling_date).strftime("%d/%m/%Y, %H:%M:%S")+'.')
        print(colored('Gain: '+str(selling_sum-money), col(selling_sum-money)))





    return selling_sum






tweets_list1=read_tweets()
hourly_evolution=[]

for tweet in tweets_list1:
    if shouldbuy(tweet):


        print('\n\nFound tweet from', tweet[0])
        print('Text:', tweet[2])

        prev=money
        money=buy(tweet[0]+dt.timedelta(hours=1), money, 2, 'percentdown')
        if money>prev: gainc+=1
        else: lossc+=1

        # next_hours = get_hourly_prices(tweet[0], 100)
        # next_hours['close'] = next_hours['close'].map(lambda a: a / next_hours['close'].iloc[0])
        # hourly_evolution.append(next_hours['close'])


print('Final amount:', money, '$')
print('Winning trades:', gainc)
print('Losing trades:', lossc)

# sums_per_hour=[1]*100
# for series in hourly_evolution:
#     plt.plot(series)
#     for i in range(100):
#         sums_per_hour[i]+=series.iloc[i]-1
#
# plt.plot(sums_per_hour)
# plt.show()



















