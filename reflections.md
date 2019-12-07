# High level summary of the feedbacks during lab session:
1.	There were some typos in titles and text in the app.
2.	The second chart in Tab 2 needed a title and axis labels.
3.	In Tab 2, there were two scroll bars.
4.  In Tab2, the x-axis for the first plot changes format if the user selects a date window. It might be better to keep the same format.
4.	The slider in Tab 3 was down the graph at the bottom. It was not obvious to users and they tend to miss it.
5.	It might be better to fix the starting point of the slider bar
6.	Users were confused by the result of the chart in Tab 3: why Google has the highest stock price, but Apple has the highest investment value.
7.	There might need a vertical line in the chart in Tab 3.
8.	More colors could be added to make the app more visually appealing.

The feedbacks can be found from the Github issues here:     
[summary of feedbacks](https://github.com/UBC-MDS/DSCI-532_group-211_dashboards/issues/40)     
[feedback 1](https://github.com/UBC-MDS/DSCI-532_group-211_dashboards/issues/37)   
[feedback 2](https://github.com/UBC-MDS/DSCI-532_group-211_dashboards/issues/38)     
[feedback 3](https://github.com/UBC-MDS/DSCI-532_group-211_dashboards/issues/39)    

# High level summary of the changes we made:
1.	We fixed the typos in the app.
2.	We added a title and axis labels for the second chart in Tab 2.
3.	We fixed the “two scroll bars” problem in Tab 2.
4.	We moved the slider bar in Tab 3 to the top of the chart.
5.  We fixed the starting point of the slider bar in Tab 3. Now users can only select different end points on the slider bar.
6.	We added explanations of the investment “mystery”: why Google has the highest stock price, but Apple has the highest investment value.

We chose to take those changes as high priorities and we changed them according to our feedbacks. We believe that these changes can improve the usability of our app and improve user interface. We want to make the app itself as explicit as possible and easy for people to use. These changes help us achieve this goal.

# Features we did not update
1.	Add a vertical line to the chart in Tab 3.     
  We tried to add a vertical line to the chart, but the effect was not satisfying. Because we have some lines that overlap with each other, adding a vertical line to display all the labels at the same time causes distraction. So we decided not to add the vertical line and keep the chart simple but effective. 

2.  Fix the format of the x-axis for the first plot in Tab 2
There are two main reasons why we did not implement this feedback.
    1. The default is to show the whole 10-year time range, it makes sense to show the "year" instead of "month". When you select a specific time range, it makes sense to show more details of the that time range, namely, to show "month" rather than "year".
    2. This also has something to do with how Altair defines the temporal data type. It is the default how Altair represents temporal data on the axis. It is more of a technical issue.

3.	Add a theme to the app to make it more appealing. 

    For the third feature, we did not implement it, partly because of the time constraint, and partly because lacking an appealing theme does not affect the usability of our app.  

# Wishlist of the feature 
If we have infinite time, we would like to:
1. Find a better format to represent the x-axis for the first plot in Tab 2.
2. Make the app more appealing, such as adding themes and colors. 


# Reflection on the feedbacks
## Similarities:
1.	A number of people noticed that there were some typos in the text in our app.
2. The second chart on Tab 2 lacked a title and axis labels, and this made the graph difficult to understand.
3. A number of people liked the fact that we have 3 tabs. Each tab serves only one function. This makes each tab clean and easy to navigate. They also liked the systematic layout of each of our tabs.
4. A number of people liked the fact that we have a brief introduction of our dataset and short explanation in each tab. This helps people understand the functionalities of our app and how to use the app.


## Reflections on the usability of the app:
1. Our app is easy to use and easy to understand. The drop-down window and slider bar are common interaction widgets. They are easy to use and also inspire user interests. When seeing the drop-down window in Tab 2, people immediately understand that there is something they can select. They also know how to use the slider bar to select the time range of interest. These interactions give people the freedom to explore by themselves. This is better than giving them all the information at once. 
2.	The introductions of the dataset and the explanation on each tab helps people understand the purpose and functions of this app. This shows that we cannot assume users to have prior knowledge as us the developers. We need to provide them with sufficient amount of information and guidance to help them learn and understand our app. 
3.	Being a "fly-on-the-wall" gives us a chance to see how users interact with our app in reality. This helps us to view our app from different perspectives and how we should improve it. We think this is a very useful experience. 
