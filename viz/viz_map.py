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
from datetime import date, datetime, timedelta

from viz.viz_map_utils import *

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
        if StateCountyID in list(df["countyFIPS"].values):
            temp_var = df[df["countyFIPS"] == StateCountyID][variable_to_distribute].values[0]
#             if temp_var > 0.0:
            variable_dictionary[re.sub("[^\w]","",variable_to_distribute)].append(temp_var)
            for vd in variables_to_display:
                variable_dictionary[re.sub("[^\w]","",vd)].append(round(float(df[df["countyFIPS"] == StateCountyID][vd].values),2))
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


# -- Plot cumulative deaths map with slider.

def plot_cumulative_deaths_map_with_slider(df,
                                           target_days=np.array([0, 1, 2, 3, 4, 5]),
                                           filename="results/deaths.html",
                                           plot_choropleth=False,
                                           counties_json=None,
                                           dark=True,
                                           plot_fig=True,
                                           auto_open=True):
    """
    Create an interactive plot of the cumulative deaths data for counties
    across the US, with a slider to change the date.

    Params
    ------
    df
       A county-level dataframe, with predictions if target_days has positive numbers.
       The df must also have columns called 'countyFIPS', 'tot_deaths', 'State', 'StateName',
       'CountyName', 'PopulationEstimate2018', 'tot_cases', '#Hospitals', 'POP_LATITUDE',
       and 'POP_LONGITUDE'.
    target_days
        Array of days to plot. 0 is the last observed day, positive numbers are predictions,
        and negative numbers are past days.
    filename
        Where to save the interactive plot html.
    plot_choropleth
        If True, plot a choropleth in addition to bubbles.
    counties_json
        A JSON object with the borders of the geographical units of interest.
        If None, will try to open geojson-counties-fips.json in the data dir of this repo.
    dark
        Whether to use a dark theme for the figure.
    plot_fig
        If True, plots the figure to a filename and possibly opens it in a browser.
    auto_open
        If True, the plot will open in a browser.
    """
    if plot_choropleth:
        if counties_json is None:
            counties_json = json.load(open(oj(parentdir, 'data', 'geojson-counties-fips.json'), "r"))

    # TODO: note that df should have all data (preds and lat lon)
    fips = df['countyFIPS'].tolist()
    tot_deaths = df['tot_deaths']

    latest_date = most_recent_date_in_data(df)
    latest_date_str = str_from_date(latest_date)

    d = df

    d['text'] = 'State: ' + d['State'].astype(str) + \
        ' (' + d['StateName'].astype(str) + ')' + '<br>' + \
        'County: ' + d['CountyName'].astype(str) + '<br>' + \
        'Population (2018): ' + d['PopulationEstimate2018'].astype(str) + '<br>' + \
        '# Recorded Cases as of ' + latest_date_str + ": " + \
        d['tot_cases'].astype(str) + '<br>' + \
        '# Recorded Deaths as of ' + latest_date_str +  ": " + \
        tot_deaths.astype(str) + '<br>' + \
        '# Hospitals: ' + d['#Hospitals'].astype(str)

    map_title='Predicted Cumulative COVID-19 Deaths<br>' + \
        '<span style="font-size: 14px; color: red;">Use the slider below the map to change date.</span>'

    # make main figure
    fig = make_us_map(map_title, dark)

    target_dates = make_target_dates(df, target_days)
    observed_cols = observed_dates_to_cols(np.array(target_dates)[target_days <= 0])
    predicted_cols = target_days_to_cols(target_days[target_days > 0])

    plotting_cols = observed_cols + predicted_cols

    # make choropleth if plotting
    # want this to happen first so bubbles overlay
    if plot_choropleth:
        add_choropleth_traces(
            fig, df, plotting_cols, counties_json
        )

    value_labels = []
    for i, date in enumerate(target_dates):
        if target_days[i] <= 0:
            value_label = '<b>Observed Count, ' + nice_date_str(str_from_date(date)) + ': </b>'
        else:
            value_label = '<b>Predicted Count, ' + nice_date_str(str_from_date(date)) + ': </b>'
        value_labels.append(value_label)

    # add Scattergeo
    add_bubble_traces(
        fig, df, plotting_cols, plot_choropleth, show_hovertext = True,
        value_labels = value_labels
    )

    # make first day visible
    fig.data[0].visible = True
    if plot_choropleth:
        # make bubbles visible
        fig.data[n_past_days + target_days.size].visible = True

    # add slider to layout
    sliders = make_slider_from_dates(target_dates, plot_choropleth)
    fig.update_layout(
        sliders=sliders
    )

    if plot_fig:
        plot(fig, filename=filename, config={
            'showLink': False,
            'showSendToCloud': False,
            'sendData': True,
            'responsive': True,
            'autosizable': True,
            'displaylogo': False
        }, auto_open = auto_open)
    fig['layout']['title']['font']['size'] = 25
    return fig


# --- Plot hospital severity index.

def add_hopsital_severity_index_scatter_traces(fig, df, target_days, visible=False):
    def make_bubble_trace(lat, lon, text, size, color, name):
        bubble_trace = go.Scattergeo(
            visible=visible,
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

    colors = ["#6E8E96", "#D3787D", "#AC3931"]

    target_date_strs = [nice_date_str(str_from_date(date))
                        for date in make_target_dates(df, target_days)]

    # add predictions
    for i in range(len(target_days)):
        for s in range(3):
            severity_col = f'Severity {target_days[i]}-day'
            surge_col = f'Surge {target_days[i]}-day'
            pred_col = f'Predicted Deaths {target_days[i]}-day'
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
                '<b># Deaths Predicted in County, ' + target_date_strs[i] + '</b>: ' + \
                preds.astype(str) + '<br>' + df_s['text_county'].tolist()
            bubble_trace = make_bubble_trace(
                lat, lon, text, size=s+7, color=colors[s], name=str(s+1)
            )
            fig.add_trace(bubble_trace)

    return None


def make_severity_index_sliders(dates, plot_choropleth):
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

    num_days = len(dates)

    # add steps for predicted days
    for i, date in enumerate(dates):
        if plot_choropleth:
            args = ["visible", [False] * (4*num_days)]
        else:
            args = ["visible", [False] * 3*num_days]
        slider_step = {
            "args": args,
            "label": nice_date_str(str_from_date(date)),
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
                                  filename="severity_map.html", # no effect unless plot = True
                                  plot_choropleth=False,
                                  df_county=None,
                                  counties_json=None,
                                  dark=True,
                                  plot_fig=True,
                                  auto_open=True,
                                  county_filter=None):
    """
    Create an interactive plot of the predicted hospital-level severity index
    data for hospitals across the US, with a slider to change the date.

    Params
    ------
    df
       A hospital-level dataframe, with predictions.
    target_days
        Array of days to plot. Unlike for plot_cumulative_deaths_map_with_slider(),
        must be only positive numbers.
    filename
        Where to save the interactive plot html.
    plot_choropleth
        If True, plot a choropleth in addition to bubbles.
    df_county
        A county-level df with predictions. Must be present if plot_choropleth is True.
    counties_json
        A JSON object with the borders of the geographical units of interest.
        If None, will try to open geojson-counties-fips.json in the data dir of this repo.
    dark
        Whether to use a dark theme for the figure.
    plot_fig
        If True, plots the figure to a filename and possibly opens it in a browser.
    auto_open
        If True, the plot will open in a browser.

    """
    target_days = target_days[target_days > 0]

    if plot_choropleth:
        if counties_json is None:
            counties_json = json.load(open(oj(parentdir, 'data', 'geojson-counties-fips.json'), "r"))
        assert df_county is not None, 'df_county must be included for plotting county predictions'
    # TODO: note that df should have all data (preds and lat lon)
    d = df
    d_c = df_county

    if county_filter is not None: # TODO: remove this
        d = d[d['CountyName'] == county_filter]
        if plot_choropleth:
            d_c = d[d['CountyName'] == county_filter]

    fips = d['countyFIPS'].tolist()
    tot_deaths = d['tot_deaths']

    for day in target_days:
        pred_col = f'Predicted Deaths {day}-day'
        d[pred_col] = d[pred_col].astype(float).round()
    # replace missing values with string so below 'text' isn't missing
    d = d.replace(np.nan, 'Missing', regex=True)

    latest_date_str = d.filter(regex='#Deaths_').columns[-1].replace('#Deaths_', '')

    d['text_hospital'] = 'Hospital Name: ' + d['Hospital Name'].astype(str) + '<br>' + \
        'Hospital # Employees: ' + d['Hospital Employees'].astype(str) + '<br>' + \
        'Hospital Type: ' + d['Hospital Type'].astype(str) + '<br>' + \
        'Hospital Ownership: ' + d['Hospital Ownership'].astype(str) + '<br>' + \
        'Estimated # Deaths in Hospital as of ' + latest_date_str + ": " + \
        d['Total Deaths Hospital'].round().astype(str)
    d['text_county'] = 'County: ' + d['CountyName'].astype(str) + '<br>' + \
        'State: ' + d['StateName'].astype(str) + '<br>' + \
        'County Population (2018): ' + d['PopulationEstimate2018'].astype(str) + '<br>' + \
        'County # Recorded Cases as of ' + latest_date_str + ": " + \
        d['tot_cases'].astype(str) + '<br>' + \
        'County # Recorded Deaths as of ' + latest_date_str + ": " + \
        tot_deaths.astype(str) + '<br>' + \
        'County Total # Hospitals: ' + d['#Hospitals'].astype(str) + '<br>' + \
        'County Total # Hospital Employees: ' + d['Hospital Employees in County'].astype(str)

    map_title='Hospital-Level COVID-19 Pandemic Severity Index (CPSI)'
    if plot_choropleth:
        map_title = map_title + ' and Predicted Deaths'
    map_title = map_title + '<br>' + \
    '<span style="font-size: 14px; color: red;">Use the slider below the map to change date.</span>'

    # make main figure
    fig = make_us_map(map_title, dark)

    # get prediction dates
    latest_date = datetime.strptime(latest_date_str, '%m-%d-%Y').date()
    time_deltas = [timedelta(days = int(day)) for day in target_days]
    pred_dates = [latest_date + time_delta for time_delta in time_deltas]

    # add Scattergeo
    add_hopsital_severity_index_scatter_traces(fig, d, target_days, plot_choropleth)

    # make first day visible
    fig.data[0].visible = True
    fig.data[1].visible = True
    fig.data[2].visible = True

    # make choropleth if plotting
    if plot_choropleth:
        plotting_cols = target_days_to_cols(target_days)
        add_choropleth_traces(
            fig, d_c, plotting_cols, counties_json
        )
        # make first day choropleth visible
        fig.data[3*target_days.size].visible = True

    # add slider to layout
    sliders = make_severity_index_sliders(pred_dates, plot_choropleth)
    fig.update_layout(
        sliders=sliders
    )

    if plot_fig:
        plot(fig, filename=filename, config={
            'showLink': False,
            'showSendToCloud': False,
            'sendData': True,
            'responsive': True,
            'autosizable': True,
            'displaylogo': False
        }, auto_open = auto_open)
    fig['layout']['title']['font']['size'] = 25
    return fig


# -- Plot map of daily change in deaths.

def plot_change_map():
    """
    Plot a map of the US with the change in # of new deaths from day to day.
    new_death{t} = pred_cumulative{t} - pred_cumulative{t-1}
    change{t} = new_death{t} - new_death{t - 1}
    """
    pass

