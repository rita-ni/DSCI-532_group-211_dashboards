## Motivation and Purpose

Stock prices can be easily influenced by the overall economic environment and are sensitive to financial crisis. Therefore, it may be better to hold a stock in the long run to capture more capital gains. More and more people nowadays are interested in stock markets, but few people are aware of the risks in stock markets nor the value of long-term investment. To address this issue, we propose building a data visualization app that uses historical stock price data to show stock price fluctuations and long-term investment gains or losses. Our app will show the monthly price fluctuations, monthly percentage changes in stock prices, investment value fluctuations, and long-term investment returns. 

## Description of the data

The dataset we are using is the  `Stocks`  data from the `vega-datasets`. The dataset has 560 observations in total. The original dataset has 3 columns: `symbol`, `date`, and `price`.  
    
`symbol` lists out the stock ticker symbol for the companies included in the dataset. There are 5 companies in total, and they are Microsoft, Amazon, IBM, Google, and Apple. For visualization and readability purposes, we renamed the column to `company` and replaced the stock ticker symbol with actual company names.     
     
The `date` column lists out the date when the stock price was recorded. The value of the `date` column ranges from January 1, 2000 to March 1, 2010. The date range is the same for Microsoft, Amazon, IBM, and Apple. Each of them has 123 observations in the dataset. Since  Google held its IPO in August, 2004, the record for Google started from August 1, 2004. Therefore, there are 68 observations for Google.     
     
The `price` column lists out the price of that stock on the recorded `date`.    
    
We then created a number of new columns to facilitate our analysis. For plotting and grouping benefits, we created the `year` column, which extracted the year from the `date` column.     
   
We created the `monthly_return` column, which is the monthly percentage changes in stock prices compare to the previous month.      
     
In order to calculate the investment value and investment return of each stock, we created `shares` and `inv_value` columns. We assume that the investor started with an initial investment of $10,000 in January 1, 2000. The `shares` column is calculated as $10,000 divided by the price at January 1, 2000. For Google it is $10,000 divided by the price at August 1, 2004.      

The `inv_value` column was calculated by `price` * `shares`.   
<p style="text-align:center;"><img src="https://latex.codecogs.com/svg.latex?\inline&space;\large&space;inv\_value=price&space;*&space;shares" title="\large inv\_value=price * shares" />
   
To calculate the investment return at each period, we created another column called `investment_return`, which was `inv_value` divided by 10,000 then minus 1:

<a href="https://www.codecogs.com/eqnedit.php?latex=\inline&space;\large&space;investment\_return&space;=&space;\frac{inv\_value}{10000}&space;-&space;1." target="_blank"><img src="https://latex.codecogs.com/svg.latex?\inline&space;\large&space;investment\_return&space;=&space;\frac{inv\_value}{10000}&space;-&space;1." title="\large investment\_return = \frac{inv\_value}{10000} - 1." /></a>

## Research questions and usage scenarios

*Note: in the usage scenarios, tasks are emphasized using [ ], e.g. [explore]*

Ted is a layman in financial markets. He just becomes interested in the stock markets and he wants to [explore] how stock prices changed in the past. He is interested in the tech industry, especially these five companies: Microsoft, Amazon, IBM, Google, and Apple. He wants to [explore] their price fluctuations and monthly price changes. His first question is:

#### Research Question 1: How did stock prices change between 2000 and 2010? Did the 2008 financial crisis has any impact on stock prices?

To answer this question, he wants to [explore] price fluctuations for the abovementioned five stocks and their monthly price changes. He wants to be able to [compare] the price changes of different stocks, and [identify] when there was the greatest price volatility. 

When Ted logs on to the “Stocks Price and Return” app, on the first tab, on the left, he sees the plot of monthly stock prices from January 2000 to March 2010 of the five stocks. On the right, there is another plot depicts the monthly percentage changes in stock prices. There is a drop-down menu for him to select the stocks. When Ted selects one stock in the left plot, the plot on the right will automatically change by displaying only that stock and shading other stocks. He can also select different stocks and compare them. When doing so, Ted may find out that during the 2008 financial crisis, the price fluctuations were the most. Then he can take a closer look at the monthly stock price percentage changes plot to further examine how the financial crisis affected stock prices. Ted may find out that the stock prices dropped significantly during the financial crisis.      

Then, Ted wants to know more about the investment return. His second question is:     

#### Research Question 2: What is the investment return for each of these five stocks?

Ted wants to be able to [explore] the hypothetical investment value over the 10-year range, [compare] the hypothetical investment returns of different stocks, and [identify] which stock gives the highest return.    
    
On the second tab, Ted can take a look at the hypothetical investment value of the five stocks from January 2000 to March 2010 (August 2004 to Mach 2010 for Google). He can zoom in or zoom out to select the time period to take a closer look at the hypothetical investment value at that time. In another graph, Ted can select different end year from a slide bar to check out the overall investment return for each stock during selected time range. By doing so, Ted may find out that Apple will give him the highest return and it may be best for him to hold the stock from the beginning till the end.    
    
This app may give Ted some basic ideas of how stock prices fluctuate and how long-term investment can help him get through financial crisis. Next, Ted decides to talk to a financial advisor to explore his investment plans, since he believes now he understands the stock market better. 
