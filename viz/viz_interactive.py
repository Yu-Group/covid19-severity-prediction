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

red = '179,74,71'
blue = '111,136,190'
credstr ='rgb(' + red + ')'
cbluestr = 'rgb(' + blue + ')'
fill_strings = ['rgba(' + red + ',0.4)','rgba(' + blue + ',0.4)']
color_strings=[credstr,cbluestr]
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

def viz_curves_all_counties(df, filename, date1, date2, keys_curves = ['deaths','cases']):
    '''Visualize explanation for all features (table + ICE curves) 
    and save to filename
    
    Params
    ------
    df: table of data
    
    '''
    def make_plot(pre1, pre2, keys, title, show_interval, js):
        newdates = [date1[-1] + timedelta(days =i) for i in range(0,8)]
        fig = make_subplots(rows=1, cols=2, specs=[[{"secondary_y": True},{"secondary_y": True}]],
            subplot_titles=("Time series with 7 day prediction","Time series with historical prediction(7 day)"))

        def cal_coverage(row,date1,date2,keys):
            def cal(key, key_inv):
                dic_real = {}
                dic_pre = {}
                for i in range(len(date1)):
                    dic_real[date1[i]] = row[key][i]
                for i in range(len(date2)):
                    dic_pre[date2[i]] = row[key_inv][i]
                hit = miss = 0
                for d in dic_pre.keys():
                    if d in dic_real:
                        if dic_real[d] >= round(dic_pre[d][0],0) and dic_real[d] <= round(dic_pre[d][1],0):
                            hit += 1
                        else:
                            miss += 1
                return (hit/(hit+miss+1e-5))
            return [cal(key, 'pred_7day_' + key + '_interval') for key in keys]
        def make_traces(fig, row, pre, date1, date2, r, c, width,show_lengend,keys_curves):
            for j, key_curve in enumerate(keys_curves):
                curve = row[key_curve]
                traces = []
                traces.append(go.Scatter(x=date1,
                    y=curve,
                    showlegend=show_lengend,
                    visible=True, #key == key0,# False, #key == key0,
                    name=key_curve,
                    line=dict(color=color_strings[j], width=width))        )
                low = np.hstack((curve[-1],[x[0] for x in row[pre + key_curve + '_interval']]))
                curve_pre = np.hstack((curve[-1],row[pre + key_curve]))

                up = np.hstack((curve[-1],[x[1] for x in row[pre + key_curve + '_interval']]))
                if not(show_interval):
                    low = curve_pre
                    up = curve_pre
                if pre == pre1:
                    low = low[1:]
                    up = up[1:]
                    curve_pre = curve_pre[1:]
                traces.append(go.Scatter(
                    name = 'Upper Bound',
                    showlegend= False,
                    x = date2,
                    y = up,
                    marker = dict(size = 0),
                    line=dict(dash ='solid',color=fill_strings[j], width = 0)))
                traces.append(go.Scatter(x= date2,
                    y=curve_pre,
                    name = key_curve +' prediction',
                    showlegend= show_lengend,
                    mode = 'lines',
                    line=dict(dash ='dash',color = color_strings[j], width = width),
                    fillcolor = fill_strings[j],
                    fill ='tonexty'))
                traces.append(go.Scatter(
                    name = 'Lower Bound',
                    showlegend= False,
                    marker = dict(size = 0),
                    x = date2,
                    y = low,
                    fill ='tonexty',
                    fillcolor = fill_strings[j],
                    line=dict(dash ='solid',color = fill_strings[j], width = 0)))
                for trace in traces:
                    fig.add_trace(trace, secondary_y = "deaths" in key_curve, row = r,col = c)
            return fig
        fig = make_traces(fig, row,'pred_7day_',date1,date2,1,2,3,False, keys)
        newdates = [date1[-1] + timedelta(days = i) for i in range(0,8)]

        fig = make_traces(fig, row,'pred_',date1,newdates,1,1,4,True, keys)            
        for i in fig['layout']['annotations']:
            i['font'] = dict(size=15,color='white')  

        deaths_cov,cases_cov = cal_coverage(row,date1,date2, keys)
    # Update the margins to add a title and see graph x-labels.
        fig.layout.update(margin = {'t':120,'b':120})
        if title:        
            fig.layout.update(
                title = dict(text = county+', '+state+ '<br>' + 'FIPS:'+row['countyFIPS'], 
                    y = 0.92,
                    x = 0.03, 
                    yanchor = 'top'),
                legend=dict(x=0.25, y=1.2),
                legend_orientation="h")
        else:
            fig.layout.update(
                legend=dict(x=0.15, y=1.2),
                legend_orientation="h")
        fig.layout.update(
            width=1000,height=600,
            font=dict(size=12))
        if show_interval:
            fig.add_annotation(dict(font=dict(color="white",size=11),
                            x=0.85,
                            y=0.9,
                            showarrow=False,
                            text='Cases Prediction coverage: '+str(round(cases_cov, 2))+'<br>'
                                '  Deaths Prediction coverage: '+str(round(deaths_cov, 2)),
                            textangle=0,
                            xref="paper",
                            yref="paper"
                           ))
## Set plot1 axes properties
        y1 = max([x[1] for x in row[pre2+keys[1]+'_interval']])
        if not(show_interval):
            y1 = 0
        y1 = max(y1, max(row[keys[1]]))
        y2 = max([x[1] for x in row[pre2+keys[0]+'_interval']])
        if not (show_interval):
            y2 = 0
        y2 = max(y2, max(row[keys[0]]))
        dic = {'cases':'Cumulative Cases','deaths':'Cumulative Deaths','new_cases':'New cases','new_deaths':'New deaths'}
        fig.update_xaxes(title_text="Date",range=[datetime(2020, 4, 18), newdates[-1]],domain = [0,0.4],row=1, col=1)
        fig.update_yaxes(title_text=dic[keys[1]], color=cbluestr,rangemode = 'tozero',
            dtick = y1/5,range=[0,y1], domain=[0,0.95],row=1, col=1)  
        fig.update_yaxes(title_text=dic[keys[0]],showgrid=False,rangemode = 'tozero',color=credstr,
            dtick = round(y2*1.3/5), range=[0,y2*1.3], secondary_y=True, row=1,col=1)
        ## Set plot2 axes properties
        fig.update_xaxes(title_text="Date",range=[date2[-1], date2[7]],domain = [0.57,0.97], row=1, col=2)
        fig.update_yaxes(title_text=dic[keys[1]], color=cbluestr,rangemode = 'tozero',
            dtick = y1/5,range=[0,y1], domain=[0,0.95],row=1, col=2)  
        fig.update_yaxes(title_text=dic[keys[0]],rangemode = 'tozero',color=credstr,
            dtick = round(y2*1.3/5), showgrid=False,range=[0,y2*1.3], secondary_y=True, row=1,col=2)
        fig.layout.template = 'plotly_dark'
        return plotly.offline.plot(fig, 
                include_plotlyjs= js, output_type='div')
           
    for i in range(df.shape[0]):
        row = df.iloc[i]
        state,county,FIPS = row['State'],row['County']+" County",row['countyFIPS']
        if state == 'Alaska':
            county = row['County']+" Borough"
        if state == 'Louisiana':
            county = row['County'] + " Parish"
        if county == "De Kalb":
            county = "DeKalb"
        filename1 = filename + state+'_'+county+'.html'
        c1 = make_plot('pred_7day_','pred_',['deaths','cases'], True, True, "https://cdnjs.cloudflare.com/ajax/libs/plotly.js/1.54.6/plotly-basic.min.js")
        c2 = make_plot('pred_7day_','pred_',['new_deaths','new_cases'], False, False, False)
        f = open(filename1,"w+")
        f.write(c1+c2)

            

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
