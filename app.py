import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
import altair as alt


app = dash.Dash()
server = app.server

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


# variables for plot on tab 2
layout = go.Layout(title = 'Investment value change'
                   )


fig  = dict(
        data=[
            dict(
                x=df_tab2.date,
                y = df_tab2[df_tab2.company == 'Microsoft']['inv_value'],
                name='Microsoft',
                marker=dict(
                    color='#FF0056'
                )
            ),
             dict(
                x=df_tab2.date,
                y = df_tab2[df_tab2.company == 'Apple']['inv_value'],
                name='Apple',
                marker=dict(
                    color='#5E0DAC'
                )
            ),
             dict(
                x=df_tab2.date,
                y = df_tab2[df_tab2.company == 'Google']['inv_value'],
                name='Google',
                marker=dict(
                    color='#FF7400'
                )
             ),
                 dict(
                x=df_tab2.date,
                y  = df_tab2[df_tab2.company == 'Amazon']['inv_value'],
                name='Amazon',
                marker=dict(
                    color='#375CB1'
                )
                 ),
                 dict(
                x=df_tab2.date,
                y = df_tab2[df_tab2.company == 'IBM']['inv_value'],
                name='IBM',
                marker=dict(
                    color='#FF4F00'
                )
             )    
        ],
 layout = layout)

##variables for slider on tab 2
dates = [
         '2004-08-01', '2005-02-01', '2005-08-01', '2006-02-01', '2006-08-01',
         '2007-02-01',  '2007-08-01','2008-02-01',  '2008-08-01','2009-02-01',  '2009-08-01',
         '2010-02-01', '2010-03-01']
date_mark = {i : dates[i] for i in range(0,13)}


app.layout = html.Div([
    # Setting the main title of the Dashboard
    html.H1("Stock Price Data Analysis", style={"textAlign": "center", 'fontFamily': 'arial'}),
    # Dividing the dashboard in tabs
    dcc.Tabs(id="tabs", children=[
        # Defining the layout of the first Tab
        dcc.Tab(label='Stock Trends', children=[
            html.Div([
                html.H1("Price History", style={'textAlign': 'center', 'fontFamily': 'arial'}),
                html.H2("From 2000 to 2010, Apple's stock price increased 760%.", style={'textAlign': 'center', 'fontFamily': 'arial'}),
                html.H3("In this interactive chart below, you can visualize how the sotcks of 5 major tech companies changed between 2000 and 2010.", 
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
                             multi=True,value=['Apple', 'IBM', 'Google'],
                             style={"display": "block", "margin-left": "auto", 
                                    "margin-right": "auto", "width": "60%"}),
                                 
                dcc.Graph(id='history', 
                          style={'height': 500,
                                'width': '70%',
                                "display": "block",
                                "margin-left": "auto",
                                "margin-right": "auto",}),
                
                html.H1("Monthly change", style={'textAlign': 'center', 'fontFamily': 'arial'}),
                html.H3("Use this chart to explore the stock price monthly percentage changes.", 
                        style={'textAlign': 'center', 'fontFamily': 'arial'}),
                html.P("Use the slide bar down the graph to select the time range.", 
                        style={'textAlign': 'center', 'fontFamily': 'arial'}),
                dcc.Graph(id='monthchange', 
                          style={'width': '70%',
                                "display": "block",
                                "margin-left": "auto",
                                "margin-right": "auto",
                                'textAlign': 'center'})
            ], className="container"),
        ]),
        # Defining the layout of the second tab
        dcc.Tab(label='Investment Value', children=[
            html.H1("How much would my investment be?", 
                    style={"textAlign": "center", 'fontFamily': 'arial'}),
            html.H3("""If I invested $10,000 in each of the 5 tech companies in August 2004 (when Google held its IPO), 
                    how much would have my investment been in later days?""", 
                        style={'textAlign': 'center', 'fontFamily': 'arial'}),
                html.P("Use the year slide bar to select the time range and find out the investment value.", 
                        style={'textAlign': 'center', 'fontFamily': 'arial'}), 
            # adding investment plot
            dcc.Graph(id = 'investment', 
                    style={'width': '75%',
                                "display": "block",
                                "margin-left": "auto",
                                "margin-right": "auto",
                                'textAlign': 'center'}),
            # range slider
                html.P([
                    html.Label("Time Period"),
                    dcc.RangeSlider(id = 'slider',
                                    marks = date_mark,
                                    min = 0,
                                    max = 12,
                                    value = [0, 2]) 
                        ], style = {'width' : '75%',
                                    'fontSize' : '20px',
                                    'padding-left' : '100px',
                                    'display': 'inline-block',}),
        ]),
                dcc.Tab(label='About Our Data', children=[
            html.Div(children = [html.H1("Dataset Introduction", style={'textAlign': 'center', 'fontFamily': 'arial'}),
            html.P("""The dataset we are using is the  Stocks  data from the vega-datasets. 
            The dataset has 560 observations in total. """, style={'fontFamily': 'arial'}),

    
                dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df_original.columns],
                    data=df_original.iloc[0:5,:].to_dict("rows"),
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
        ])
    ])


@app.callback(Output('history', 'figure'),
              [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown):
    dropdown = {"Google": "Google", "IBM": "IBM","Apple": "Apple","Amazon": "Amazon","Microsoft": "Microsoft",}
    trace = []
    for stock in selected_dropdown:
        trace.append(
          go.Scatter(x=df[df["company"] == stock]["date"],
                     y=df[df["company"] == stock]["price"],
                     mode='lines', opacity=0.7, 
                     name=f' {dropdown[stock]}',textposition='bottom center'))
    data = [val for val in trace]
    figure = {'data': data,
              'layout': go.Layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FF0056'],
            height=600,
            title=f"Historial Prices for {', '.join(str(dropdown[i]) for i in selected_dropdown)} Over Time",
            xaxis={"title":"Date",
                   'rangeselector': {'buttons': list([{'count': 5, 'label': '5Y', 
                                                       'step': 'year', 
                                                       'stepmode': 'backward'},
                                                       {'count': 2, 'label': '2Y', 
                                                       'step': 'year', 
                                                       'stepmode': 'backward'},
                                                      {'count': 1, 'label': '1Y',
                                                       'step': 'year', 
                                                       'stepmode': 'backward'},
                                                      {'step': 'all'}])},
                   'rangeslider': {'visible': True}, 'type': 'date',
                                   'range':['2007-04-01', '2009-01-01']},
             yaxis={"title":"Stock price (USD)"},)}
    return figure


@app.callback(Output('monthchange', 'figure'),
              [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    dropdown = {"Google": "Google", "IBM": "IBM","Apple": "Apple","Amazon": "Amazon","Microsoft": "Microsoft",}
    trace1 = []
    for stock in selected_dropdown_value:
        trace1.append(stock)
    df2 = df[df.company.isin(trace1)].dropna()
    bins = [-999, 0, 999]
    labels = ['neg', 'pos']
    df2['labels'] = pd.cut(df2.monthly_return, bins=bins, labels=labels)

    figure = px.bar(df2, x = 'date',
                        y = 'monthly_return',
                        color = 'labels',
                        facet_row = 'company',
                        labels={'monthly_return':'Monthly Change %'},
                        category_orders={"company": trace1})
    
    figure = figure.update_layout(height=400*len(trace1), 
            title_text=f"Monthly price change for {', '.join(str(dropdown[i]) for i in selected_dropdown_value)} Over Time",
            xaxis={"title":"Date",
                   'rangeslider': {'visible': True}, 'type': 'date'},
            barmode='relative',
            showlegend=False,
            title_xanchor = 'auto')
    return figure



## call back for slider on tab 2
@app.callback(Output('investment', 'figure'),
             [Input('slider', 'value')])
def update_figure(X):
    df2 = df_tab2[(df_tab2.date >= dates[X[0]]) & (df_tab2.date <= dates[X[1]])]
    
    fig  = dict(
        data=[
            dict(
                x=df2.date,
                y = df2[df2.company == 'Microsoft']['inv_value'],
                name='Microsoft',
                marker=dict(
                    color='#FF0056'
                )
            ),
             dict(
                x=df2.date,
                y = df2[df2.company == 'Apple']['inv_value'],
                name='Apple',
                marker=dict(
                    color='#5E0DAC'
                )
            ),
             dict(
                x=df2.date,
                y = df2[df2.company == 'Google']['inv_value'],
                name='Google',
                marker=dict(
                    color='#FF7400'
                )
             ),
                 dict(
                x=df2.date,
                y  = df2[df2.company == 'Amazon']['inv_value'],
                name='Amazon',
                marker=dict(
                    color='#375CB1'
                )
                 ),
                 dict(
                x=df2.date,
                y = df2[df2.company == 'IBM']['inv_value'],
                name='IBM',
                marker=dict(
                    color='#FF4F00'
                )
             )    
        ],
            layout = layout)
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)
