import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_table
import plotly.express as px
import dash_bootstrap_components as dbc


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

df['symbol'] = df['symbol'].str.replace('MSFT', 'Microsoft', regex = True)
df['symbol'] = df['symbol'].str.replace('AMZN', 'Amazon', regex = True)
df['symbol'] = df['symbol'].str.replace('GOOG', 'Google', regex = True)
df['symbol'] = df['symbol'].str.replace('AAPL', 'Apple', regex = True)
df = df.rename(columns = {"symbol": "company"})


app.layout = html.Div([
    # Setting the main title of the Dashboard
    html.H1("Stock Price Data Analysis", style={"textAlign": "center"}),
    # Dividing the dashboard in tabs
    dcc.Tabs(id="tabs", children=[
        # Defining the layout of the first Tab
        dcc.Tab(label='Stock Trends', children=[
            html.Div([html.H1("Dataset Introduction", style={'textAlign': 'center'}),
                dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.iloc[0:5,:].to_dict("rows"),
                ),
                html.H1("Price history", style={'textAlign': 'center'}),
                # Adding the first dropdown menu and the subsequent time-series graph
                dcc.Dropdown(id='my-dropdown',
                             options=[{'label': 'IBM', 'value': 'IBM'},
                                      {'label': 'Apple','value': 'Apple'}, 
                                      {'label': 'Amazon', 'value': 'Amazon'}, 
                                      {'label': 'Microsoft','value': 'Microsoft'},
                                      {'label': 'Google','value': 'Google'}], 
                             multi=True,value=['Apple'],
                             style={"display": "block", "margin-left": "auto", 
                                    "margin-right": "auto", "width": "60%"}),
                dcc.Graph(id='history'),
                html.H1("Montly change", style={'textAlign': 'center'}),
                
                dcc.Graph(id='monthchange')
            ], className="container"),
        ]),
        # Defining the layout of the second tab
        dcc.Tab(label='Investment Value', children=[
            html.H1("Facebook Metrics Distributions", 
                    style={"textAlign": "center"}),
            # Adding a dropdown menu and the subsequent histogram graph
            html.Div([
                      html.Div([dcc.Dropdown(id='feature-selected1',
                      options=[{'label': i.title(),
                                'value': i} for i in df.columns.values[1:]], 
                                 value="Type")],
                                 className="twelve columns", 
                                 style={"display": "block", "margin-left": "auto",
                                        "margin-right": "auto", "width": "60%"}),
                    ], className="row",
                    style={"padding": 50, "width": "60%", 
                           "margin-left": "auto", "margin-right": "auto"}),
                    dcc.Graph(id='my-graph2'),
        ])
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
                   'rangeslider': {'visible': True}, 'type': 'date'},
             yaxis={"title":"Stock price (USD)"})}
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
    # trace = go.Bar(x=df2.date, y=df2.monthly_return)

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
            showlegend=False)
    return figure



if __name__ == '__main__':
    app.run_server(debug=True)