import os
import color_scale
import data
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime
from dash.dependencies import Input, Output
from process_df import process_df


mapbox_access_token = 'pk.eyJ1IjoiaXZhbm5pZXRvIiwiYSI6ImNqNTU0dHFrejBkZmoycW9hZTc5NW42OHEifQ._bi-c17fco0GQVetmZq0Hw'

app = dash.Dash(__name__,external_stylesheets=['https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css'])

server = app.server
server.secret_key = os.environ.get('secret_key', 'secret')

# Color scale for heatmap (green-to-red)
color_scale = color_scale.GREEN_RED

# Load the data
df = data.load_data()

# Get all valuable column headers
to_skip = ['lat', 'lat-dir', 'lon', 'lon-dir', 'year', 'date']
main_columns = [x for x in df.columns if x not in to_skip]

print([{'label': str(date) for date in df['year'].unique()}])

# Layout generation
app.layout = html.Div([
    # LANDING
    html.Div(
        className='section',
        children=[
            html.H1('ACCIDENTS IN BARRANQUILLA', className='landing-text')
        ]
    ),
    html.Div(
        className='content',
        children=[
            html.Div(
                className='col',
                children=[
                    html.H2(
                        id='this-year',
                        style={
                            'fontSize': 60,
                            'color': '#D2D2D2',
                            'margin':'10px 50px 20px'
                        }
                    ),
                ]
            ),
            # SLIDER ROW
            html.Div(
                className='col',
                children=[
                    html.Div(
                        id='slider',
                        children=[
                            dcc.RangeSlider(
                                id='date-slider',
                                min=min(df['year']),
                                max=max(df['year']),
                                marks={str(date): str(date)
                                        for date in df['year'].unique()},
                                value=[min(df['year']),max(df['year'])],
                                allowCross=False
                            ),
                        ], style={
                            'background': '#191a1a',
                            'margin-bottom': '50px'
                        }
                    )
                ], style={
                    'background': '#191a1a',
                }
            ),
                
            # GRAPHS ROW
            html.Div(
                id='graphs',
                className='row',
                children=[
                    html.Div(
                        className='col-5',
                        children=[
                          dcc.Graph(
                              id='line-chart-damages',
                          ),
                        ]),
                    html.Div(
                        className='col-3',
                        children=[
                            dcc.Graph(
                                id='bar-chart',
                            ),
                        ]),
                    html.Div(
                        className='col-4',
                        children=[
                            dcc.Graph(
                                id='plot-graph',
                            ),
                        ])
                ], style={
                    'padding-bottom': 100
                }
            ),
            # INFO ROW
            html.Div(
                id='group-x',
                className='row',
                children=[
                    html.Div(
                        className='col-6',
                        children=[
                          html.Div(
                              className='row',
                              children=[
                                  
                                  html.Div(
                                      className='col-3',
                                      children=[
                                          html.H3(
                                              'Total Accidents',
                                              id='this-year-1st',
                                              style={
                                                  'fontSize': 12,
                                                  'color': '#D2D2D2'
                                              }
                                          ),
                                          html.H1(
                                              id='qty_accidents',
                                              style={
                                                  'fontSize': 30,
                                                  'color': '#D2D2D2'
                                              }
                                          )
                                      ]),
                                  html.Div(
                                      className='col-3',
                                      children=[
                                          html.H3(
                                              'Total injured',
                                              id='this-year-2nd',
                                              style={
                                                  'fontSize': 12,
                                                  'color': '#D2D2D2'
                                              }
                                          ),
                                          html.H1(
                                              id='qty-injured',
                                              style={
                                                  'fontSize': 30,
                                                  'color': '#D2D2D2'
                                              }
                                          )
                                      ]),
                                  html.Div(
                                      className='col-3',
                                      children=[
                                          html.H3(
                                              'Total fatalities',
                                              id='this-year-3rd',
                                              style={
                                                  'fontSize': 12,
                                                  'color': '#D2D2D2'
                                              }
                                          ),
                                          html.H1(
                                              id='qty_fatalities',
                                              style={
                                                  'fontSize': 30,
                                                  'color': '#D2D2D2'
                                              }
                                          )
                                      ])
                              ]),

                        ]),
                    html.Div(
                        className='col-3',
                        children=[
                            dcc.Dropdown(
                                id='xaxis-dd',
                                className='col',
                                options=[{'label': i, 'value': i}
                                         for i in main_columns],
                                value='RELEVANCIA_PARTIDO',
                            ),
                        ]),
                    html.Div(
                        className='col-3',
                        children=[
                            dcc.Dropdown(
                                id='yaxis-dd',
                                className='col',
                                options=[{'label': i, 'value': i}
                                         for i in main_columns],
                                value='PIEZA_URBANA',
                            ),
                            html.Div(
                                className='col radius-group',
                                children=[
                                    dcc.RadioItems(
                                        id='yaxis-type',
                                        options=[
                                          {'label': i, 'value': i} for i in ['total', 'relative']
                                        ],
                                        value='total',
                                        labelStyle={
                                            'color': '#D2D2D2'
                                        }
                                    ),
                                ])
                        ]),
                ]
            ),
            #HEAT MAP ROW
            html.Div(
                id='graphs1',
                className='row',
                children=[
                    html.Div(
                        className='col-2',
                        children=[
                            html.H3('heatmap x-axis',
                                id='this-year-3rd1',
                                style={
                                    'fontSize': 12,
                                    'color': '#D2D2D2',
                                    'padding-top': 150
                                }
                            ),
                            dcc.Dropdown(
                                id='xaxis-heatmap',
                                className='col',
                                options=[{'label': i, 'value': i}
                                         for i in ['hour','day','day of week','month']],
                                value='hour',
                            ),
                            html.H3('heatmap y-axis',
                                id='this-year-3rd2',
                                style={
                                    'fontSize': 12,
                                    'color': '#D2D2D2',
                                    'padding-top': 50
                                }
                            ),
                            dcc.Dropdown(
                                id='yaxis-heatmap',
                                className='col',
                                options=[{'label': i, 'value': i}
                                         for i in ['hour','day','day of week','month']],
                                value='month',
                            ),
                        ]),
                    html.Div(
                        className='col-10',
                        children=[
                            dcc.Graph(
                                id='heatmap',
                                style={
                                    'width': '100%',
                                }   
                            ),
                        ])
                ], style={
                    'padding-bottom': 100
                }
            ),
            # MAP ROW
            html.Div(
                className='row',
                children=[
                    # Main graph holding the map
                    dcc.Graph(
                        id='map-graph',
                        #animate=True,
                        style={
                          'width': '100%',
                          'height': 1000,
                        }
                    ),
                    
                ]),
            # MAP 2    
            html.Div(
                className='row',
                children=[
                    # Main graph holding the map
                    dcc.Graph(
                        id='map-graph-2',
                        #animate=True,
                        style={
                          'width': '100%',
                          'height': 1000,
                        }
                    ),
                    
                ]),
            # ABOUT ROW

        ],
        style={
            'padding': 40
        }
    )
]
)

########################CALLBACKS##########################
@app.callback(
    [
        Output("heatmap", 'figure'),
        Output("line-chart-damages", 'figure')
    ],
    [Input('date-slider', 'value'),Input('xaxis-heatmap', 'value'),Input('yaxis-heatmap', 'value')])
def update_heatmap(year_value,xaxis,yaxis):
    dff = df[(df["year"] >= year_value[0]) & (df["year"] <= year_value[1])]

    if xaxis==yaxis:
        yaxis='year'

    axis_dict = {'month': 'month_name', 'hour':'hour','day':'day_name','day of week':'day of week','year':'year'}
    ylab=dff[axis_dict[yaxis]].unique()
    xlab=dff[axis_dict[xaxis]].unique()

    legend_axis = {'month'      :['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
                   'hour'       :np.sort(list(dff['hour'].unique())),
                   'day of week': ['Mo','Tu','We','Th','Fr','Sa','So'],
                   'day'        :np.sort(list(dff['hour'].unique())),
                   'year'       :np.sort(list(dff['year'].unique())) }

    df_year_type=dff[[xaxis,'GRAVEDAD_ACCIDENTE','ID']].groupby([xaxis,'GRAVEDAD_ACCIDENTE'], as_index=False).count()
    dff=dff[[xaxis,yaxis,'ID']].groupby([xaxis,yaxis]).count().reset_index()

    trace = go.Heatmap(
        x=legend_axis[xaxis], 
        y=legend_axis[yaxis], 
        z=dff.pivot(yaxis,xaxis,'ID').fillna(0), 
        colorscale='RdYlGn', 
        reversescale=True,
        colorbar=dict(
                title='Number of accidents',
                titlefont={'color':'#D2D2D2'},
                tickfont={'color':'#D2D2D2'},
                tickcolor='#D2D2D2',
            ),
        showscale=True)

    data_freq_graph = go.Data([
        go.Scatter(
            name='just damages',
            x=np.sort(list(dff[xaxis].unique())), 
            y=df_year_type[df_year_type['GRAVEDAD_ACCIDENTE']=='Solo daños']['ID'],
            mode='lines',
            marker={
                'symbol': 'circle',
                'size': 5,
                'color': '#9C280F'
            },
            hoverlabel={
                'bgcolor': '#D2D2D2',
            },
        ),
        go.Scatter(
            name='with injured persons',
            # events qty
            x=np.sort(list(dff[xaxis].unique())), 
            # year
            y=df_year_type[df_year_type['GRAVEDAD_ACCIDENTE']=='Con heridos']['ID'],
            mode='lines',
            marker={
                'symbol': 'circle',
                'size': 5,
                'color': '#FFC300'
            },
            hoverlabel={
                'bgcolor': '#D2D2D2',
            },
        ),
        go.Scatter(
            name='with fatalities',
            # events qty
            x=np.sort(list(dff[xaxis].unique())), 
            # year
            y=df_year_type[df_year_type['GRAVEDAD_ACCIDENTE']=='Con muertos']['ID'],
            mode='lines',
            marker={
                'symbol': 'circle',
                'size': 5,
                'color': '#DAF7A6'
            },
            hoverlabel={
                'bgcolor': '#D2D2D2',
            },
        ),
    ])
    layout_freq_graph = go.Layout(
        xaxis={
            'gridcolor': '#696969',
            'gridwidth': 1,
            'autorange': True,
            'color': '#D2D2D2',
            'title': xaxis,
        },
        yaxis={
            'gridcolor': '#696969',
            'gridwidth': 1,
            'autorange': True,
            'color': '#D2D2D2',
            'title': 'Number of accidents',

        },
        margin={
            'l': 40,
            'b': 40,
            't': 10,
            'r': 0
        },
        legend=dict(font={'color':'#D2D2D2'}),
        hovermode='closest',
        paper_bgcolor='#464646',
        plot_bgcolor='#464646',
    )

    return {"data": [trace],
            "layout": go.Layout(height=500,
                                 title={"text": 'Accidents heatmap',
                                "font": {"color": '#D2D2D2'}},
                                xaxis={"title": xaxis,'color': '#D2D2D2',},
                                yaxis={"title": yaxis, "tickmode": "array",
                                       'color': '#D2D2D2'                                  
                                    },
                                paper_bgcolor='#464646',
                                plot_bgcolor='#464646',
                            )
            },go.Figure(
                data=data_freq_graph,  # 54b4e4
                layout=layout_freq_graph
            )
    

@app.callback(
    Output('this-year', 'children'),
    [Input('date-slider', 'value')])
def update_year(year_value):
    if year_value[0]==year_value[1]:
        years='Date Range: ' + str(year_value[0])
    else:
        years='Date Range: ' + str(year_value[0])+'-'+str(year_value[1])
    return years

@app.callback(
    Output('qty_accidents', 'children'),
    [Input('date-slider', 'value')])
def update_qty_accidents(year_value):
    dff = df[(df["year"] >= year_value[0]) & (df["year"] <= year_value[1])]
    return '{} '.format(str(dff.shape[0]))

@app.callback(
    Output('qty-injured', 'children'),
    [Input('date-slider', 'value')])
def update_qty_injured(year_value):
    dff = df[(df["year"] >= year_value[0]) & (df["year"] <= year_value[1])]
    return '{}'.format(str(dff['CANT_HERIDOS_EN _SITIO_ACCIDENTE'].sum()))

@app.callback(
    Output('qty_fatalities', 'children'),
    [Input('date-slider', 'value')])
def update_fatalities(year_value):
    dff = df[(df["year"] >= year_value[0]) & (df["year"] <= year_value[1])]
    return '{}'.format(str(dff['CANT_MUERTOS_EN _SITIO_ACCIDENTE'].sum()))

@app.callback(
    Output('bar-chart', 'figure'),
    [Input('date-slider', 'value'),
     Input('xaxis-dd', 'value'),
     Input('yaxis-type', 'value')])
def update_bar_chart(year_value,xaxis,axistype):
    dff = df[(df["year"] >= year_value[0]) & (df["year"] <= year_value[1])]
    dff=dff[[xaxis,'FECHA_ACCIDENTE','ID','year']]

    dff.dropna()
    dff_xx=dff.groupby([xaxis,"year"], as_index=False).count()

    unique_x=dff_xx[xaxis].unique()

    ally=[]
    traces=[]
    for year in range(min(year_value),max(year_value)+1):
        # Obtain the number to divide the results. If relative, it will obtain # of days, in order to obtain total accidents per day.
        if axistype=='relative':
            count_dff=[dff[(dff[xaxis]==i) & (dff['year']==year)]['FECHA_ACCIDENTE'].unique().size for i in unique_x]
        else:
            count_dff=[1 for i in unique_x]
        
        y0=dff_xx[dff_xx['year']==year][['ID',xaxis]] # Number of accidents per AXIS and YEAR
        y=[]
        counter=0
        for i in range(len(unique_x)): # Iterating all the AXIS unique categories
            if counter >= len(y0[xaxis]):
                y.append(pd.Series({'ID':0,xaxis:unique_x[i]}))
                print(y)
            elif y0[xaxis].iloc[counter]==unique_x[i]:
                    y.append(y0.iloc[counter])
                    counter=counter+1
            else:
                y.append(pd.Series({'ID':0,xaxis:unique_x[i]}))
        y=pd.DataFrame(y)
        ally.append(y)

        trace = go.Bar(
            name=year,
            x=y[xaxis].unique(),
            y=y['ID']/count_dff,        
        )
        traces.append(trace)

    layout = go.Layout(
        xaxis=dict(color='#D2D2D2'),
        yaxis=dict(
            title='Number of accidents',
            autorange=True,
            color='#D2D2D2',
            zeroline=True,
            gridwidth=1,
            zerolinecolor='rgb(255, 255, 255)',
            zerolinewidth=2,
        ),
        colorway=['#9C280F','#FFC300','#DAF7A6','#0C8522'],
        hoverlabel={
            'bgcolor': '#D2D2D2',
            'font': {
                'color': 'black'
            },
        },
        legend=dict(font={'color':'#D2D2D2'}),
        margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
        hovermode='closest',
        paper_bgcolor='#464646',
        plot_bgcolor='#464646',
    )

    return {'data': traces,'layout':layout}


@app.callback(
    Output('plot-graph', 'figure'),
    [Input('date-slider', 'value'),
     Input('xaxis-dd', 'value'),
     Input('yaxis-dd', 'value'),
     Input('yaxis-type', 'value')]
)
def update_plot(year_value, xaxis_value, yaxis_value, yaxis_type):
    """
    Top Right graph callback
    """
    dff = df[(df["year"] >= year_value[0]) & (df["year"] <= year_value[1])]
    dff=dff.groupby([xaxis_value,yaxis_value]).count()['ID']
    data = go.Data([
        go.Scatter(
            x=[i[0] for i in dff.index],
            y=[i[1] for i in dff.index],
            text= list(dff),
            mode='markers',
            marker={
                'symbol': 'circle',
                'size': list(dff)/np.max(list(dff))*100,
                'color': '#0C8522'
            },
            hoverlabel={
                'bgcolor': '#D2D2D2',
                'font': {
                    'color': 'black'
                },
            },
        )
    ],
        style={
        'color': '#D2D2D2'})

    layout = go.Layout(
        autosize=True,
        xaxis={
            'gridcolor' : '#696969',
            'gridwidth' : 1,
            'color': '#D2D2D2',
            'autorange': True,
            'title': xaxis_value,
            'showspikes': True
        },
        yaxis={
            'gridcolor' : '#696969',
            'gridwidth' : 1,
            'color': '#D2D2D2',
            'autorange': True,
            'title': yaxis_value,
        },
        margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
        hovermode='closest',
        paper_bgcolor='#464646',
        plot_bgcolor='#464646',
    )

    return go.Figure(
        data=data,
        layout=layout
    )


@app.callback(
    Output('map-graph', 'figure'),
    [Input('date-slider', 'value')]
)
def update_map(year_value):
    """
    Map graph callback
    """

    # Update dataframe with the passed value
    dff = df[(df["year"] >= year_value[0]) & (df["year"] <= year_value[1])]
    dff=dff[['lat','lon','ID']].groupby(['lat','lon']).count().reset_index()
    #yd=dff.pivot(yaxis_heatmap,xaxis_heatmap,'ID').fillna(0),


    # Paint mapbox into the data
    data = go.Data([
        go.Scattermapbox(
            lat=dff['lat'],
            lon=dff['lon'],
            mode='markers',
            marker=go.Marker(
                # size=dff['vel']
                size=dff['ID'],
                colorscale='RdYlGn',
                reversescale=True,
                cmin=dff['ID'].min(),
                color=dff['ID'],
                cmax=dff['ID'].max(),
                colorbar=dict(
                    title='Number of accidents',
                    titlefont={'color':'#D2D2D2'},
                    tickfont={'color':'#D2D2D2'},
                    tickcolor='#D2D2D2',
                ),
                opacity=0.5
            ),
            text=dff['ID'],
            hoverlabel={
                'bordercolor': None,
                'font': {
                    'color': '#D2D2D2'
                }
            }
        )
    ],
        style={
        'height': 800
    }
    )

    # Layout and mapbox properties
    layout = go.Layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            pitch=0,
            zoom=12,
            style='dark'
        ),
        mapbox_center={"lat": 10.981619, "lon": -74.802569},
        paper_bgcolor='#191a1a',
        plot_bgcolor='#191a1a',
    )

    return go.Figure(
        data=data,
        layout=layout
    )


# Run dash server
if __name__ == '__main__':
    app.run_server(debug=True)