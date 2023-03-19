from dash import Dash, dcc, html
from dash.dependencies import Input, Output

app = Dash('my app')

app.layout = html.Div(
    [
         html.H1('Hello World!'),
         htlm.Label(
             )
         dcc.Input(
             name = 'Stock Tickers',
             value = 'TSLA',
             id='my_input'
        ),
        dcc.Graph(
            figure={
                'data':[
                    {'x':[1,2],'y':[3,1]}
                ]
            },
            id='my-graph'
        )
    ]
)



app.server.run(debug=True)



