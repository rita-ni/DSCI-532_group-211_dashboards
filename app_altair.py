import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
import altair as alt
import vega_datasets
import pandas as pd
import dash_table




app = dash.Dash(__name__, assets_folder='assets')
app.config['suppress_callback_exceptions'] = True
server = app.server
app.title = 'Dash app with pure Altair HTML'
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
def make_plot(xval = 'date',
              yval = 'price'):
    # Don't forget to include imports
    def mds_special():
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
    typeDict = {'Displacement':['quantitative','Displacement (mm)'],
                'Cylinders':['quantitative', 'Cylinders (#)'],
                'Miles_per_Gallon':['quantitative', 'Fuel Efficiency (mpg)'],
                'Horsepower':['quantitative', 'Horsepower (hp)']
                }
    # Create a plot from the cars dataset
    highlight = alt.selection(type='single', on='click',
                          fields=['company'])
    brush = alt.selection(type='interval', encodings=['x'])
    chart = alt.Chart(df).mark_line().encode(
                alt.X('date', title = 'Date', scale=alt.Scale(domain=brush)),
                alt.Y('price', title = 'Stock price (USD)'),
                color=alt.Color('company', title = "Company"),
                size=alt.condition(~highlight, alt.value(3), alt.value(5))
            ).add_selection(highlight
            ).properties(title='Historical Stock Prices',
                        width=800, height=350)
    bars = alt.Chart(df).mark_bar().encode(
                y='monthly_return',
                x=alt.X('date', scale=alt.Scale(domain=brush)),
                color=alt.condition(
                    alt.datum.monthly_return > 0,
                    alt.value("steelblue"),  # The positive color
                    alt.value("orange"))
            ).transform_filter(highlight).facet(facet='company', columns=2)
    lower = alt.Chart(df).mark_line().encode(
                alt.X('date', title = ' ', scale=alt.Scale(domain=brush)),
                alt.Y('price', title = ' ', axis = None),
                color=alt.Color('company', title = "Company"),
                size=alt.condition(~highlight, alt.value(3), alt.value(5))
            ).add_selection(highlight
            ).properties(title = 'Feel free to drag across a time period below to zoom in the chart!',
    height=60, width = 800
    ).add_selection(brush)
    return alt.vconcat(chart, lower) & bars
app.layout = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.Div('Plotly Dash', className="app-header--title")
        ]
    ),
    ### ADD CONTENT HERE like: html.H1('text'),
    html.H1('This is my first dashboard'),
    
    html.H3('Here is our first plot:'),
    html.Iframe(
        sandbox='allow-scripts',
        id='plot',
        height='1660',
        width='1000',
        style={'border-width': '0'},
        ################ The magic happens here
        srcDoc=make_plot().to_html()
        ################ The magic happens here
        ),
        html.H3('Dropdown to control Altair Chart'),
        dcc.Dropdown(
        id='dd-chart-x',
        options=[
            {'label': 'IBM', 'value': 'IBM'},
                                      {'label': 'Apple','value': 'Apple'},
                                      {'label': 'Amazon', 'value': 'Amazon'},
                                      {'label': 'Microsoft','value': 'Microsoft'},
                                      {'label': 'Google','value': 'Google'}
        ],
        value='Horsepower',
        style=dict(width='45%',
                   verticalAlign="middle")
        ),
        # Just to add some space
        html.Iframe(height='200', width='10',style={'border-width': '0'})
])
# This callback tells Dash the output is the `plot` IFrame; srcDoc is a
# special property that takes in RAW html as an input and renders it
# As input we take in the values from second dropdown we created (dd-chart)
# then we run update_plot
if __name__ == '__main__':
    app.run_server(debug=True)