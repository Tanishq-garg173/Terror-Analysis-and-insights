# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 21:53:04 2020

@author: hp
"""

import pandas as pd
import dash
import dash_html_components as html
from  dash.dependencies import Input,Output,State
import webbrowser
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px 
from dash.exceptions import PreventUpdate

app=dash.Dash()   #object creation 

def load_data():
    data = "global_terror.csv"
    global df    #set to none at last-memory management 
    df = pd.read_csv(data)
   #print('\n First 5 records:\n ',df.head())
  
    global monthdesc
    monthdesc={'January':1,
                'February':2,
                'March':3,
                'April':4,
                'May':5,
                'June':6,
                'July':7,
                'August':8,
                'September':9,
                'October':10,
                'November':11,
                'December':12}
  
    global month_list
    month_list= [{"label":key, "value":values} for key,values in monthdesc.items()]

    global date_list
    date_list = [x for x in range(1, 32)] #1 to 31 
   
    global region_list
    region_list=[{'label':str(i),'value':str(i)} for i in sorted(df['region_txt'].unique().tolist())]
   
    global country_list #converted to dict to link 
    country_list = df.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()
    
    global state_list
    state_list = df.groupby("country_txt")["provstate"].unique().apply(list).to_dict()
    
    global city_list
    city_list=df.groupby("provstate")["city"].unique().apply(list).to_dict()
    
    global attack_type_list
    attack_type_list= [{'label':str(i),'value':str(i)} for i in df['attacktype1_txt'].unique().tolist()]
    
    global year_list
    year_list=  sorted(df['iyear'].unique().tolist())
    
    global year_dict
    year_dict= {str(i):str(i) for i in year_list }  #slider require year to be a dictionary

  # dropdown -chart
    global cdd_values
    cdd_val = {"Terrorist organisation":'gname',
                  "Target Nationality":'natlty1_txt', 
                  "Target type":'targtype1_txt', 
                  "Attack type":'attacktype1_txt', 
                  "Weapon Type":'weaptype1_txt', 
                  "Region":'region_txt', 
                  "Country attacked":'country_txt'
                          }
                
    cdd_values = [{"label":keys, "value":value} for keys, value in cdd_val.items()]
  
def open_browser():
    webbrowser.open_new('http://127.0.0.1:8050/') #chk address


def create_app_ui():
    layout=html.Div([html.H1(
        id='head_1',
        children='Terror analysis and Insights',
        style={'textAlign': 'center'}),
        
        dcc.Tabs(
            id="Tabs",
            value="Map",
            children=[dcc.Tab(label="Map tool" ,
                              id="Map tool",
                              value="Map",
                              children=[dcc.Tabs(id = "subtabs",
                                                 value = "WorldMap",
                                                 children = [dcc.Tab(label="World map",
                                                                     id="map_World",
                                                                     value="WorldMap"),
                                                             dcc.Tab(label="India map",
                                                                     id="map_India",
                                                                     value="IndiaMap")
                                                             ]),
                                        
                                        html.Br(),
                                        html.H4(id='head_2',
                                                children='Choose map filters',
                                                style={'text-align':'left'}),
                                        
                                        dcc.Dropdown(
                                            id='month-dd',
                                            options= month_list,
                                            placeholder='Select month',
                                            multi=True,
                                            style={'display':'block',
                                                   'width':'300px'}),
                                        
                                        dcc.Dropdown(
                                            id='date-dd',
                                            options= date_list,
                                            placeholder='Select date',
                                            multi=True,
                                            style={'display':'block',
                                                   'width':'300px'}),
      
                                        dcc.Dropdown(
                                            id='region-dd',
                                            options= region_list,
                                            placeholder='Select region',
                                            multi=True,
                                            style={'display':'block',
                                                   'width':'300px'}),
            
                                        dcc.Dropdown(
                                            id='country-dd',  
                                            options=country_list,
                                            value='India',
                                            placeholder='Select country',
                                            multi=True,
                                            style={'display':'block',
                                                   'width':'300px'}),
            
                                        dcc.Dropdown(
                                            id='state-dd',
                                            options= state_list,
                                            placeholder='Select state/province',
                                            multi=True,
                                            style={'display':'block',
                                                   'width':'300px'}),
            
                                        dcc.Dropdown(
                                            id='city-dd',
                                            options= city_list,
                                            placeholder='Select city',
                                            multi=True,
                                            style={'display':'block',
                                                   'width':'300px'}),
           
                                        dcc.Dropdown(
                                            id='attacktype-dd',
                                            options=attack_type_list,
                                            placeholder='Select attack type',
                                            multi=True,
                                            style={'display':'block',
                                                   'width':'300px'}),
                                        
                                        html.H4(id='head_3',
                                                children='Select year range',
                                                style={'text-align':'left'}),
                                        
                                        dcc.RangeSlider(id='year-slider',
                                                        min=min(year_list),
                                                        max=max(year_list),
                                                        value=[min(year_list),max(year_list)],
                                                        marks=year_dict,
                                                        step=None),
                                        html.Hr()
                                        ]),
                      
                      dcc.Tab(label = "Chart Tool",
                              id="chart tool", 
                              value="Chart",
                              children=[dcc.Tabs(id = "stab2",
                                                 value = "W-Chart",
                                                 children = [dcc.Tab(label="World chart", 
                                                                     id="chart-world", 
                                                                     value="WorldChart"
                                                                     ),          
                                                             
                                                             dcc.Tab(label="India chart",
                                                                     id="chart-India", 
                                                                     value="IndiaChart",
                                                                    
                                                                     )]),
                                        
                                        html.Br(),
                                         html.H4(id='head_4',
                                                children='Choose chart filters',
                                                style={'text-align':'left'}),
                                        
                                        dcc.Dropdown(id="Chart-dd",
                                                     options = cdd_values,
                                                     placeholder="Select option",
                                                     value = "region_txt",
                                                     style={'display':'block',
                                                            'width':'300px'}),#default chart for region
                                        
                                        html.Br(),
                                        
                                        dcc.Input(id="search",
                                                  placeholder="Search",
                                                  style={'display':'block',
                                                   'width':'300px'}),
    
                                        html.H4(id='head_5',
                                                children='Select year range',
                                                style={'text-align':'left'}),
                                        
                                        dcc.RangeSlider(
                                            id='year-slider1',
                                            min=min(year_list),
                                            max=max(year_list),
                                            value=[min(year_list),max(year_list)],
                                            marks=year_dict,
                                            step=None),
                                        
                                        html.Br(),
                                        html.Hr()
                                        
                                        ]),    
                      ]),
        html.Div(id = "graph-object", children ="Graph is shown here")
        ])
    
    return layout


# linking dripdowns
@app.callback(dash.dependencies.Output('graph-object', 'children'),
    [dash.dependencies.Input("Tabs", "value"),
     dash.dependencies.Input('month-dd', 'value'),
     dash.dependencies.Input('date-dd', 'value'),
     dash.dependencies.Input('region-dd', 'value'),
     dash.dependencies.Input('country-dd', 'value'),
     dash.dependencies.Input('state-dd', 'value'),
     dash.dependencies.Input('city-dd', 'value'),
     dash.dependencies.Input('attacktype-dd', 'value'),
     dash.dependencies.Input('year-slider', 'value'), 
     dash.dependencies.Input('year-slider1', 'value'), 
     dash.dependencies.Input("Chart-dd", "value"),
     dash.dependencies.Input("search", "value"),
     dash.dependencies.Input("stab2", "value")]
    )

def update_app9_ui(Tabs, month_value, date_value,region_value,country_value,state_value,city_value,attack_value,year_value,chart_year_selector, chart_dp_value, search,
                   stab2):
    fig = None
     
    if Tabs == "Map":
        print("Data Type of month value = " , str(type(month_value)))
        print("Data of month value = " , month_value)
        
        print("Data Type of Day value = " , str(type(date_value)))
        print("Data of Day value = " , date_value)
        
        print("Data Type of region value = " , str(type(region_value)))
        print("Data of region value = " , region_value)
        
        print("Data Type of country value = " , str(type(country_value)))
        print("Data of country value = " , country_value)
        
        print("Data Type of state value = " , str(type(state_value)))
        print("Data of state value = " , state_value)
        
        print("Data Type of city value = " , str(type(city_value)))
        print("Data of city value = " , city_value)
        
        print("Data Type of Attack value = " , str(type(attack_value)))
        print("Data of Attack value = " , attack_value)
        
        print("Data Type of year value = " , str(type(year_value)))
        print("Data of year value = " , year_value)
        
        
        year_range = range(year_value[0], year_value[1]+1)
        new_df = df[df["iyear"].isin(year_range)]
        
        #to set dates in month
        if month_value==[] or month_value is None:
            pass
        else:
            if date_value==[] or date_value is None:
                new_df = new_df[new_df["imonth"].isin(month_value)]
            else:
                new_df = new_df[new_df["imonth"].isin(month_value) & (new_df["iday"].isin(date_value))]
        
        # filter for region country state
        
        if region_value==[] or region_value is None:
            pass
        else:
            if country_value==[] or country_value is None :
                new_df = new_df[new_df["region_txt"].isin(region_value)]
            
            else:
                if state_value == [] or state_value is None:
                    new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                    (new_df["country_txt"].isin(country_value))]
                
                else:
                    if city_value == [] or city_value is None:
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&
                        (new_df["country_txt"].isin(country_value)) &
                        (new_df["provstate"].isin(state_value))]
                    
                    else:
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&
                        (new_df["country_txt"].isin(country_value)) &
                        (new_df["provstate"].isin(state_value))&
                        (new_df["city"].isin(city_value))]
                        
        if attack_value == [] or attack_value is None:
            pass
        else:
            new_df = new_df[new_df["attacktype1_txt"].isin(attack_value)] 
        
        mapFigure = go.Figure()
        if new_df.shape[0]:
            pass
        else: 
            new_df = pd.DataFrame(columns = ['iyear', 
                                             'imonth', 
                                             'iday',
                                             'country_txt',
                                             'region_txt', 
                                             'provstate',
                                             'city',
                                             'latitude',
                                             'longitude',
                                             'attacktype1_txt', 
                                             'nkill'])
            
            new_df.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]
            
        
        mapFigure = px.scatter_mapbox(new_df,
                                      lat="latitude", 
                                      lon="longitude",
                                      color="attacktype1_txt",
                                      hover_name="city", 
                                      hover_data=["attacktype1_txt",
                                                  "region_txt",
                                                  "country_txt",
                                                  "provstate",
                                                  "city", 
                                                  "nkill",
                                                  "iyear",
                                                  "imonth",
                                                  "iday"],
                                      zoom=1.5
                                      )
        mapFigure.update_layout(mapbox_style="open-street-map",
                                autosize=True,
                                margin=dict(l=0, r=0, t=25, b=25),
                                )
          
        fig = mapFigure

    elif Tabs=="Chart":
        fig = None
        
        
        year_range_c = range(chart_year_selector[0], chart_year_selector[1]+1)
        chart_df = df[df["iyear"].isin(year_range_c)]
        

        
        if stab2 == "WorldChart":
            pass
        elif stab2 == "IndiaChart":
            chart_df = chart_df[(chart_df["region_txt"]=="South Asia") &(chart_df["country_txt"]=="India")]
        
        
        if chart_dp_value is not None and chart_df.shape[0]:
            
            if search is not None:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name = "count")
                chart_df  = chart_df[chart_df[chart_dp_value].str.contains(search, case=False)]
            
            else:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name="count")
        
        
        if chart_df.shape[0]:
            pass
        else: 
            chart_df = pd.DataFrame(columns = ['iyear', 'count', chart_dp_value])
            
            chart_df.loc[0] = [0, 0,"No data"]
        
        chartFigure = px.area(chart_df, x="iyear", y ="count", color = chart_dp_value)
        
        fig = chartFigure
    
    return dcc.Graph(figure = fig)



@app.callback(
  Output("date-dd", "options"),
  [Input("month-dd", "value")])

def update_date(month):
    option = []
    if month:
        option= [{"label":m, "value":m} for m in date_list]
    else:
        pass
    return option

@app.callback([Output("region-dd", "value"),
               Output("region-dd", "disabled"),  #for only india case 
               Output("country-dd", "value"),
               Output("country-dd", "disabled")],
              [Input("subtabs", "value")])
def update_r(tab):
    region = None
    disabled_r = False
    country = None
    disabled_c = False
    
    if tab == "WorldMap":
        pass
    
    elif tab=="IndiaMap":
        region = ["South Asia"]
        disabled_r = True
        country = ["India"]
        disabled_c = True
    
    return region, disabled_r, country, disabled_c



@app.callback(
    Output('country-dd', 'options'),
    [Input('region-dd', 'value')])

def set_country_options(region_value):
    option = []
    
    if region_value is  None:
        raise PreventUpdate
    
    else:
        for var in region_value:
            
            if var in country_list.keys():
                option.extend(country_list[var])
    
    return [{'label':m , 'value':m} for m in option]


@app.callback(
    Output('state-dd', 'options'),
    [Input('country-dd', 'value')])

def set_state_options(country_value):
  # Making the state Dropdown data
    option = []
    
    if country_value is None :
        raise PreventUpdate
    
    else:
        for var in country_value:
            if var in state_list.keys():
                option.extend(state_list[var])
    
    return [{'label':m , 'value':m} for m in option]

@app.callback(
    Output('city-dd', 'options'),
    [Input('state-dd', 'value')])

def set_city_options(state_value):
  # Making the city Dropdown data
    option = []

    if state_value is None:
        raise PreventUpdate
    else:
        for var in state_value:
            if var in city_list.keys():
                option.extend(city_list[var])

    return [{'label':m , 'value':m} for m in option]

def fmain():
  load_data()
  
  open_browser()
  
  global app
  app.layout = create_app_ui()
  app.title = "Terrorism Analysis"
  app.run_server()
  
  df = None #Memory saving 
  app = None


if __name__ == '__main__':
    fmain()
