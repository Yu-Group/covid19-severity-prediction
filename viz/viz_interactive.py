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

credstr ='rgb(234, 51, 86)'
cbluestr = 'rgb(57, 138, 242)'

def plot_counties(df, variable_to_distribute, variables_to_display, state=None, logcolor=False):
    """Plots the distribution of a given variable across the given sttate
    
    Params
    ------
    df
        df is a data frame containing the county level data
    variable_to_distribute
        variable_to_distribute is the variable that you want to see across the state
    variables_to_display
        Variables to display on hovering over each county
    
    output: Bokeh plotting object
    """
    from bokeh.sampledata.us_counties import data as counties
    
    counties = {
        code: county for code, county in counties.items()
        if county["state"] == state.lower()
    }

    county_xs = [county["lons"] for county in counties.values()]
    county_ys = [county["lats"] for county in counties.values()]
    
    if variable_to_distribute in variables_to_display:
        variables_to_display.remove(variable_to_distribute)

    colors = palettes.RdBu11 #(n_colors)
    min_value = df[variable_to_distribute].min()
    max_value = df[variable_to_distribute].max()
    gran = (max_value - min_value) / float(len(colors))
    #print variable_to_distribute,state,min_value,max_value
    index_range = [min_value + x*gran for x in range(len(colors))]
    county_colors = []
    variable_dictionary = {}
    variable_dictionary["county_names"] = [county['name'] for county in counties.values()]
    variable_dictionary["x"] = county_xs
    variable_dictionary["y"] = county_ys
    variable_dictionary[re.sub("[^\w]","",variable_to_distribute)] = []
    for vd in variables_to_display:
        variable_dictionary[re.sub("[^\w]","",vd)] = []
    for county_id in counties:
        StateCountyID = str(county_id[0]).zfill(2) + str(county_id[1]).zfill(3)
        if StateCountyID in list(df["Header-FIPSStandCtyCode"].values):
            temp_var = df[df["Header-FIPSStandCtyCode"] == StateCountyID][variable_to_distribute].values[0]
#             if temp_var > 0.0:
            variable_dictionary[re.sub("[^\w]","",variable_to_distribute)].append(temp_var)
            for vd in variables_to_display:
                variable_dictionary[re.sub("[^\w]","",vd)].append(round(float(df[df["Header-FIPSStandCtyCode"] == StateCountyID][vd].values),2))
            color_idx = list(temp_var - np.array(index_range)).index(min(x for x in list(temp_var - np.array(index_range)) if x >= 0))
            county_colors.append(colors[color_idx])

            '''
            else:
                variable_dictionary[re.sub("[^\w]","",variable_to_distribute)].append(0.0)
                county_colors.append("#A9A9A9")
                for vd in variables_to_display:
                    variable_dictionary[re.sub("[^\w]","",vd)].append(0.0)
            '''
        else:
            variable_dictionary[re.sub("[^\w]","",variable_to_distribute)].append(0.0)
            county_colors.append("#A9A9A9")
            for vd in variables_to_display:
                variable_dictionary[re.sub("[^\w]","",vd)].append(0.0)
        #print temp_var,counties[county_id]["name"]
    variable_dictionary["color"] = county_colors
    source = ColumnDataSource(data = variable_dictionary)
    TOOLS = "pan,wheel_zoom,box_zoom,reset,hover,save"

    if logcolor:
        mapper = LogColorMapper(palette=colors, low=min_value, high=max_value)
    else:
        mapper = LinearColorMapper(palette=colors, low=min_value, high=max_value)

    color_bar = ColorBar(color_mapper=mapper, location=(0, 0), orientation='horizontal', 
                     title = variable_to_distribute,ticker=FixedTicker(ticks=index_range))

    p = figure(title=variable_to_distribute, toolbar_location="left",tools=TOOLS,
        plot_width=1100, plot_height=700,x_axis_location=None, y_axis_location=None)

    p.patches('x', 'y', source=source, fill_alpha=0.7,fill_color='color',
        line_color="#884444", line_width=2)

    hover = p.select_one(HoverTool)
    hover.point_policy = "follow_mouse"
    tool_tips = [("County ", "@county_names")]
    for key in variable_dictionary.keys():
        if key not in ["x","y","color","county_names"]:
            tool_tips.append((key,"@"+re.sub("[^\w]","",key) + "{1.11}"))
    hover.tooltips = tool_tips
    
    p.add_layout(color_bar, 'below')
    
    return p


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


def make_counties_slider_subplots(title_text, subplot_titles, curves=False):
    if curves:
        column_widths = [0.15, .15, 0.7]
    else:
        column_widths = [0, 0, 1]
    fig = make_subplots(
        rows=3, cols=3, column_widths=column_widths,
        specs=[ # indices of outer list correspond to rows
            [ # indices of inner list to cols
                {"type" : 'scatter'}, {"type" : 'scatter'}, {"type" : 'scattergeo', 'rowspan' : 3}
            ], # row 1
            [
                {"type" : 'scatter'}, {"type" : 'scatter'}, None # row 2
            ], # row 2
            [
                {"type" : 'scatter'}, {"type" : 'scatter'}, None # row 2
            ] # row 3
        ],
        subplot_titles=subplot_titles
    )

    fig.update_geos(
        scope = 'usa',
        projection=go.layout.geo.Projection(type = 'albers usa'),
        subunitcolor = "rgb(0, 0, 0)",
        landcolor = 'rgb(255, 255, 255)'
    )

    fig.update_layout(
        dragmode = 'pan',
        title = {
            'text' : title_text,
            'pad' : {'b': 25},
            'y' : 0.95,
            'x' : 0.18,
            'xanchor': 'center',
            'yanchor': 'bottom'
        }
    )

    return fig


def add_counties_slider_scatter_traces(fig, df,
                                       key_toggle='CountyName',
                                       keys_curves=['deaths', 'cases'],
                                       decimal_places=0,
                                       expl_dict=None, interval_dicts=None,
                                       point_id=None, show_stds=False, ):
        '''
        Plot the top 6 counties with the most deaths.
        '''
        color_strings = [credstr, cbluestr]

        # scatter plots
        num_traces_per_plot = len(keys_curves)
        # for i in range(df.shape[0]):
        for i in range(6):
            row = df.iloc[i]
            key = row[key_toggle]

            for j, key_curve in enumerate(keys_curves):
                curve = row[key_curve]
                x = np.arange(curve.size)
                fig.add_trace(
                    go.Scatter(x=x,
                               y=curve,
                               showlegend=False,
                               visible=True,
                               name=key_curve,
                               line=dict(color=color_strings[j], width=4),
                               xaxis='x1', yaxis='y1'),
                    row=i % 3 + 1, col=(i - 1) % 2 + 1
                )
                # fig.update_layout(yaxis_type="log")
                # annotations.append(
                #     {
                #         'x' : .05,
                #         'y' : 0,
                #         'text' : key + ' County, ' + row['StateNameAbbreviation'],
                #         'visible' : i==0
                #     }
                # )

                # fig.layout['hovermode'] = annotations

        return None


def add_counties_slider_choropleth_traces(fig, df, past_days, target_days, scale_max, counties_json):
    def make_choropleth_trace(values, fips):
        choropleth_trace = go.Choropleth(
            visible=False,
            colorscale=color_scl,
            z=values,
            geojson=counties_json,
            locations=fips,
            zmin=0,
            zmax=scale_max,
            hoverinfo='skip',
            name="Choropleth Plot"
        )
        return choropleth_trace

    color_scl = [[0.0, '#ffffff'],[0.2, '#ff9999'],[0.4, '#ff4d4d'],
                 [0.6, '#ff1a1a'],[0.8, '#cc0000'],[1.0, '#4d0000']] # reds

    # add past days
    for col in past_days:
        values = df[col]
        fips = df['SecondaryEntityOfFile']

        # TODO: add new deaths

        choropleth_trace = make_choropleth_trace(values, fips)
        fig.add_trace(choropleth_trace, row=1, col=3)

    for i in range(target_days.size):

        #df['new_deaths'] = (preds - tot_deaths).apply(
        #    lambda x: np.array(
        #        [x[i] - x[i - 1] if i > 0 else x[i] for i in range(target_days.size)]
        #    )
        #)

        pred_col = f'Predicted Deaths {i+1}-day'
        values = df[pred_col]
        val_idx = values < 10000
        values = values[val_idx]
        fips = df['SecondaryEntityOfFile'][val_idx]

        choropleth_trace = make_choropleth_trace(values, fips)
        fig.add_trace(choropleth_trace, row=1, col=3)

    return None


def add_counties_slider_bubble_traces(fig, df, past_days, target_days, scale_max, plot_choropleth):
    def make_bubble_trace(values, fips, lat, lon, text):
        bubble_trace = go.Scattergeo(
            visible=False,
            lon=lon,
            lat=lat,
            text=text,
            hovertemplate='%{text}',
            name="Bubble Plot",
            marker = dict(
                size = values,
                sizeref = 0.5*(100/scale_max), # make bubble slightly larger
                color = values,
                colorscale = color_scl,
                cmin=0,
                cmax=scale_max,
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode='area',
                showscale=not plot_choropleth
            )
        )
        return bubble_trace

    color_scl = [[0.0, '#ffffff'],[0.2, '#ff9999'],[0.4, '#ff4d4d'],
                 [0.6, '#ff1a1a'],[0.8, '#cc0000'],[1.0, '#4d0000']] # reds

    # add past days
    for col in past_days:
        values = df[col]
        fips = df['SecondaryEntityOfFile']
        lon = df['lon']
        lat = df['lat']
        text = '<b>Actual # of Deaths</b>: ' + values.round(2).astype(str) + '<br>' + \
            df['text'].tolist()

        # TODO: add new deaths

        bubble_trace = make_bubble_trace(values, fips, lat, lon, text)
        fig.add_trace(bubble_trace, row=1, col=3)

    # add predictions
    for i in range(target_days.size):

        #df['new_deaths'] = (preds - tot_deaths).apply(
        #    lambda x: np.array(
        #        [x[i] - x[i - 1] if i > 0 else x[i] for i in range(target_days.size)]
        #    )
        #)

        pred_col = f'Predicted Deaths {i+1}-day'
        values = df[pred_col].round()
        val_idx = values < 10000
        values = values[val_idx]
        fips = df['SecondaryEntityOfFile'][val_idx]
        lon = df['lon'][val_idx]
        lat = df['lat'][val_idx]
        text = '<b>Deaths Predicted</b>: ' + values.round(2).astype(str) + '<br>' + \
            df['text'][val_idx].tolist()

        # day_name = "Day " + str(target_days[i])
        # TODO: add new deaths

        bubble_trace = make_bubble_trace(values, fips, lat, lon, text)
        fig.add_trace(bubble_trace, row=1, col=3)

    return None


def make_counties_slider_sliders(past_days, target_days, plot_choropleth, curves=False):
    sliders = [
        {
            "active": 0,
            "visible": True,
            "pad": {"t": 50},
            "currentvalue": {'xanchor' : 'right'},
            'transition': {'duration': 1000, 'easing': 'cubic-in-out'},
            "steps": [],
        }
    ]

    days = list(map(lambda x: x.replace('#Deaths_', ''), past_days))
    num_days = len(days) + target_days.size

    # add steps for past days
    for i, day in enumerate(days):
        if plot_choropleth:
            args = ["visible", [False] * (2*num_days) + [curves] * 12]
        else:
            args = ["visible", [False] * num_days + [curves] * 12]
        slider_step = {
            # the first falses are the map traces
            # the last 12 trues are the scatter traces
            "args": args,
            "label": day,
            "method": "restyle"
        }
        slider_step['args'][1][i] = True # Toggle i'th trace to "visible"
        if plot_choropleth:
            slider_step['args'][1][num_days + i] = True # and the other trace
        sliders[0]['steps'].append(slider_step)

    # add steps for predicted days
    for i in range(target_days.size):
        if i == 0:
            day_name = "Today"
        elif i == 1:
            day_name = "Tomorrow"
        else:
            day_name = "In " + str(i + 1) + " Days"
        if plot_choropleth:
            args = ["visible", [False] * (2*num_days) + [curves] * 12]
        else:
            args = ["visible", [False] * num_days + [curves] * 12]
        slider_step = {
            "args": args,
            "label": day_name,
            "method": "restyle"
        }
        slider_step['args'][1][len(days) + i] = True
        if plot_choropleth:
            slider_step['args'][1][num_days + len(days) + i] = True
        sliders[0]['steps'].append(slider_step)

    return sliders


def plot_counties_slider(df,
                         target_days=np.array([1, 2, 3]),
                         filename="results/deaths.html",
                         cumulative=True, # not currently used
                         plot_choropleth=False,
                         counties_json=None,
                         n_past_days=3,
                         dark=True,
                         curves=True,
                         auto_open=True):
    """
    """
    # TODO: note that df should have all data (preds and lat lon)
    # TODO: add previous days
    fips = df['SecondaryEntityOfFile'].tolist()
    tot_deaths = df['tot_deaths']

    df['text'] = 'State: ' + df['StateName'] + \
        ' (' + df['StateNameAbbreviation'] + ')' + '<br>' + \
        'County: ' + df['CountyName'] + '<br>' + \
        'Population (2018): ' + df['PopulationEstimate2018'].astype(str) + '<br>' + \
        '# Recorded Cases: ' + df['tot_cases'].astype(str) + '<br>' + \
        '# Recorded Deaths: ' + tot_deaths.astype(str) + '<br>' + \
        '# Hospitals: ' + df['#Hospitals'].astype(str)

    # compute scale_max for plotting colors
    pred_col = f'Predicted Deaths {target_days[-1]}-day'
    values = df[pred_col]
    val_idx = values < 10000
    values = values[val_idx]
    scale_max = values.quantile(.995)

    # if not cumulative:
    #     df['new_deaths'] = (preds - tot_deaths).apply(
    #        lambda x: np.array(
    #            [x[i] - x[i - 1] if i > 0 else x[i] for i in range(target_days.size)]
    #        )
    #     )
    #     title_text='Predicted New COVID-19 Deaths Over the Next '+ str(target_days.size) + ' Days'
    # else:
    #     title_text='Predicted Cumulative COVID-19 Deaths Over the Next '+ str(target_days.size) + ' Days'

    # TODO: use new_deaths
    map_title='Predicted Cumulative COVID-19 Deaths Over the Next '+ str(target_days.size) + ' Days'

    if curves:
        # compute normalized growth rate:
        # avg(growth = # deaths day i / # deaths day i-1) + cov(time, growth)
        # and penalizes areas where growth is slowing
        def compute_growth_factor(x, n_days=4):
            past_n_days = x[-n_days:]
            growth_factor = (past_n_days / np.insert(x[-4:-1], 0, 1))[-(n_days-1):]
            return np.mean(growth_factor) + np.cov(np.arange(3), growth_factor)[0][1]

        # the emerging_index scales by log(pop_density) * median_age / (# hospitals + 1)
        df['emerging_index'] = df['deaths'].apply(lambda x: compute_growth_factor(x)) * \
            (np.log(df['PopulationDensityperSqMile2010']) * df['MedianAge2010'] / (df['#Hospitals'] + 1))

        df_top_6 = df.sort_values('emerging_index', ascending = False)
        df_top_6 = df_top_6[(df_top_6['tot_deaths'] > 20) & (df_top_6['tot_deaths'] < 50)]

        top_6_county = df_top_6['CountyName'].take(range(6)).tolist()
        top_6_state = df_top_6['StateNameAbbreviation'].take(range(6)).tolist()
        top_6 = [county + ', ' + state for (county, state) in zip(top_6_county, top_6_state)]
        subplot_titles = top_6[0:2] + [title_text] + top_6[2:4] + top_6[4:]

        title = "Emerging Hotspots (20 to 50 Deaths) <br> Avg. Growth in Death Rate Weighted by<br> log Pop. Density * Median Age / (# Hospitals + 1)"
    else:
        title = ""
        subplot_titles = ["", "", map_title]

    # make main figure
    fig = make_counties_slider_subplots(title, subplot_titles, curves)

    # get names of columns with past 3 days' deaths
    past_days = df.filter(regex='#Deaths_').columns[-n_past_days:]

    # make choropleth if plotting
    # want this to happen first so bubbles overlay
    if plot_choropleth:
        add_counties_slider_choropleth_traces(
            fig, df, past_days, target_days, scale_max, counties_json
        )

    # add Scattergeo
    add_counties_slider_bubble_traces(fig, df, past_days, target_days, scale_max, plot_choropleth)

    # make first day visible
    fig.data[0].visible = True
    if plot_choropleth:
        # make bubbles visible
        fig.data[n_past_days + target_days.size].visible = True

    if curves:
        # add case and death curves
        add_counties_slider_scatter_traces(fig, df)

    # add slider to layout
    sliders = make_counties_slider_sliders(past_days, target_days, plot_choropleth, curves)
    fig.update_layout(
        sliders=sliders
    )

    if dark:
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,255)',
            plot_bgcolor='rgba(0,0,0,255)',
            template='plotly_dark'
        )

    plot(fig, filename=filename, config={
        'showLink': False,
        'showSendToCloud': False,
        'sendData': True,
        'responsive': True,
        'autosizable': True,
        'displaylogo': False
    }, auto_open = False)

    
    
'''Interactive plots for counties/hospitals'''

'''
fig = px.scatter(df, x="tot_deaths", y="Predicted Deaths 3-day", log_x=True, log_y=True,
                 hover_name="CountyName", hover_data=["CountyName", 'StateName'])
plotly.offline.plot(fig, filename="results/pred_deaths_vs_curr_deaths.html")

fig = px.scatter(df, x="tot_deaths", y="Predicted New Deaths 3-day", log_x=True, log_y=True,
                 hover_name="CountyName", hover_data=["CountyName", 'StateName'])
plotly.offline.plot(fig, filename="results/new_deaths_vs_curr_deaths.html")
'''


def viz_index_animated(d, NUM_DAYS_LIST, out_name="results/hospital_index_animated.html"):
    def flat_list(list_list):
        l = []
        for ll in list_list:
            l += ll.tolist()
        return l

    N = d.shape[0]
    NUM_DAYS = len(NUM_DAYS_LIST)
    dd = pd.concat([d] * NUM_DAYS)
    dd['Days'] = np.repeat(range(NUM_DAYS), N) + 1
    dd['Predicted New Deaths'] = flat_list([d[f"Predicted New Deaths Hospital {i}-day"].values for i in range(1, NUM_DAYS + 1)])
    dd['Severity Index'] = flat_list([d[f"Severity Index {i}-day"].values for i in range(1, NUM_DAYS + 1)])
    
    fig = px.scatter(dd, x="Total Deaths Hospital", 
                 y="Predicted New Deaths", 
                 animation_frame="Days", 
                 animation_group="Hospital Name",
                 color='Severity Index',
                 size='Hospital Employees',
                 hover_name="Hospital Name", 
                 hover_data=["CountyName", 'StateName'],
                 log_x=True, log_y=True)
    fig.add_annotation(text='Circle size corresponds to hospital size', 
                       x=max(dd['Total Deaths Hospital']),
                       y=max(dd['Predicted New Deaths']))
    fig.update_layout(
                paper_bgcolor='rgba(0,0,0,255)',
                plot_bgcolor='rgba(0,0,0,255)',
                template='plotly_dark'
            )
    plotly.offline.plot(fig, filename=out_name)
