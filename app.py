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

df = pd.read_csv('https://raw.githubusercontent.com/vega/vega-datasets/master/data/stocks.csv')
df['date']= pd.to_datetime(df['date']) 

# Extract "year" from the datetime
df['year'] = pd.DatetimeIndex(df['date']).year 

# Calculate monthly price change
df['monthly_return'] = df.groupby('symbol')['price'].pct_change()

# Calculate standard deviation as a proxy for volatility and risk
df['volatility'] = df.groupby(['symbol','year'])['price'].transform('std')
# Separate the dataframe to calculate investment return for Microsoft
df_msft = df[df['symbol'] == "MSFT"].copy()
df_msft = df_msft.reset_index(drop = True)

# Number of Microsoft shares I can buy with initial investment $10000 
# in January 1, 2001
df_msft['shares'] = 10000 / df_msft.loc[0, 'price']

# My investment value, calculated by shares*price
df_msft['inv_value'] = df_msft['shares'] * df_msft['price']

# Calculate the overall return of Microsoft, using 
# end-investment-value / start-investment-value - 1
# between January 1, 2001 and March 1, 2010
msft_inv_value0 = df_msft['inv_value'][0]
msft_inv_value1 = df_msft.iloc[-1]['inv_value']
msft_return = msft_inv_value1 / msft_inv_value0 - 1
print('{:.2%}'.format(msft_return))

# Separate the dataframe to calculate investment return for Amazon
df_amazon = df[df['symbol'] == "AMZN"].copy()
df_amazon = df_amazon.reset_index(drop = True)

# Number of Amazon shares I can buy with initial investment $10000
# in January 1, 2001
df_amazon['shares'] = 10000 / df_amazon.loc[0, 'price']

# My investment value, calculated by shares*price
df_amazon['inv_value'] = df_amazon['shares'] * df_amazon['price']

# Calculate the overall return of Amazon, using 
# end-investment-value / start-investment-value - 1
# between January 1, 2001 and March 1, 2010
amazon_inv_value0 = df_amazon['inv_value'][0]
amazon_inv_value1 = df_amazon.iloc[-1]['inv_value']
amazon_return = amazon_inv_value1 / amazon_inv_value0 - 1
print('{:.2%}'.format(amazon_return))


# Separate the dataframe to calculate investment return for IBM
df_ibm = df[df['symbol'] == "IBM"].copy()
df_ibm = df_ibm.reset_index(drop = True)

# Number of IBM shares I can buy with initial investment $10000
# in January 1, 2001
df_ibm['shares'] = 10000 / df_ibm.loc[0, 'price']

# My investment value, calculated by shares*price
df_ibm['inv_value'] = df_ibm['shares'] * df_ibm['price']

# Calculate the overall return of IBM, using 
# end-investment-value / start-investment-value - 1
# between January 1, 2001 and March 1, 2010
ibm_inv_value0 = df_ibm['inv_value'][0]
ibm_inv_value1 = df_ibm.iloc[-1]['inv_value']
ibm_return = ibm_inv_value1 / ibm_inv_value0 - 1
print('{:.2%}'.format(ibm_return))

# Separate the dataframe to calculate investment return for Google
df_google = df[df['symbol'] == "GOOG"].copy()
df_google = df_google.reset_index(drop = True)

# Number of Google shares I can buy with initial investment $10000
# in January 1, 2001
df_google['shares'] = 10000 / df_google.loc[0, 'price']

# My investment value, calculated by shares*price
df_google['inv_value'] = df_google['shares'] * df_google['price']

# Calculate the overall return of Google, using 
# end-investment-value / start-investment-value - 1
# between January 1, 2001 and March 1, 2010
google_inv_value0 = df_google['inv_value'][0]
google_inv_value1 = df_google.iloc[-1]['inv_value']
google_return = google_inv_value1 / google_inv_value0 - 1

# Separate the dataframe to calculate investment return for Apple
df_apple = df[df['symbol'] == "AAPL"].copy()
df_apple = df_apple.reset_index(drop = True)

# Number of Apple shares I can buy with initial investment $10000
# in January 1, 2001
df_apple['shares'] = 10000 / df_apple.loc[0, 'price']

# My investment value, calculated by shares*price
df_apple['inv_value'] = df_apple['shares'] * df_apple['price']

# Calculate the overall return of Apple, using 
# end-investment-value / start-investment-value - 1
# between January 1, 2001 and March 1, 2010
apple_inv_value0 = df_apple['inv_value'][0]
apple_inv_value1 = df_apple.iloc[-1]['inv_value']
apple_return = apple_inv_value1 / apple_inv_value0 - 1
print('{:.2%}'.format(apple_return))


# Create a new data frame that displays the overall investment return
# from January 1, 2001 to March 1, 2010
df_return = pd.DataFrame({'company': ['Microsoft', 'Amazon', 'IBM', 'Google', 'Apple'],
                          'investment_value': [msft_inv_value1, amazon_inv_value1, ibm_inv_value1, 
                                               google_inv_value1, apple_inv_value1],
                           'investment_return': [msft_return, amazon_return, ibm_return, 
                                                 google_return, apple_return]})
df_return


# Concatenate the data frames together
dflist = [df_msft,df_amazon, df_ibm, df_google, df_apple]
df = pd.concat(dflist)

# Reset index
df = df.reset_index(drop = True)

# Reagrange the order of columns
df = df[['date', 'year', 'symbol', 'price', 'shares', 'monthly_return', 'volatility', 'inv_value']]

# Replace stock symbols with company names
# Improve readability
df['symbol'] = df['symbol'].str.replace('MSFT', 'Microsoft', regex = True)
df['symbol'] = df['symbol'].str.replace('AMZN', 'Amazon', regex = True)
df['symbol'] = df['symbol'].str.replace('GOOG', 'Google', regex = True)
df['symbol'] = df['symbol'].str.replace('AAPL', 'Apple', regex = True)
df = df.rename(columns = {"symbol": "company"})



# variables for plot on tab 2
layout = go.Layout(title = 'Investment value change'
                   )


fig  = dict(
        data=[
            dict(
                x=df.date,
                y = df[df.company == 'Microsoft']['inv_value'],
                name='Microsoft',
                marker=dict(
                    color='#FF0056'
                )
            ),
             dict(
                x=df.date,
                y = df[df.company == 'Apple']['inv_value'],
                name='Apple',
                marker=dict(
                    color='#5E0DAC'
                )
            ),
             dict(
                x=df.date,
                y = df[df.company == 'Google']['inv_value'],
                name='Google',
                marker=dict(
                    color='#FF7400'
                )
             ),
                 dict(
                x=df.date,
                y  = df[df.company == 'Amazon']['inv_value'],
                name='Amazon',
                marker=dict(
                    color='#375CB1'
                )
                 ),
                 dict(
                x=df.date,
                y = df[df.company == 'IBM']['inv_value'],
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
         '2010-02-01']
date_mark = {i : dates[i] for i in range(0,12)}


app.layout = html.Div([
    # Setting the main title of the Dashboard
    html.H1("Stock Price Data Analysis", style={"textAlign": "center"}),
    # Dividing the dashboard in tabs
    dcc.Tabs(id="tabs", children=[
        # Defining the layout of the first Tab
        dcc.Tab(label='Stock Trends', children=[
            html.Div([html.H1("Dataset Introduction", style={'textAlign': 'center'}),
                
                html.H1("Price history", style={'textAlign': 'center'}),
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
                html.H1("Montly change", style={'textAlign': 'center'}),
                
                dcc.Graph(id='monthchange', 
                          style={'width': '70%',
                                "display": "block",
                                "margin-left": "auto",
                                "margin-right": "auto",
                                'textAlign': 'center'})
            ], className="container"),
        ]),
        # Defining the layout of the second tab
        dcc.Tab(label='Investment Value/Return', children=[
            html.H1("Investment Value Change", 
                    style={"textAlign": "center"}),
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
                                    max = 11,
                                    value = [0, 2]) 
                        ], style = {'width' : '75%',
                                    'fontSize' : '20px',
                                    'padding-left' : '100px',
                                    'display': 'inline-block',}),
        ]),
        # Defining the layout of the third Tab
        dcc.Tab(label='About our data', children=[
            html.Div([html.H1("Dataset Introduction", style={'textAlign': 'center'}),
                dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.iloc[0:5,:].to_dict("rows"),
                )]
            )])


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
    df2 = df[(df.date > dates[X[0]]) & (df.date < dates[X[1]])]
    
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



