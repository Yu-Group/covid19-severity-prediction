import os, inspect, json
from os.path import join as oj
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

from datetime import date, datetime, timedelta

import numpy as np
import plotly.graph_objs as go

# --- Functions for working with dates for the maps.

NICE_DATE_FORMAT = '%B %d'

DATA_DATE_FORMAT = '%m-%d-%Y'


def date_from_str(date_str):
    """
    Parse a date string in format DATA_DATE_FORMAT
    """
    return datetime.strptime(date_str, DATA_DATE_FORMAT).date()


def str_from_date(date):
    return date.strftime(DATA_DATE_FORMAT)


def most_recent_date_in_data(df):
    deaths_cols = df.filter(regex='^#Deaths_').columns
    latest_date_str = deaths_cols[-1].replace('#Deaths_', '')
    latest_date = date_from_str(latest_date_str)
    return(latest_date)


def nice_date_str(date_str):
    """
    date_str: in format DATA_DATE_FORMAT

    returns format NICE_DATE_FORMAT
    """
    return date_from_str(date_str).strftime(NICE_DATE_FORMAT)


def date_day(date_str):
    """
    date_str: in format DATA_DATE_FORMAT

    returns format "%-d"
    """
    return date_from_str(date_str).strftime("%-d")


def make_target_dates(df, target_days):
    latest_date = most_recent_date_in_data(df)
    time_deltas = [timedelta(days = int(day)) for day in target_days]
    plot_dates = [latest_date + time_delta for time_delta in time_deltas]
    return plot_dates


def date_to_n_days_ago(df, date_str):
    """
    Compute the number of days ago {the_date} occurred from latest date of
    predictions in the data.

    date_str: in format '%m-%d-%Y'

    """
    latest_date = most_recent_date_in_data(df)
    in_date = date_from_str(date_str)
    date_delta = latest_date - in_date
    return date_delta.days


def date_interval_n_days(begin_date_str, end_date_str):
    begin_date = date_from_str(begin_date_str)
    end_date = date_from_str(end_date_str)
    time_diff = end_date - begin_date
    return time_diff.days + 1


# --- Helpers for constructing map figures.


def make_us_map(title_text='', dark=False, usa_scope=True):
    """
    Make a plotly.graph_objs.Figure with a US map geo

    Params
    ------
    title_text
        The map title to display.
    dark
        Whether to use a dark theme for the figure.
    usa_scope
        Whether to center the figure on the US.
    """
    fig = go.Figure()

    if usa_scope:
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


def make_slider_from_dates(dates, double_layers=False):
    """
    Create slider controls for a plotly.graph_objs.Figure based on the dates provided.

    Params
    ------
    dates
        A list of datetime.datetime objects.
    double_layers
        If True, the figure corresponding to this slider has both choropleth and bubble traces,
        in which case the slider has to deal with twice as many layers.
    """
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

    # add steps for past days
    for i, date in enumerate(dates):
        if double_layers:
            args = ["visible", [False] * (2*num_days)]
        else:
            args = ["visible", [False] * num_days]
        slider_step = {
            # the first falses are the map traces
            # the last 12 trues are the scatter traces
            "args": args,
            "label": nice_date_str(str_from_date(date)),
            "method": "restyle"
        }
        slider_step['args'][1][i] = True # Toggle i'th trace to "visible"
        if double_layers:
            slider_step['args'][1][num_days + i] = True # and the other trace
        sliders[0]['steps'].append(slider_step)

    return sliders


def add_choropleth_traces(fig, df, plotting_cols, counties_json=None, visible=False,
                          show_hovertext=False, colorbar_title="Deaths",
                          color_scl = [[0.0, '#FFFFFF'],[0.2, '#B96D67'],[0.4, '#A83C3B'],
                                       [0.6, '#8B2222'],[0.8, '#5B0D0D'],[1.0, '#5A2318']],
                          value_labels = ["Deaths: "]):
    """
    Add choropleth layers to a fig using one or more of df's columns.

    Params
    ------
    fig
        A plotly.graph_objs.Figure
    df
        A Pandas dataframe which has the columns for plotting.
        The df must have a column called 'countyFIPS'.
    plotting_cols
        A list of column names to add as layers to fig.
    counties_json
        A JSON object with the borders of the geographical units of interest.
        If None, will try to open geojson-counties-fips.json in the data dir of this repo.
    visible
        Whether the layers should be visible in the figure.
    show_hovertext
        If True, df has a column called 'text' used for hover text in the choropleth.
    colorbar_title
        The title to display above the color scale.
    color_scl
        A list of lists with the range of colors to use for the color scale.
    value_labels
        A string list of length 1 or of the same length as plotting_cols to use in hover text.
    """
    if counties_json is None:
        counties_json = json.load(open(oj(parentdir, 'data', 'geojson-counties-fips.json'), "r"))

    def make_choropleth_trace(values, fips, text=None):
        choropleth_trace = go.Choropleth(
            visible=visible,
            colorscale=color_scl,
            z=values,
            text=text,
            geojson=counties_json,
            locations=fips,
            hoverinfo='skip',
            colorbar_title=colorbar_title
        )
        return choropleth_trace

    assert len(value_labels) == 1 or len(value_labels) == len(plotting_cols)

    # add past days
    for i, col in enumerate(plotting_cols):
        values = df[col]
        if np.any(values < 0):
            values[values < 0] = 0
        fips = df['countyFIPS']
        if show_hovertext:
            if len(value_labels) == 1:
                label = value_labels[0]
            else:
                label = value_labels[i]
            text = label + values.round().astype(str) + '<br>' + \
                df['text'].tolist()
        else:
            text = None

        choropleth_trace = make_choropleth_trace(values, fips, text)
        fig.add_trace(choropleth_trace)

    return None


def add_bubble_traces(fig, df, plotting_cols,
                      plot_choropleth=False, visible=False,
                      colorbar_title='<b> Deaths </b>',
                      show_hovertext=False,
                      color_scl = [[0.0, '#F5C8BB'],[0.2, '#B96D67'],[0.4, '#A83C3B'],
                                   [0.6, '#8B2222'],[0.8, '#5B0D0D'],[1.0, '#5A2318']],
                      value_labels = ["Deaths: "]):
    """
    Add bubble plot layers to a fig using one or more of df's columns.

    Params
    ------
    fig
        A plotly.graph_objs.Figure
    df
        A Pandas dataframe which has the columns for plotting.
        The df must have columns 'POP_LATITUDE' and 'POP_LONGITUDE'.
    plotting_cols
        A list of column names to add as layers to fig.
    visible
        Whether the layers should be visible in the figure.
    show_hovertext
        If True, df has a column called 'text' used for hover text in the choropleth.
    colorbar_title
        The title to display above the color scale.
    color_scl
        A list of lists with the range of colors to use for the color scale.
    """

    def make_bubble_trace(values, lat, lon, text=None):
        bubble_trace = go.Scattergeo(
            visible=visible,
            lat=lat,
            lon=lon,
            text=text,
            hovertemplate='%{text}',
            name="Bubble Plot",
            marker = dict(
                size = values,
                sizeref = 2. * 1000. / (100. ** 2.),
                color = values,
                colorscale = color_scl,
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode='area',
                colorbar_title = colorbar_title,
                showscale=not plot_choropleth
            )
        )
        return bubble_trace

    assert len(value_labels) == 1 or len(value_labels) == len(plotting_cols)

    for i, col in enumerate(plotting_cols):
        values = df[col]
        if np.any(values < 0):
            values[values < 0] = 0
        lat = df['POP_LATITUDE']
        lon = df['POP_LONGITUDE']
        if show_hovertext:
            if len(value_labels) == 1:
                label = value_labels[0]
            else:
                label = value_labels[i]
            text = label + values.round().astype(str) + '<br>' + \
                df['text'].tolist()
        else:
            text = None
        bubble_trace = make_bubble_trace(values, lat, lon, text)
        fig.add_trace(bubble_trace)

    return None


# --- Helpers for working with data.

def target_days_to_cols(target_days):
    predicted_cols = [f'Predicted Deaths {day}-day' for day in target_days]
    return predicted_cols


def observed_dates_to_cols(observed_dates):
    observed_cols = ['#Deaths_'+str_from_date(date) for date in observed_dates]
    return observed_cols


# --- Helpers to make derived data from predictions / observed data.

def add_new_deaths(df_county, target_days):
    # TODO: use average new deaths for past days
    deaths_cols = df_county.filter(regex='#Deaths_').columns
    for i, target_day in enumerate(target_days):
        if target_day < 1:
            # target_day of 0 represents the most recently observed counts
            # target_day of -1 is the second most recently observed, etc.
            baseline = df_county[deaths_cols[target_day - 2]]
            incol = df_county[deaths_cols[target_day - 1]]
            outcol_name = f'Observed New Deaths {target_day}-day'
        else:
            if target_day == 1:
                baseline = df_county['tot_deaths']
            else:
                baseline = df_county[f'Predicted Deaths {target_day-1}-day']
            incol = df_county[f'Predicted Deaths {target_day}-day']
            outcol_name = f'Predicted New Deaths {target_day}-day'

        df_county[outcol_name] = incol - baseline
        if i == 0:
            df_county['choropleth_scale_max'] = df_county[outcol_name]
        else:
            df_county['choropleth_scale_max'] = df_county[
                ['choropleth_scale_max', outcol_name]
            ].max(axis=1)

    return df_county


# TODO: update to compute change in new deaths
def add_change_in_new_deaths(df, target_days):

    ## TODO: put this into a helper fun
    deaths_cols = df.filter(regex='#Deaths_').columns
    latest_date_str = deaths_cols[-1].replace('#Deaths_', '')
    latest_date = datetime.strptime(latest_date_str, '%m-%d-%Y').date()
    time_deltas = [timedelta(days = int(day)) for day in target_days]
    plot_dates = [(latest_date + time_delta).isoformat() for time_delta in time_deltas]

    for i, target_day in enumerate(target_days):
        if target_day < 1:
            # target_day of 0 represents the most recently observed counts
            # target_day of -1 is the second most recently observed, etc.
            baseline = df[deaths_cols[target_day - 2]]
            incol = df[deaths_cols[target_day - 1]]
            outcol_name = f'Observed New Deaths {target_day}-day'
        else:
            if target_day == 1:
                baseline = df['tot_deaths']
            else:
                baseline = df[f'Predicted Deaths {target_day-1}-day']
            incol = df[f'Predicted Deaths {target_day}-day']
            outcol_name = f'Predicted New Deaths {target_day}-day'

        df[outcol_name] = incol - baseline
        if i == 0:
            df['choropleth_scale_max'] = df[outcol_name]
        else:
            df['choropleth_scale_max'] = df[['choropleth_scale_max', outcol_name]].max(axis=1)
