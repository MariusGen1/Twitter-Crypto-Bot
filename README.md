# Twitter Crypto Bot (project in progress)

A crypto trading bot built in Python that trades based on Twitter events (as of now, Elon Musk's tweets). Utilizes Binance API to fetch prices and buy/sell.
Will soon be running live, all stats will be available at http://192.168.68.83:80 (updated in realtime, running on a Raspberry Pi).


## Idea
Originally based on the idea that Tweets from certain influential people can heavily affect crypto-currency value short-term. Thus using a bot to buy instantly and sell at the optimal time would allow to make significant gains while investing over short periods of time.
Articles that illustrate the fundamental idea: 
 - https://www.coindesk.com/layer2/culture-week/2021/12/14/the-elon-effect-how-musks-tweets-move-crypto-markets/
 - https://www.vox.com/recode/2021/5/18/22441831/elon-musk-bitcoin-dogecoin-crypto-prices-tesla


## Preliminary Research
Using historical data from cryptocompare.com, the principle can be tested against numerous situations like this.
Evolution of Bitcoin (BTC) price 100 hours from each tweet from Elon Musk containing 'Bitcoin' or 'BTC' (not case-sensitive) since November 2017. Lines show (price after x hours)/(initial price). Grey line represents the sum of the others.


## Buying algorithm
The algorithm purchases Bitcoin every time Elon Musk posts a tweet containing one of the keywords:
- 'Bitcoin', 'BTC' (not case-sensitive)


## Selling algorithm
Four selling methods have been implemented in the project:
 - Fixed time ('fixedtime'): sells after a fixed duration in hours 
 - Percent down ('percentdown'): sells when price reaches a set percentage less than max price reached since buying. PRO: allows for large gains if the price were to augment continuously, while limiting potential losses
 - Percent up ('percentup'): sells when price reaches a set percentage more than buying price. 
 - Percent up/down ('percentupdown'): combines percent up and percent down methods.

By testing each of the methods against historical data, their effectiveness can be assessed. This table shows the final money after using each of the methods since November 2017 with a starting capital of 10 000$ and ignoring trading fees as they would not affect how the performance of each method compares.




## Performance
The bot will be launched and given a starting capital of 100$. From there on it will be left running continuously for an indefinite duration. 
Live statistics will be publicly available at http://192.168.68.83:80 


## Potential Improvements
- Add AI sentiment analysis (to determine wether the tweet is positive or negative)
- Add investment options for other currencies such as Ethereum or Dogecoin
- Use tweets from other influential users as well to improve accuracy
- Get data from other sources as well such as newspapers
