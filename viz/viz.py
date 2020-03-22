from bokeh.sampledata import us_states, us_counties
from bokeh.plotting import figure, show, output_notebook, output_file, save
from bokeh import palettes
from bokeh.models import ColorBar,HoverTool,LinearColorMapper,ColumnDataSource,FixedTicker
output_notebook()
import re
import numpy as np


def plot_counties(df, variable_to_distribute, variables_to_display, state=None):
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

    colors = palettes.viridis(4)
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
            if temp_var > 0.0:
                variable_dictionary[re.sub("[^\w]","",variable_to_distribute)].append(temp_var)
                for vd in variables_to_display:
                    variable_dictionary[re.sub("[^\w]","",vd)].append(round(float(df[df["Header-FIPSStandCtyCode"] == StateCountyID][vd].values),2))
                color_idx = list(temp_var - np.array(index_range)).index(min(x for x in list(temp_var - np.array(index_range)) if x >= 0))
                county_colors.append(colors[color_idx])
            else:
                variable_dictionary[re.sub("[^\w]","",variable_to_distribute)].append(0.0)
                county_colors.append("#A9A9A9")
                for vd in variables_to_display:
                    variable_dictionary[re.sub("[^\w]","",vd)].append(0.0)
        else:
            variable_dictionary[re.sub("[^\w]","",variable_to_distribute)].append(0.0)
            county_colors.append("#A9A9A9")
            for vd in variables_to_display:
                variable_dictionary[re.sub("[^\w]","",vd)].append(0.0)
        #print temp_var,counties[county_id]["name"]
    variable_dictionary["color"] = county_colors
    source = ColumnDataSource(data = variable_dictionary)
    TOOLS = "pan,wheel_zoom,box_zoom,reset,hover,save"

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