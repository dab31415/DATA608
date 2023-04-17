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

from dash import Dash, dcc, html, Output, Input
#import dash_bootstrap_components as dbc
import plotly.express as px

import numpy as np
import pandas as pd

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
    pageSize = 300000
    page = 0
    df = pd.DataFrame()
    
    while (page == 0 or (df.shape[0] == (page * pageSize))):
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
    #health_categories = pd.api.types.CategoricalDtype(categories=['Poor','Fair','Good'],ordered=True)
    #df['health'] = df['health'].astype(health_categories)
    
    #Update steward categories
    #steward_categories = pd.api.types.CategoricalDtype(categories=['None','1or2','3or4','4orMore'],ordered=True)
    #df['steward'] = df['steward'].astype(steward_categories)
    
    return df

trees = GetTreeData()

# Update health categories
trees['healthcat'] = pd.Categorical(trees['health'], categories = ['Poor','Fair','Good'], ordered = True)

# Update steward categories
trees['stewardcat'] = pd.Categorical(trees['steward'], categories = ['None','1or2','3or4','4orMore'], ordered = True)


#%%
treelist = np.sort(trees['spc_common'].unique())
borolist = np.sort(trees['boroname'].unique())
#%%

#%%
app = Dash(__name__)
server = app.server

treeDropdown = dcc.Dropdown(options = [{'label':i, 'value':i} for i in treelist], value = treelist[2])
boroGraph = dcc.Graph(figure={})
stewardGraph = dcc.Graph(figure={})

app.layout = html.Div([
    dcc.Markdown('### NYC Street Tree Health'),
    treeDropdown,
    boroGraph,
    stewardGraph
])

@app.callback(
    Output(boroGraph,'figure'),
    Output(stewardGraph,'figure'),
    Input(treeDropdown,'value')
)

def update_output(treename):
    borodf = trees[trees['spc_common'] == treename].groupby(['boroname','healthcat']).size().reset_index(name='treecount')
    borodf['treepct'] = 100 * borodf['treecount'] / borodf.groupby('boroname')['treecount'].transform('sum')
    borofigure = px.bar(borodf, x = 'boroname', y = 'treepct', color = 'healthcat', barmode = 'stack', title = treename + ': Health percentage by borough', labels = dict(boroname='Borough', treepct='Health Percentage', healthcat='Health'))

    stewarddf = trees[trees['spc_common'] == treename].groupby(['stewardcat','healthcat']).size().reset_index(name='treecount')
    stewarddf['treepct'] = 100 * stewarddf['treecount'] / stewarddf.groupby('stewardcat')['treecount'].transform('sum')
    stewardfigure = px.bar(stewarddf, x = 'stewardcat', y = 'treepct', color = 'healthcat', barmode = 'stack', title = treename + ': Health percentage by stewardship', labels = dict(stewardcat='Stewardship', treepct='Health Percentage', healthcat='Health'))

    return borofigure, stewardfigure


#%%

#%%


#%%

#%%
if __name__ == '__main__':
    app.run_server()

#%%
