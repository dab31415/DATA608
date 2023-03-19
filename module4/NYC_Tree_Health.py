'''
    DATA 608: Module 4
    Author: Donald Butler
    Date: 03/18/2023
    
    NYC Tree Health

    This module we'll be looking at the New York City tree census. This data was provided 
    by a volunteer driven census in 2015, and we'll be accessing it via the socrata API. 
    The main site for the data is here, and on the upper right hand side you'll be able 
    to see the link to the API.

'''

from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd

import datashader as ds
import datashader.transfer_functions as tf
import datashader.glyphs
from datashader import reductions
from datashader.core import bypixel
from datashader.utils import lnglat_to_meters as webm, export_image
from datashader.colors import colormap_select, Greys9, viridis, inferno

from functools import partial
import matplotlib.pyplot as plt

'''
This module we'll be looking at the New York City tree census. 
This data was provided by a volunteer driven census in 2015, 
and we'll be accessing it via the socrata API. The main site 
for the data is here, and on the upper right hand side you'll 
be able to see the link to the API.

The data is conveniently available in json format, so we 
should be able to just read it directly in to Pandas:
'''

url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json'

def GetTreeData():
    pageSize = 50000
    page = 0
    while (page == 0 or (df.shape[0] == (page * pageSize))):
        print(page)
        url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
               '$limit=' + str(pageSize) +\
               '&$offset=' + str(page * pageSize) +\
               '&$select=tree_id,health,spc_common,steward,borocode,boroname,latitude,longitude,x_sp,y_sp' +\
               '&$where=status=\'Alive\' AND health IS NOT NULL AND spc_common IS NOT NULL' +\
               '&$order=tree_id').replace(' ','%20')
        
        if (page == 0):
            df = pd.read_json(url)
        else:
            df = pd.concat([df,pd.read_json(url)])

        page += 1

    #Update health categories
    health_categories = pd.api.types.CategoricalDtype(categories=['Poor','Fair','Good'],ordered=True)
    df['health'] = df['health'].astype(health_categories)
    
    #Update steward categories
    steward_categories = pd.api.types.CategoricalDtype(categories=['None','1or2','3or4','4orMore'],ordered=True)
    df['steward'] = df['steward'].astype(steward_categories)
    
    return df

trees = GetTreeData()

#%%
app = dash.Dash()
app.layout = html.Div(children=[
    html.H1('NYC Tree Health'),
    html.P('Select a Borough: '),
    dcc.RadioItems(
        id='input-boro',
        options=[{'label': i, 'value': i} for i in np.sort(trees['boroname'].unique())],
        value='Bronx'),
    html.Div(id='output-a'),
    html.P('Select')
    ])


#%%




'''
#Defining some helper functions for DataShader
background = "black"
export = partial(export_image, background = background, export_path="export")
cm = partial(colormap_select, reverse=(background!="black"))

NewYorkCity = (( 913164.0,  1067279.0), (120966.0, 272275.0))
cvs = ds.Canvas(700,700, *NewYorkCity)
agg = cvs.points(trees, 'x_sp', 'y_sp')
view = tf.shade(agg, cmap = cm(viridis), how = 'log')
export(tf.spread(view, px=2), 'trees')


'''




'''



        if (i==0):
            df = pd.read_json(url)
        else:
            df = pd.concat([df,pd.read_json(url)])


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



'''