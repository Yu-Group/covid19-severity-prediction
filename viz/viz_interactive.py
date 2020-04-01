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
from urllib.request import urlopen
import json

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
                                             'showEditInChartStudio': False,
                                             'displaylogo': False
                                            }) 
#         fig.show()
        print('plot saved to', filename)


def plot_counties_slider(df,
                         methods: list=[fit_and_predict.exponential,
                                        fit_and_predict.shared_exponential,
                                        fit_and_predict.demographics],
                         target_days: np.ndarray=np.array([1, 2, 3, 4]),
                         filename: str="results/deaths.html",
                         cumulative: bool=True,
                         scale_max: int=100):

    with urlopen(
            'https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json'
    ) as response:
         counties = json.load(response)

    # get predictions
    df_preds = fit_and_predict.fit_and_predict_ensemble(
        df, outcome='deaths', methods=methods,
        mode='predict_future', target_day=target_days,
        output_key='predicted_deaths'
    )

    # filter out any rows with predictions over 10,000
    # TODO: fix upstream rather than filter here
    df_preds = df_preds[df_preds['predicted_deaths'].apply(lambda x: np.all(x < 1e4))]

    preds = df_preds['predicted_deaths']
    fips = df_preds['SecondaryEntityOfFile'].tolist()
    tot_deaths = df_preds['tot_deaths']

    if not cumulative:
        df_preds['new_deaths'] = (preds - tot_deaths).apply(
            lambda x: np.array(
                [x[i] - x[i - 1] if i > 0 else x[i] for i in range(target_days.size)]
            )
        )
        title_text='Predicted New COVID-19 Deaths Over the Next '+ str(target_days.size) + ' Days'
    else:
        title_text='Predicted Cumulative COVID-19 Deaths Over the Next '+ str(target_days.size) + ' Days'

    df_preds['text'] = 'State: ' + df_preds['StateName'] + \
        ' (' + df_preds['StateNameAbbreviation'] + ')' + '<br>' + \
        'County: ' + df_preds['CountyName'] + '<br>' + \
        'Total Cases: ' + df_preds['tot_cases'].astype(str) + '<br>' + \
        'Total Deaths: ' + tot_deaths.astype(str) + '<br>' + \
        'Population (2018): ' + df_preds['PopulationEstimate2018'].astype(str) + '<br>' + \
        '# Hospitals: ' + df_preds['#Hospitals'].astype(str)

    days = ["Day " + str(day) for day in target_days]

    color_scl = [[0.0, '#ffffff'],[0.2, '#ff9999'],[0.4, '#ff4d4d'],
                 [0.6, '#ff1a1a'],[0.8, '#cc0000'],[1.0, '#4d0000']] # reds

    # make figure
    fig_dict = {
        "data": [],
        "layout": {},
        "frames": []
    }

    # fill in most of layout
    fig_dict["layout"]["hovermode"] = "closest"
    # fig_dict["layout"]["sliders"] = {
    #     "args": [
    #         "transition", {
    #             "duration": 400,
    #             "easing": "cubic-in-out"
    #         }
    #     ],
    #     "initialValue": "Day 1",
    #     "plotlycommand": "animate",
    #     "values": days,
    #     "visible": True
    # }
    fig_dict["layout"]["updatemenus"] = [
        # TODO: couldn't get animations working correctly
        # {
        #     "buttons": [
        #         {
        #             "args": [[None], {"frame": {"duration": 500, "redraw": True},
        #                               "fromcurrent": True, "transition": {"duration": 2000,
        #                                                                   "easing": "quadratic-in-out"}}],
        #             "label": "Play",
        #             "method": "animate"
        #         },
        #         {
        #             "args": [None, {"frame": {"duration": 0, "redraw": True},
        #                             "mode": "immediate",
        #                             "transition": {"duration": 0}}],
        #             "label": "Pause",
        #             "method": "animate"
        #         }
        #     ],
        #     "direction": "left",
        #     "pad": {"r": 10, "t": 87},
        #     "showactive": False,
        #     "type": "buttons",
        #     "x": 0.1,
        #     "xanchor": "right",
        #     "y": 0,
        #     "yanchor": "top"
        # },
        # dict(
        #     active=0,
        #     buttons=list([
        #         dict(label="Heatmap",
        #              method="update",
        #              args=[{"visible": [True] + [False] * (2*target_days.size - 1)},
        #                    {"title": "Heatmap"}]),
        #         dict(label="Bubble Map",
        #              method="update",
        #              args=[{"visible": [False] * target_days.size + [True] + [False] * (target_days.size - 1)},
        #                    {"title": "Bubble Map"}])
        #     ]),
        #     direction="down",
        #     pad={"r": 10, "t": 10},
        #     showactive=True,
        #     x=0.1,
        #     xanchor="left",
        #     y=1.1,
        #     yanchor="top"
        # )

    ]

    sliders = [
        {
            "active": 0,
            "visible": True,
            "pad": {"t": 50},
            "steps": []
        },
        {
            "active": 0,
            "visible": False,
            "pad": {"t": 50},
            "steps": []
        }
    ]

    # add data for default view
    # values = preds.apply(lambda x: x[0])
    # choropleth_trace = go.Choropleth(
    #     colorscale=color_scl,
    #     z=values.tolist(),
    #     geojson=counties,
    #     locations=fips,
    #     zmin=0,
    #     zmax=scale_max,
    #     hovertemplate='<b>Deaths Predicted</b>: %{z:.2f}<br>'+'%{text}',
    #     text=text
    # )
    # fig_dict["data"].append(choropleth_trace)

    # # add frames
    # for i in range(target_days.size):

    #     day_name = "Day " + str(target_days[i])
    #     frame = {"data": [], "name": day_name}

    #     # TODO: add new deaths
    #     values = preds.apply(lambda x: x[i])

    #     choropleth_trace = go.Choropleth(
    #         colorscale=color_scl,
    #         z=values.tolist(),
    #         geojson=counties,
    #         locations=fips,
    #         zmin=0,
    #         zmax=scale_max,
    #         hovertemplate='<b>Deaths Predicted</b>: %{z:.2f}<br>'+'%{text}',
    #         text=text
    #     )
    #     frame["data"].append(choropleth_trace)
    #     fig_dict["frames"].append(frame)
    #     slider_step = {"args": [
    #         [day_name],
    #         {"frame": {"duration": 2000, "redraw": True},
    #          "mode": "immediate",
    #          "transition": {"duration": 2000}}
    #     ],
    #                    "label": day_name,
    #                    "method": "animate"}
    #     sliders_dict["steps"].append(slider_step)

    fig = go.Figure(fig_dict)

    # add traces for choropleth
    for i in range(target_days.size):

        day_name = "Day " + str(target_days[i])
        # TODO: add new deaths
        values = preds.apply(lambda x: x[i])

        text = '<b>Deaths Predicted</b>: ' + values.round(2).astype(str) + '<br>' + \
            df_preds['text'].tolist()

        choropleth_trace = go.Choropleth(
            visible=False,
            colorscale=color_scl,
            z=values.tolist(),
            geojson=counties,
            locations=fips,
            zmin=0,
            zmax=scale_max,
            hovertemplate='%{text}',
            text=text,
            name="Choropleth " + day_name
        )
        fig.add_trace(choropleth_trace)

        slider_step = {
            "args": ["visible", [False] * target_days.size],
            "label": day_name,
            "method": "restyle"
        }
        slider_step['args'][1][i] = True # Toggle i'th trace to "visible"
        sliders[0]["steps"].append(slider_step)

    # make first trace visible
    fig.data[0].visible = True

    # add traces for bubbleplot
    for i in range(target_days.size):

        day_name = "Day " + str(target_days[i])
        values = preds.apply(lambda x: x[i])

        text = '<b>Deaths Predicted</b>: ' + values.round(2).astype(str) + '<br>' + \
            df_preds['text'].tolist()

        bubble_trace = go.Scattergeo(
            visible=False,
            geojson=counties,
            lon=df['lon'],
            lat=df['lat'],
            hovertemplate='%{text}',
            text=text,
            name="Bubble " + day_name,
            marker = dict(
                size = values,
                sizeref = 0.5,
                # color = values.tolist(),
                cmin=0,
                cmax=scale_max,
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode = 'area'
            )
        )
        fig.add_trace(bubble_trace)

        slider_step = {
            "args": ["visible", [False] * target_days.size],
            "label": day_name,
            "method": "restyle"
        }
        slider_step['args'][1][i] = True # Toggle i'th trace to "visible"
        sliders[1]["steps"].append(slider_step)

    fig.data[target_days.size].visible = True

    fig.update_layout(
        title_text=title_text,
        geo = dict(
            scope='usa',
            projection=go.layout.geo.Projection(type = 'albers usa'),
            showlakes=False, # lakes
            lakecolor='rgb(255, 255, 255)'),
        sliders=sliders
    )

    # fig.show()

    plot(fig, filename=filename, config={
        'showLink': False,
        'showSendToCloud': False,
        'sendData': True,
        'responsive': True,
        'autosizable': True,
        'showEditInChartStudio': False,
        'displaylogo': False
    })
