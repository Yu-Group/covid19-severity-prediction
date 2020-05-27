from bokeh.sampledata import us_states, us_counties
from bokeh.plotting import figure, show, output_notebook, output_file, save
from bokeh import palettes
from bokeh.models import ColorBar,HoverTool,LinearColorMapper,ColumnDataSource,FixedTicker, LogColorMapper
output_notebook()
import re
import numpy as np
from modeling import fit_and_predict
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.offline import plot
from plotly.subplots import make_subplots
import json
import plotly.express as px
import plotly
import pandas as pd
from datetime import datetime, timedelta

credstr ='rgb(234, 51, 86)'
cbluestr = 'rgb(57, 138, 242)'

def viz_curves(df, filename='out.html', 
               key_toggle='CountyName',
               keys_table=['CountyName', 'StateName'], 
               keys_curves=['deaths', 'cases'],
               dropdown_suffix=' County',
               decimal_places=0,
               expl_dict=None, interval_dicts=None, 
               point_id=None, show_stds=False, ):
        '''Visualize explanation for all features (table + ICE curves) 
        and save to filename
        
        Params
        ------
        df: table of data
        
        '''
        color_strings = [credstr, cbluestr]

        
        # plot the table
        df_tab = df[keys_table]
        fig = ff.create_table(df_tab.round(decimal_places))
        
        # scatter plots
        traces = []
        num_traces_per_plot = len(keys_curves)
        key0 = df_tab[key_toggle].values[0] # only want this to be visible
        for i in range(df.shape[0]):
            row = df.iloc[i]
            key = row[key_toggle]
            
            for j, key_curve in enumerate(keys_curves):
                curve = row[key_curve]
                x = np.arange(curve.size)
                traces.append(go.Scatter(x=x,
                    y=curve,
                    showlegend=False,
                    visible=i==0, #key == key0,# False, #key == key0,
                    name=key_curve,
                    line=dict(color=color_strings[j], width=4),
                    xaxis='x2', yaxis='y2')
                )
                
        fig.add_traces(traces)
        
        # add buttons to toggle visibility
        buttons = []
        for i, key in enumerate(df[key_toggle].values):
            table_offset = 1
            visible = np.array([True] * table_offset + [False] * num_traces_per_plot * len(df[key_toggle]))
            visible[num_traces_per_plot * i + table_offset: num_traces_per_plot * (i + 1) + table_offset] = True            
            buttons.append(
                dict(
                    method='restyle',
                    args=[{'visible': visible}],
                    label=key + dropdown_suffix
                ))

        # initialize xaxis2 and yaxis2
        fig['layout']['xaxis2'] = {}
        fig['layout']['yaxis2'] = {}
        
        
        fig.layout.updatemenus = [go.layout.Updatemenu(
            dict(
                active=int(np.argmax(df[key_toggle].values == key0)),
                buttons=buttons,
                x=0.8, # this is fraction of entire screen
                y=1.05,
                direction='down'
            )
        )]
        
        # Edit layout for subplots
        fig.layout.xaxis.update({'domain': [0, .5]})
        fig.layout.xaxis2.update({'domain': [0.6, 1.]})
        fig.layout.xaxis2.update({'title': 'Time'})
        
        # The graph's yaxis MUST BE anchored to the graph's xaxis
        fig.layout.yaxis.update({'domain': [0, .9]})
        fig.layout.yaxis2.update({'domain': [0, .9], 'anchor': 'x2', })
        fig.layout.yaxis2.update({'title': 'Count'})

        # Update the margins to add a title and see graph x-labels.
        fig.layout.margin.update({'t':50, 'b':120})
        

        fig.layout.update({
            'title': 'County-level outbreaks',
            'height': 800
        })

        # fig.layout.template = 'plotly_dark'
        plot(fig, filename=filename, config={'showLink': False, 
                                             'showSendToCloud': False,
                                             'sendData': True,
                                             'responsive': True,
                                             'autosizable': True,
                                             'displaylogo': False
                                            }) 
#         fig.show()
        print('plot saved to', filename)




'''Interactive plots for counties/hospitals'''

'''
fig = px.scatter(df, x="tot_deaths", y="Predicted Deaths 3-day", log_x=True, log_y=True,
                 hover_name="CountyName", hover_data=["CountyName", 'StateName'])
plotly.offline.plot(fig, filename="results/pred_deaths_vs_curr_deaths.html")

fig = px.scatter(df, x="tot_deaths", y="Predicted New Deaths 3-day", log_x=True, log_y=True,
                 hover_name="CountyName", hover_data=["CountyName", 'StateName'])
plotly.offline.plot(fig, filename="results/new_deaths_vs_curr_deaths.html")
'''


def viz_index_animated(d, NUM_DAYS_LIST, by_size=False,
                       x_key='Total Deaths Hospital', # Hospital Employees
                       y_key='Predicted new deaths at hospital', # 'Predicted (cumulative) deaths at hospital'
                       hue='Severity Index', # 'Surge Index'
                       out_name="results/hospital_index_animated.html"):
    '''
    by_size: bool
        If False, make the plot of new deaths vs current deaths
        If true, make the plot of tot deaths vs hosp size
    '''
    def flat_list(list_list):
        l = []
        for ll in list_list:
            l += ll.tolist()
        return l

    N = d.shape[0]
    NUM_DAYS = len(NUM_DAYS_LIST)
    dd = pd.concat([d] * NUM_DAYS)
    # days_past = [(datetime.now() + timedelta(days=i)).strftime("%B %d") for i in NUM_DAYS_LIST]
    dd['Days in the future'] = np.repeat(NUM_DAYS_LIST, N)
    dd['Predicted new deaths at hospital'] = flat_list([d[f"Predicted New Deaths Hospital {i}-day"].values for i in NUM_DAYS_LIST])
    dd['Predicted (cumulative) deaths at hospital'] = flat_list([d[f"Predicted Deaths Hospital {i}-day"].values for i in NUM_DAYS_LIST])
    dd['Severity Index'] = flat_list([d[f"Severity Index {i}-day"].values for i in NUM_DAYS_LIST])
    dd['Surge Index'] = flat_list([d[f"Surge {i}-day"].values for i in NUM_DAYS_LIST])
    today = datetime.today().strftime("%B %d")
    todays_deaths_key = f'Total (estimated) deaths at hospital by {today}'
    dd = dd.rename(columns={'Total Deaths Hospital': todays_deaths_key})
    dd = dd[~np.isnan(dd['Hospital Employees'])]
    
    # decide x and y keys
    if x_key == 'Total Deaths Hospital':
        x_key = todays_deaths_key
    
    # make plot
    fig = px.scatter(dd, x=x_key, 
                 y=y_key, 
                 animation_frame="Days in the future", 
                 animation_group="Hospital Name",
                 color=hue,
                 size='Hospital Employees',
                 hover_name="Hospital Name", 
                 hover_data=["CountyName", 'StateName'],
                 log_x=True, log_y=True)
    fig.update_layout(
                paper_bgcolor='rgba(0,0,0,255)',
                plot_bgcolor='rgba(0,0,0,255)',
                template='plotly_dark'
            )
    plotly.offline.plot(fig, filename=out_name, auto_open=False)
