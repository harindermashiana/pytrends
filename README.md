# pytrends
Code to get hourly, daily and weekly pytrends data

# Approach
We need to understand that pytrends provides data that is normalized on a scale of 0 - 100. This normalization also depends on the timeframe for which the data is requested, which means that for the same keyword, it can have different values based on the timeframe requested. 
Also, pytrends returns hourly, daily, weekly and monthly data based on how wide the requested time frame. For example, in order to get hourly data, it must be within a 7 day interval, for weekly it must be within 270 days(9months) and for monthly it must be within 5 years.
Based on the starting data, the data is requested from 2015-01-01 till today and we might have to request data multiple times to get hourly, daily and weekly data because the gap between starting date and current date is larger than the timeframe width allowed for this kind of data.

This means that we might have renormalize the data if requested multiple times because as described previously the data is already normalized based on the timeframe by google. In order to do this we can do it in two ways:

1. We can normalize data for a smaller time interval like weekly based on the values of the larger time interval like monthly. For example like [here](https://github.com/GeneralMills/pytrends/blob/master/pytrends/dailydata.py)
2. We can normalize data based on the overlapping period between the two timeframes requested.

We chose the second approach because it is more accurate based on [this](https://towardsdatascience.com/reconstruct-google-trends-daily-data-for-extended-period-75b6ca1d3420)

It took me around 4-5 hours to do everything.

# How to run

run requirements.txt to ensure all the requirements are satisfied.

You can provide hourly, daily and weekly argument based on the requirement and a file called bitcoin_hourly.csv etc. will contain the final result based on the keyword provided. 
```
python trends.py weekly
```


