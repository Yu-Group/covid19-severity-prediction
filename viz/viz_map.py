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


"""
Predicted death maps
"""
def make_us_map(title_text, dark=False):
    fig = go.Figure()

    fig.update_geos(
        scope = 'usa',
        projection=go.layout.geo.Projection(type = 'albers usa'),
        subunitcolor = "rgb(0, 0, 0)",
        landcolor = 'rgb(255, 255, 255)'
    )

    fig.update_layout(
        dragmode = 'pan',
        title = {'text' : title_text}
    )

    if dark:
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,255)',
            plot_bgcolor='rgba(0,0,0,255)',
            template='plotly_dark'
        )

    return fig


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
            colorbar_title = "<b> Deaths </b>"
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
        fig.add_trace(choropleth_trace)

    for i in range(target_days.size):

        #df['new_deaths'] = (preds - tot_deaths).apply(
        #    lambda x: np.array(
        #        [x[i] - x[i - 1] if i > 0 else x[i] for i in range(target_days.size)]
        #    )
        #)
        pred_col = f'Predicted Deaths {i+1}-day'
        values = df[pred_col]
        fips = df['SecondaryEntityOfFile']

        choropleth_trace = make_choropleth_trace(values, fips)
        fig.add_trace(choropleth_trace)

    return None


def add_counties_slider_bubble_traces(fig, df, past_days, target_days, scale_max, plot_choropleth):
    def make_bubble_trace(values, fips, lat, lon, text):
        bubble_trace = go.Scattergeo(
            visible=False,
            lat=lat,
            lon=lon,
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
                colorbar_title = "<b> Deaths </b>",
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
        lat = df['lat']
        lon = df['lon']
        text = '<b>Actual # of Deaths</b>: ' + values.round().astype(str) + '<br>' + \
            df['text'].tolist()

        # TODO: add new deaths

        bubble_trace = make_bubble_trace(values, fips, lat, lon, text)
        fig.add_trace(bubble_trace)

    # add predictions
    for i in range(target_days.size):

        #df['new_deaths'] = (preds - tot_deaths).apply(
        #    lambda x: np.array(
        #        [x[i] - x[i - 1] if i > 0 else x[i] for i in range(target_days.size)]
        #    )
        #)

        pred_col = f'Predicted Deaths {i+1}-day'
        values = df[pred_col].round()
        fips = df['SecondaryEntityOfFile']
        lat = df['lat']
        lon = df['lon']
        text = '<b>Deaths Predicted</b>: ' + values.round().astype(str) + '<br>' + \
            df['text'].tolist()

        # day_name = "Day " + str(target_days[i])
        # TODO: add new deaths

        bubble_trace = make_bubble_trace(values, fips, lat, lon, text)
        fig.add_trace(bubble_trace)

    return None


def make_counties_slider_sliders(past_days, target_days, plot_choropleth):
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
            args = ["visible", [False] * (2*num_days)]
        else:
            args = ["visible", [False] * num_days]
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
            day_name = "In " + str(i) + " Days"
        if plot_choropleth:
            args = ["visible", [False] * (2*num_days)]
        else:
            args = ["visible", [False] * num_days]
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
                         target_days=np.array([1, 2, 3, 4, 5]),
                         filename="results/deaths.html",
                         cumulative=True, # not currently used
                         plot_choropleth=False,
                         counties_json=None,
                         n_past_days=3,
                         dark=True,
                         auto_open=True):
    """
    """
    if plot_choropleth:
        assert counties_json is not None, 'counties_json must be included for plotting choropleth'
    # TODO: note that df should have all data (preds and lat lon)
    # TODO: add previous days
    fips = df['SecondaryEntityOfFile'].tolist()
    tot_deaths = df['tot_deaths']

    d = df
    d['text'] = 'State: ' + d['StateName'] + \
        ' (' + d['StateNameAbbreviation'] + ')' + '<br>' + \
        'County: ' + d['CountyName'] + '<br>' + \
        'Population (2018): ' + d['PopulationEstimate2018'].astype(str) + '<br>' + \
        '# Recorded Cases: ' + d['tot_cases'].astype(str) + '<br>' + \
        '# Recorded Deaths: ' + tot_deaths.astype(str) + '<br>' + \
        '# Hospitals: ' + d['#Hospitals'].astype(str)

    # compute scale_max for plotting colors
    pred_col = f'Predicted Deaths {target_days[-1]}-day'
    values = d[pred_col]
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

    # TODO: add new_deaths
    map_title='Predicted Cumulative COVID-19 Deaths Over the Next '+ str(target_days.size) + ' Days'

    # make main figure
    fig = make_us_map(map_title, dark)

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

    # add slider to layout
    sliders = make_counties_slider_sliders(past_days, target_days, plot_choropleth)
    fig.update_layout(
        sliders=sliders
    )

    plot(fig, filename=filename, config={
        'showLink': False,
        'showSendToCloud': False,
        'sendData': True,
        'responsive': True,
        'autosizable': True,
        'displaylogo': False
    }, auto_open = auto_open)


"""
Death curve scatter plot grid
"""
def make_scatter_plot_grid_subplot(title_text, subplot_titles):
    fig = make_subplots(
        rows=3, cols=3, column_widths=[0.2]*3,
        specs=[ # indices of outer list correspond to rows
            [ # indices of inner list to cols
                {"type" : 'scatter'}, {"type" : 'scatter'}, {"type" : 'scatter'}
            ], # row 1
            [
                {"type" : 'scatter'}, {"type" : 'scatter'}, {"type" : 'scatter'}
            ], # row 2
            [
                {"type" : 'scatter'}, {"type" : 'scatter'}, {"type" : 'scatter'}
            ] # row 3
        ],
        subplot_titles=subplot_titles
    )

    fig.update_layout(
        hovermode = 'x',
        dragmode = 'pan',
        title = {
            'text' : title_text,
            # 'pad' : {'b': 25},
            # 'y' : 0.95,
            # 'x' : 0.18,
            # 'xanchor': 'center',
            # 'yanchor': 'bottom'
        }
    )

    return fig


def add_scatter_traces_to_grid(fig, df,
                               key_toggle='CountyName',
                               keys_curves=['deaths', 'cases'],
                               decimal_places=0,
                               expl_dict=None, interval_dicts=None,
                               point_id=None, show_stds=False,
                               annotation_text=None,
                               annotation_x=None,
                               annotation_y=None):
        '''
        Add first 9 rows as scatter plot traces to a 3x3 grid.
        '''
        color_strings = [credstr, cbluestr]

        # scatter plots
        annotations = []

        for i in range(9):
            row = df.iloc[i]
            key = row[key_toggle]

            for j, key_curve in enumerate(keys_curves):
                curve = row[key_curve]
                x = np.arange(curve.size)
                fig.add_trace(
                    go.Scatter(
                        x=x,
                        y=curve,
                        showlegend=False,
                        visible=True,
                        name=key_curve,
                        line=dict(color=color_strings[j], width=4)
                    ),
                    row=i // 3 + 1, col=i % 3 + 1
                )
            if annotation_text is not None:
                if i==0:
                    xref='x'
                    yref='y'
                else:
                    xref='x'+str(i+1)
                    yref='y'+str(i+1)
                fig.add_annotation(
                        x=annotation_x[i],
                        y=annotation_y[i],
                        text=annotation_text[i],
                        xref=xref,
                        yref=yref,
                        showarrow=True,
                        arrowhead=7,
                        visible=True
                )

        return None


def plot_emerging_hotspots_grid(df,
                                target_days=[1,2,3],
                                n_days_past=3,
                                order_by='emerging_index',
                                filename='results/emerging_hotspots.html',
                                auto_open=True):
    """
    Plot observations and predictions for the first nine rows of df in a grid.
    """
    d = df.sort_values(order_by, ascending=False)

    counties = d['CountyName'].take(range(9)).tolist()
    states = d['StateNameAbbreviation'].take(range(9)).tolist()
    subplot_titles = [county + ', ' + state + ' (Hotspot Rank: ' +  str(rank + 1) + ')' for
                      (county, state, rank) in zip(counties, states, range(9))]


    # get col names of past obs, plus one more as the baseline
    past_cols = d.filter(regex='#Deaths_').columns[-(n_days_past):].tolist()
    # get col names of predictions
    pred_cols = [f'Predicted Deaths {day}-day' for day in target_days]

    past_days = list(map(lambda x: x.replace('#Deaths_', ''), past_cols))

    title = "Emerging Hotspots"

    d['deaths'] = d[past_cols + pred_cols].values.tolist()
    d['deaths'] = d['deaths'].apply(lambda x: np.around(np.array(x)))

    fig = make_scatter_plot_grid_subplot(title, subplot_titles)

    add_scatter_traces_to_grid(
        fig, d, keys_curves=['deaths'],
        annotation_text = ['Predictions Begin'] * 9,
        annotation_x = [n_days_past] * 9,
        annotation_y = d['deaths'].take(range(9)).apply(lambda x: x[n_days_past]).tolist()
    )

    # add more annotations
    annotation_y = d['deaths'].take(range(9)).apply(lambda x: x[n_days_past-1]).tolist()
    for i in range(9):
        if i==0:
            xref='x'
            yref='y'
        else:
            xref='x'+str(i+1)
            yref='y'+str(i+1)
        fig.add_annotation(
                x=n_days_past-1,
                y=annotation_y[i],
                text=past_days[-1],
                xref=xref,
                yref=yref,
                showarrow=True,
                arrowhead=7,
                visible=True
        )

    plot(fig, filename=filename, config={
        'showLink': False,
        'showSendToCloud': False,
        'sendData': True,
        'responsive': True,
        'autosizable': True,
        'displaylogo': False
    }, auto_open = auto_open)


"""
Hospital-level: severity index scatter, death predictions choropleth
"""
def add_hopsital_severity_index_scatter_traces(fig, df, target_days, plot_choropleth):
    def make_bubble_trace(lat, lon, text, size, color, name):
        bubble_trace = go.Scattergeo(
            visible=False,
            lat=lat,
            lon=lon,
            text=text,
            hovertemplate='%{text}',
            name=name,
            marker = dict(
                # color is only available for circle marker :(
                size = size,
                color = color,
                line_color='rgb(40,40,40)',
                line_width=0.5
            ),
            showlegend=False
        )
        return bubble_trace

    # colors = ["#2d3a9a", "#DEC34B", "#9e0521"]
    colors = ["#6E8E96", "#D3787D", "#AC3931"]

    # add predictions
    for i in range(target_days.size):
        for s in range(3):
            severity_col = f'Severity {i+1}-day'
            surge_col = f'Surge {i+1}-day'
            pred_col = f'Predicted Deaths {i+1}-day'
            df_s = df[df[severity_col] == s+1]
            values = df_s[severity_col]
            surge = df_s[surge_col]
            preds = df_s[pred_col]
            lat = df_s['Latitude']
            lon = df_s['Longitude']
            text = '<b>COVID-19 Pandemic Severity Index (CPSI)</b>: ' + values.astype(str) + '<br>' + \
                '<b>Surge Index (SUI)</b>: ' + surge.astype(str) + '<br>' + \
                df_s['text_hospital'].tolist() + '<br>' \
                '------ <br>' + \
                '<b># Deaths Predicted in County</b>: ' + preds.astype(str) + '<br>' + \
                df_s['text_county'].tolist()
            bubble_trace = make_bubble_trace(
                lat, lon, text, size=(s+1)*3, color=colors[s], name=str(s+1)
            )
            fig.add_trace(bubble_trace)

    return None


def make_severity_index_sliders(target_days, plot_choropleth):
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

    # days = list(map(lambda x: x.replace('#Deaths_', ''), past_days))
    num_days = target_days.size

    # add steps for predicted days
    for i in range(target_days.size):
        if i == 0:
            day_name = "Today"
        elif i == 1:
            day_name = "Tomorrow"
        else:
            day_name = "In " + str(i) + " Days"
        if plot_choropleth:
            args = ["visible", [False] * (4*num_days)]
        else:
            args = ["visible", [False] * 3*num_days]
        slider_step = {
            "args": args,
            "label": day_name,
            "method": "restyle"
        }
        for s in range(3):
            slider_step['args'][1][i*3 + s] = True
        if plot_choropleth:
            slider_step['args'][1][3*num_days + i] = True
        sliders[0]['steps'].append(slider_step)
    return sliders


def plot_hospital_severity_slider(df, # merged hospital and county, with severity
                                  target_days=np.array([1, 2, 3, 4, 5]),
                                  filename="severity_map.html",
                                  cumulative=True, # not currently used
                                  plot_choropleth=True,
                                  df_county = None,
                                  counties_json=None,
                                  dark=True,
                                  auto_open=True):
    """
    """
    if plot_choropleth:
        assert counties_json is not None, 'counties_json must be included for plotting choropleth'
        assert df_county is not None, 'df_county must be included for plotting county predictions'
    # TODO: note that df should have all data (preds and lat lon)
    # TODO: add previous days
    fips = df['SecondaryEntityOfFile'].tolist()
    tot_deaths = df['tot_deaths']

    d = df
    for day in target_days:
        pred_col = f'Predicted Deaths {day}-day'
        d[pred_col] = d[pred_col].astype(float).round()
    # replace missing values with string so below 'text' isn't missing
    d = d.replace(np.nan, 'Missing', regex=True)

    d['text_hospital'] = 'Hospital Name: ' + d['Hospital Name'] + '<br>' + \
        'Hospital # Employees: ' + d['Hospital Employees'].astype(str) + '<br>' + \
        'Hospital Type: ' + d['Hospital Type'] + '<br>' + \
        'Hospital Ownership: ' + d['Hospital Ownership'] + '<br>' + \
        'Estimated # Deaths in Hospital (As Of Yesterday): ' + d['Total Deaths Hospital'].astype(str)
    d['text_county'] = 'County: ' + d['CountyName'] + '<br>' + \
        'State: ' + d['StateName'] + ' (' + d['StateNameAbbreviation'] + ')' + '<br>' + \
        'County Population (2018): ' + d['PopulationEstimate2018'].astype(str) + '<br>' + \
        'County # Recorded Cases: ' + d['tot_cases'].astype(str) + '<br>' + \
        'County # Recorded Deaths: ' + tot_deaths.astype(str) + '<br>' + \
        'County Total # Hospitals: ' + d['#Hospitals'].astype(str) + '<br>' + \
        'County Total # Hospital Employees: ' + d['Hospital Employees in County'].astype(str)

    # compute scale_max for plotting colors
    pred_col = f'Predicted Deaths {target_days[-1]}-day'
    values = df_county[pred_col]
    scale_max = values.quantile(.995)

    map_title='Hospital-Level COVID-19 Pandemic Severity Index (CPSI)'
    if plot_choropleth:
        map_title = map_title + ' and Predicted Deaths Choropleth'
    map_title = map_title + ' Over the Next '+ str(target_days.size) + ' Days'

    # make main figure
    fig = make_us_map(map_title, dark)

    # add Scattergeo
    add_hopsital_severity_index_scatter_traces(fig, d, target_days, plot_choropleth)

    # make first day visible
    fig.data[0].visible = True
    fig.data[1].visible = True
    fig.data[2].visible = True

    # make choropleth if plotting
    if plot_choropleth:
        d_county = df_county
        add_counties_slider_choropleth_traces(
            fig, d_county, [], target_days, scale_max, counties_json
        )
        # make first day choropleth visible
        fig.data[3*target_days.size].visible = True

    # add slider to layout
    sliders = make_severity_index_sliders(target_days, plot_choropleth)
    fig.update_layout(
        sliders=sliders
    )

    plot(fig, filename=filename, config={
        'showLink': False,
        'showSendToCloud': False,
        'sendData': True,
        'responsive': True,
        'autosizable': True,
        'displaylogo': False
    }, auto_open = auto_open)
