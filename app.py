#importing required packages for the plot

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
import altair as alt
import vega_datasets
import pandas as pd
import dash_table
import plotly.express as px
import plotly.graph_objs as go



##########################################
##   Data wrangling begins for dashboard  ##
###########################################

df_original = pd.read_csv('https://raw.githubusercontent.com/vega/vega-datasets/master/data/stocks.csv')
df = df_original.copy()
df['date']= pd.to_datetime(df['date']) 

# Extract "year" from the datetime
df['year'] = pd.DatetimeIndex(df['date']).year 

# Calculate monthly price change
df['monthly_return'] = round(df.groupby('symbol')['price'].pct_change(),2)

# Calculate standard deviation as a proxy for volatility and risk
df['volatility'] = round(df.groupby(['symbol','year'])['price'].transform('std'), 2)

# Reagrange the order of columns for data frame in Tab1 
df = df[['date', 'year', 'symbol', 'price', 'monthly_return', 'volatility']]

# Replace stock symbols with company names
# Improve readability
df['symbol'] = df['symbol'].str.replace('MSFT', 'Microsoft', regex = True)
df['symbol'] = df['symbol'].str.replace('AMZN', 'Amazon', regex = True)
df['symbol'] = df['symbol'].str.replace('GOOG', 'Google', regex = True)
df['symbol'] = df['symbol'].str.replace('AAPL', 'Apple', regex = True)
df = df.rename(columns = {"symbol": "company"})

#### Create new data frame for Tab2
# Subset the data frame to "2004-08-01", the time of Google IPO
df_sub = df.query('date>="2004-08-01"')
# Separate the dataframe to calculate investment return for Microsoft
df_msft2 = df_sub[df_sub['company'] == "Microsoft"].copy()
df_msft2 = df_msft2.reset_index(drop = True)

# Number of Microsoft shares I can buy with initial investment $10000 
# in August 1, 2004
df_msft2['shares'] = round(10000 / df_msft2.loc[0, 'price'],2)

# My investment value, calculated by shares*price
df_msft2['inv_value'] = round(df_msft2['shares'] * df_msft2['price'], 0)

# Calculate the overall return of Microsoft, using 
# end-investment-value / start-investment-value - 1
# between August 1, 2004 and March 1, 2010
msft2_inv_value0 = df_msft2['inv_value'][0]
msft2_inv_value1 = df_msft2.iloc[-1]['inv_value']

# Separate the dataframe to calculate investment return for Amazon
df_amazon2 = df_sub[df_sub['company'] == "Amazon"].copy()
df_amazon2 = df_amazon2.reset_index(drop = True)

# Number of Amazon shares I can buy with initial investment $10000
# in January 1, 2001
df_amazon2['shares'] = round(10000 / df_amazon2.loc[0, 'price'],2)

# My investment value, calculated by shares*price
df_amazon2['inv_value'] = round(df_amazon2['shares'] * df_amazon2['price'], 0)

# Calculate the overall return of Amazon, using 
# end-investment-value / start-investment-value - 1
# between August 1, 2004 and March 1, 2010
amazon2_inv_value0 = df_amazon2['inv_value'][0]
amazon2_inv_value1 = df_amazon2.iloc[-1]['inv_value']
amazon_return2 = amazon2_inv_value1 / amazon2_inv_value0 - 1

# Separate the dataframe to calculate investment return for IBM
df_ibm2 = df_sub[df_sub['company'] == "IBM"].copy()
df_ibm2 = df_ibm2.reset_index(drop = True)

# Number of IBM shares I can buy with initial investment $10000
# in January 1, 2001
df_ibm2['shares'] = round(10000 / df_ibm2.loc[0, 'price'],2)

# My investment value, calculated by shares*price
df_ibm2['inv_value'] = round(df_ibm2['shares'] * df_ibm2['price'], 0)

# Calculate the overall return of IBM, using 
# end-investment-value / start-investment-value - 1
# between August 1, 2004 and March 1, 2010
ibm2_inv_value0 = df_ibm2['inv_value'][0]
ibm2_inv_value1 = df_ibm2.iloc[-1]['inv_value']
ibm_return2 = ibm2_inv_value1 / ibm2_inv_value0 - 1


# Separate the dataframe to calculate investment return for Google
df_google2 = df_sub[df_sub['company'] == "Google"].copy()
df_google2 = df_google2.reset_index(drop = True)

# Number of Google shares I can buy with initial investment $10000
# in January 1, 2001
df_google2['shares'] = round(10000 / df_google2.loc[0, 'price'], 0)

# My investment value, calculated by shares*price
df_google2['inv_value'] = round(df_google2['shares'] * df_google2['price'],0)

# Calculate the overall return of Google, using 
# end-investment-value / start-investment-value - 1
# between August 1, 2004 and March 1, 2010
google2_inv_value0 = df_google2['inv_value'][0]
google2_inv_value1 = df_google2.iloc[-1]['inv_value']
google_return2 = google2_inv_value1 / google2_inv_value0 - 1


# Separate the dataframe to calculate investment return for Apple
df_apple2 = df_sub[df_sub['company'] == "Apple"].copy()
df_apple2 = df_apple2.reset_index(drop = True)

# Number of Apple shares I can buy with initial investment $10000
# in January 1, 2001
df_apple2['shares'] = round(10000 / df_apple2.loc[0, 'price'], 2)

# My investment value, calculated by shares*price
df_apple2['inv_value'] = round(df_apple2['shares'] * df_apple2['price'], 0)

# Calculate the overall return of Apple, using 
# end-investment-value / start-investment-value - 1
# between August 1, 2004 and March 1, 2010
apple2_inv_value0 = df_apple2['inv_value'][0]
apple2_inv_value1 = df_apple2.iloc[-1]['inv_value']
apple_return2 = apple2_inv_value1 / apple2_inv_value0 - 1

# Concatenate the data frames together
dflist2 = [df_msft2,df_amazon2, df_ibm2, df_google2, df_apple2]
df_tab2 = pd.concat(dflist2)

# Reset index
df_tab2 = df_tab2.reset_index(drop = True)


##########################################
##   Data wrangling finished for dashboard  ##
###########################################

## Declaring variables used in dashboard

# variables for date slider on tab3
dates = [
         '2004-08-01', '2005-02-01', '2005-08-01', '2006-02-01', '2006-08-01',
         '2007-02-01',  '2007-08-01','2008-02-01',  '2008-08-01','2009-02-01',  '2009-08-01',
         '2010-02-01', '2010-03-01']
date_mark = {i : dates[i] for i in range(0,13)}


def make_plot(df):
    """
    Generates plots on tab 2 of the dashboard.

    Input - Data frame to be plotted

    Returns - Stock trend plot 
                slider
                monthly change chart

    """
    def mds_special():

        """
        Function for default MDS configuration  for labels, titles etc. 
        to be applied to altair plots
        """
        font = "Arial"
        axisColor = "#000000"
        gridColor = "#DEDDDD"
        return {
            "config": {
                "title": {
                    "fontSize": 24,
                    "font": font,
                    "anchor": "middle", # equivalent of left-aligned.
                    "fontColor": "#000000"
                },
                'view': {
                    "height": 300,
                    "width": 400
                },
                "axisX": {
                    "domain": True,
                    #"domainColor": axisColor,
                    "gridColor": gridColor,
                    "domainWidth": 1,
                    "grid": False,
                    "labelFont": font,
                    "labelFontSize": 12,
                    "labelAngle": 0,
                    "tickColor": axisColor,
                    "tickSize": 5, # default, including it just to show you can change it
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "X Axis Title (units)",
                },
                "axisY": {
                    "domain": False,
                    "grid": True,
                    "gridColor": gridColor,
                    "gridWidth": 1,
                    "labelFont": font,
                    "labelFontSize": 14,
                    "labelAngle": 0,
                    #"ticks": False, # even if you don't have a "domain" you need to turn these off.
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "Y Axis Title (units)",
                    # titles are by default vertical left of axis so we need to hack this
                    #"titleAngle": 0, # horizontal
                    #"titleY": -10, # move it up
                    #"titleX": 18, # move it to the right so it aligns with the labels
                },
            }
                }
    # register the custom theme under a chosen name
    alt.themes.register('mds_special', mds_special)
    # enable the newly registered theme
    alt.themes.enable('mds_special')
    #alt.themes.enable('none') # to return to default
    
    # Create a plot from the cars dataset
    highlight = alt.selection(type='single', on='click',
                          fields=['company'])
    brush = alt.selection(type='interval', encodings=['x'])

    # stock history chart
    chart = alt.Chart(df).mark_line().encode(
                alt.X('date', title = 'Date', scale=alt.Scale(domain=brush)),
                alt.Y('price', title = 'Stock price (USD)'),
                color=alt.Color('company', title = "Company"),
                size=alt.condition(~highlight, alt.value(3), alt.value(5))
            ).add_selection(highlight
            ).properties(title='Historical Stock Prices',
                        width=900, height=350)
    
    
    bars = alt.Chart(df).mark_bar().encode(
                y=alt.Y('monthly_return', axis=alt.Axis(format='%')),
                x=alt.X('date', scale=alt.Scale(domain=brush)),
                color=alt.condition(
                    alt.datum.monthly_return > 0,
                    alt.value("steelblue"),  # The positive color
                    alt.value("orange"))).properties(width = 470, title = 'Monthly price change (%)'
            ).transform_filter(highlight).facet(facet='company', columns=2)
    
    #  monthly change chart
    lower = alt.Chart(df).mark_line().encode(
                alt.X('date', title = ' ', scale=alt.Scale(domain=brush)),
                alt.Y('price', title = ' ', axis = None),
                color=alt.Color('company', title = "Company"),
                size=alt.condition(~highlight, alt.value(3), alt.value(5))
            ).add_selection(highlight
            ).properties(title = 'Feel free to drag across a time period below to zoom in the chart!',
    height=60, width = 900
    ).add_selection(brush)
   
    return alt.vconcat(chart , lower) & bars

def make_plot2(df):
    """
    Generates plots on tab 3 of the dashboard.

    Input - Data frame to be plotted

    Returns - Investment value plot
                
    """
    def mds_special():

        """
        Function for default MDS configuration  for labels, titles etc. 
        to be applied to altair plots
        """

        font = "Arial"
        axisColor = "#000000"
        gridColor = "#DEDDDD"
        return {
            "config": {
                "title": {
                    "fontSize": 24,
                    "font": font,
                    "anchor": "start", # equivalent of left-aligned.
                    "fontColor": "#000000"
                },
                'view': {
                    "height": 300,
                    "width": 400
                },
                "axisX": {
                    "domain": True,
                    #"domainColor": axisColor,
                    "gridColor": gridColor,
                    "domainWidth": 1,
                    "grid": False,
                    "labelFont": font,
                    "labelFontSize": 12,
                    "labelAngle": 0,
                    "tickColor": axisColor,
                    "tickSize": 5, # default, including it just to show you can change it
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "X Axis Title (units)",
                },
                "axisY": {
                    "domain": False,
                    "grid": True,
                    "gridColor": gridColor,
                    "gridWidth": 1,
                    "labelFont": font,
                    "labelFontSize": 14,
                    "labelAngle": 0,
                    #"ticks": False, # even if you don't have a "domain" you need to turn these off.
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "Y Axis Title (units)",
                    # titles are by default vertical left of axis so we need to hack this
                    #"titleAngle": 0, # horizontal
                    #"titleY": -10, # move it up
                    #"titleX": 18, # move it to the right so it aligns with the labels
                },
            }
                }
    # register the custom theme under a chosen name
    alt.themes.register('mds_special', mds_special)
    # enable the newly registered theme
    alt.themes.enable('mds_special')
    #alt.themes.enable('none') # to return to default
    
    # Plot for investment value change 
    chart = alt.Chart(df).mark_line().encode(
    x = alt.X('date:T',  title = 'Month'),
    y = alt.Y('inv_value:Q', title = 'Investment Value $USD'),
    color = alt.Color('company:N', title = 'Company',
                  sort = ['Apple','Google','Amazon', 'IBM', 'Microsoft'])
            ).properties(width = 800, height = 400, title = 'Investment value change over the time')

    return chart + chart.mark_circle()


####################################
#### App layout begins ############
####################################
app = dash.Dash()
server = app.server

app.layout = html.Div([
    # Setting the main title of the Dashboard
    html.H1("Stock Price Data Analysis", style={"textAlign": "center", 'fontFamily': 'arial'}),
    
    # Dividing the dashboard in  3 tabs
    dcc.Tabs(id="tabs", children=[
        # Defining the layout of the first Tab
        
        dcc.Tab(label='About Our Data', children=[
            html.Div(children = [html.H1("Dataset Introduction", style={'textAlign': 'center', 'display': 'block', 'fontFamily': 'arial'}),
            html.P("""The dataset we are using is the  Stocks  data from the vega-datasets. 
            The dataset has 560 observations in total. """, style={'fontFamily': 'arial', 'display': 'inline-block'}),

                # addding dataset intro table to tab1

                dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df_original.columns],
                    data=df_original.iloc[[0,1,2,123,124,125,246,247,248,369,370,371,437,438,439], :].to_dict("rows"),
                    style_cell={
                         'textAlign': 'center',
                        'height': 'auto',
                        'width': 'auto',
                        'whiteSpace': 'normal'}

                ),
            html.P("""There are 5 companies in total, and they are Microsoft, Amazon, IBM, Google, and Apple.""", style={'fontFamily': 'arial'}),
            html.P("""The date column lists out the date when the stock price was recorded.
            The value of the date column ranges from January 1, 2000 to March 1, 2010. The date range is the same for Microsoft, Amazon, IBM, and Apple. Each of them has 123 observations in the dataset. 
            Since Google held its IPO in August, 2004, the record for Google started from August 1, 2004. 
            Therefore, there are 68 observations for Google.""", style={'fontFamily': 'arial'}),
            html.P(""" The price column lists out the price of that stock on the recorded date.""", style={ 'fontFamily': 'arial'}),
            html.P(""" The purpose of this app is to help people form a better view of stock price fluctuations 
                        and long-term investment gains.""", style={ 'fontFamily': 'arial'}),
   
            ], className="container"), 
        ]),

        # Tab2 for historic stock trends

        dcc.Tab(label='Stock Trends', children=[
            html.Div([
                # adding text, title etc for tab2
                html.H1("Price History", style={'textAlign': 'center', 'fontFamily': 'arial'}),
                html.H2("From 2000 to 2010, Apple's stock price increased 760%.", style={'textAlign': 'center', 'fontFamily': 'arial'}),
                html.H3("In this interactive chart below, you can visualize how the stocks of 5 major tech companies changed between 2000 and 2010.", 
                        style={'textAlign': 'center', 'fontFamily': 'arial'}),
                html.P("Use the dropdown window to select the company you want to explore. Use the slide bar down the graph to select the time range.", 
                        style={'textAlign': 'center', 'fontFamily': 'arial'}), 
              
                # Adding the first dropdown menu and the subsequent time-series graph
                dcc.Dropdown(id='my-dropdown',
                             options=[{'label': 'IBM', 'value': 'IBM'},
                                      {'label': 'Apple','value': 'Apple'}, 
                                      {'label': 'Amazon', 'value': 'Amazon'}, 
                                      {'label': 'Microsoft','value': 'Microsoft'},
                                      {'label': 'Google','value': 'Google'}], 
                             multi=True,value=['IBM','Apple', 'Amazon', 'Microsoft', 'Google'],
                             style={"display": "block", "margin-left": "auto", 
                                    "margin-right": "auto", "width": "60%"}),
                
                # Importing chars created using altair 
                html.Iframe(
                        sandbox='allow-scripts',
                        id='plot',
                        height='1660',
                        width='1000',
                        style={'height': 1800,
                                'width': '70%',
                                "display": "block",
                                "margin-left": "auto",
                                "margin-right": "auto"},
                      
                        srcDoc=make_plot(df).to_html()   
                        )                         
            ], className="container"),
        ]),

            # Tab3
            dcc.Tab(label='Investment Value', children=[
                
            # adding text, title etc for tab3

            html.H1("How much would my investment be?", 
                    style={"textAlign": "center", 'fontFamily': 'arial'}),
            html.H3("""If I invested $10,000 in each of the 5 tech companies in August 2004 (when Google held its IPO), 
                    how much would have my investment been in later days?""", 
                        style={'textAlign': 'center', 'fontFamily': 'arial'}),
                html.P("Use the year slide bar to select the time range and find out the investment value.", 
                        style={'textAlign': 'center', 'fontFamily': 'arial'}), 
            
            # range slider for selecting time range
            html.P([
                    html.Label("Year range"),
                    dcc.RangeSlider(id = 'slider',
                                    marks = date_mark,
                                    min = 0,
                                    max = 12,
                                    value = [0, 12]) 
                        ], style = {'width' : '75%',
                                    'fontSize' : '20px',
                                    'padding-left' : '180px',
                                    'display': 'inline-block',}),
            
            # adding investment plot
              html.Iframe(
                        sandbox='allow-scripts',
                        id='plot2',
                        height='1660',
                        width='1000',
                        style={'height': 550,
                                'width': '70%',
                                "display": "block",
                                "margin-left": "auto",
                                "margin-right": "auto"},
                        
                        srcDoc=make_plot2(df_tab2).to_html()               
                        ),     
        ])    
            ], className="container"),
        ])
        
####################################
#### App layout ends ############
####################################  

## callbacks for interactivity based on drop-down menu on tab 2
@app.callback(
    dash.dependencies.Output('plot', 'srcDoc'),
    [dash.dependencies.Input('my-dropdown', 'value')])
def update_plot(selected_values):
    '''
    Takes in input based on list of options user select in 
        dropdown and updates plot
    Input - drop_down inputs selected
    Return - Updated plot

    '''
    
    # updating data frame based on selected values
    df_drop = df[df['company'].isin(selected_values)]
    
    updated_plot = make_plot(df_drop).to_html()
    
    return updated_plot


## callbacks for interactivity based on drop-down menu on tab 3
@app.callback(Output('plot2', 'srcDoc'),
             [Input('slider', 'value')])
def update_figure(X):
    '''
    Takes in input based on the time range user selects in 
        slider and updates plot
    Input - Slider range
    Return - Updated plot

    '''
    # updating dataframe
    df2 = df_tab2[(df_tab2.date >= dates[X[0]]) & (df_tab2.date <= dates[X[1]])]
    updated_plot = make_plot2(df2).to_html()
    
    return updated_plot


# main call 
if __name__ == '__main__':
    app.run_server(debug=True)


