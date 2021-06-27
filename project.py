from inspect import trace
import pandas_datareader as web
import pandas as pd
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output , State




options_df=pd.read_csv("./BSE.csv")
app=dash.Dash()

options=[]

for i in range(options_df.shape[0]):
    options.append({'label':options_df['STOCK'][i],'value':options_df['CODE'][i]})


app.layout = html.Div([
    html.H1('Indian Stocks Closing Prices'),
    html.Div([
        html.H3('Enter a stock symbol:',style={'paddingRight':'30px'}),
        dcc.Dropdown(
            id='stock',
            options=options,
            value=['SENSEX'], # sets a default value
            multi=True,
            style={'fontSize':15, 'width':250,'margin-right':'25px'}
        )
    ],style={'display':'inline-block', 'verticalAlign':'top'}),
    html.Div([
        html.H3('Select start and end dates:'),
        dcc.DatePickerRange(
            id='dates',
            min_date_allowed=datetime.datetime(2000,1,1),
            max_date_allowed=datetime.datetime.today()-datetime.timedelta(days=1),
            start_date=datetime.datetime.today()-pd.DateOffset(years=5),
            end_date=datetime.datetime.today()-datetime.timedelta(days=1)
        )

    ],style={'display':'inline-block'}),
    html.Div([
        html.Button(
                    id='submit-button',
                    n_clicks=0,
                    children='Submit',
                    style={'fontSize':24, 'marginLeft':'30px'}
                )
    ],style={'display':'inline-block'}),
    dcc.Graph(
        id='graph',
        figure={
            'data': [
                {'x': web.DataReader('BSE/SENSEX',"quandl",datetime.datetime.today()-pd.DateOffset(years=5),datetime.datetime.today()-datetime.timedelta(days=1),api_key='fajHRFfJpL-owxz3cvAc').index,
                 'y': web.DataReader('BSE/SENSEX',"quandl",datetime.datetime.today()-pd.DateOffset(years=5),datetime.datetime.today()-datetime.timedelta(days=1),api_key='fajHRFfJpL-owxz3cvAc').Close}
            ]
        }
    )
])

@app.callback(Output('graph','figure'),[Input('submit-button','n_clicks')],[State('stock','value'),State('dates','start_date'),State('dates','end_date')])
def update_graph(n_clicks,stocks,start,end):
    start = datetime.datetime.strptime(start[:10], '%Y-%m-%d')
    end = datetime.datetime.strptime(end[:10], '%Y-%m-%d')
    full_name='BSE/'
    traces=[]
    for stock in stocks:
        df=web.DataReader(full_name+stock,"quandl",start,end,api_key='fajHRFfJpL-owxz3cvAc')
        traces.append({'x': df.index, 'y': df.Close,'name':list(options_df[options_df['CODE'].isin([stock])]['STOCK'])[0]})

    fig = {
        'data':traces,
        'layout': {'title':', '.join(list(options_df[options_df['CODE'].isin(stocks)]['STOCK']))+' Closing Prices'}
    }

    return fig


if __name__ == '__main__':
    app.run_server()



