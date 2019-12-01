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
                            ),
                        ], style={
                            'background': '#191a1a',
                            'margin-bottom': '50px'
                        }
                    )
                ], style={
                    'background': '#191a1a',
                }),
                
            # GRAPHS ROW
            html.Div(
                id='graphs',
                className='row',
                children=[
                    html.Div(
                        className='col-5',
                        children=[
                          dcc.Graph(
                              id='freq-graph',
                          ),
                        ]),
                    html.Div(
                        className='col-3',
                        children=[
                            dcc.Graph(
                                id='another-graph',
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
                                          html.H1(
                                              id='this-year',
                                              style={
                                                  'fontSize': 60,
                                                  'color': '#D2D2D2'
                                              }
                                          ),
                                      ]
                                  ),
                                  html.Div(
                                      className='col-3',
                                      children=[
                                          html.H3(
                                              'Total',
                                              id='this-year-1st',
                                              style={
                                                  'fontSize': 12,
                                                  'color': '#D2D2D2'
                                              }
                                          ),
                                          html.H1(
                                              id='max-energy',
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
                                              id='max-velocity',
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
                                              id='max-impact-e',
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
            html.Div(
                className='col radius-group',
                children=[
                    dcc.RadioItems(
                        id='maporcloud',
                        options=[
                            {'label': i, 'value': i} for i in ['Map', 'WordCloud']
                        ],
                        value='Map',
                        labelStyle={
                            'color': '#D2D2D2'
                        }
                    ),
                ])
            # ABOUT ROW

        ],
        style={
            'padding': 40
        }
    )
]
)

@app.callback(
    [
        Output("heatmap", 'figure'),
        Output("freq-graph", 'figure')
    ],
    [Input('date-slider', 'value'),Input('xaxis-heatmap', 'value'),Input('yaxis-heatmap', 'value')])
def update_heatmap(year_value,xaxis,yaxis):
    dff = df[(df["year"] >= year_value[0]) & (df["year"] <= year_value[1])]

    xaxis_heatmap=xaxis 
    yaxis_heatmap=yaxis

    if xaxis_heatmap==yaxis_heatmap:
        yaxis_heatmap='year'

    if yaxis_heatmap=='month':
        ylab=dff['month_name'].unique()
    elif yaxis_heatmap=='hour':
        ylab=dff['hour'].unique()
    elif yaxis_heatmap=='day':
        ylab=dff['day_name'].unique()
    elif yaxis_heatmap=='day of week':
        ylab=dff['day of week'].unique()
    elif yaxis_heatmap=='year':
        ylab=dff['year'].unique()

    if xaxis_heatmap=='month':
        xlab=dff['month_name'].unique()
    elif xaxis_heatmap=='hour':
        xlab=dff['hour'].unique()
    elif xaxis_heatmap=='day':
        xlab=dff['day_name'].unique()
    elif xaxis_heatmap=='day of week':
        xlab=dff['day of week'].unique()
    elif xaxis_heatmap=='year':
        xlab=dff['year'].unique()

    df_year_type=dff[[xaxis_heatmap,'GRAVEDAD_ACCIDENTE','ID']].groupby([xaxis_heatmap,'GRAVEDAD_ACCIDENTE'], as_index=False).count()
    dff=dff[[xaxis_heatmap,yaxis_heatmap,'ID']].groupby([xaxis_heatmap,yaxis_heatmap]).count().reset_index()
    
    trace = go.Heatmap(
        x=np.sort(list(dff[xaxis_heatmap].unique())), 
        y=np.sort(list(dff[yaxis_heatmap].unique())), 
        z=dff.pivot(yaxis_heatmap,xaxis_heatmap,'ID').fillna(0), 
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
            # events qty
            x=np.sort(list(dff[xaxis_heatmap].unique())), 
            # year  df_year_type[aa['GRAVEDAD_ACCIDENTE']=='Solo daños']['ID']
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
            x=np.sort(list(dff[xaxis_heatmap].unique())), 
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
            x=np.sort(list(dff[xaxis_heatmap].unique())), 
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
            'title': xaxis_heatmap,
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
                                xaxis={"title": xaxis_heatmap,'color': '#D2D2D2',},
                                yaxis={"title": yaxis_heatmap, "tickmode": "array",
                                       'color': '#D2D2D2',
                                       #"tickvals": dff[yaxis_heatmap].unique(),
                                       #"ticktext": dff[xaxis_heatmap].unique(),
                                       #"ticktext": ['Afghanistan', 'Arab World', 'Australia', 'Belgium', 'Bangladesh',
                                       #             'Brazil', 'Canada', 'Colombia', 'Germany', 'East Asia & Pacific',
                                       #             'Europe &<br>Central Asia', 'India', 'Japan',
                                       #             'Latin America &<br>Caribbean', 'Middle East &<br>North Africa',
                                       #             'Mexico', 'North America', 'Saudi Arabia', 'Singapore',
                                       #             'Virgin Islands (US)', 'South Africa', 'Zimbabwe'],
                                       #"tickfont": {"size": 8}, "tickangle": -20}, )
                                       
                                    },
                                paper_bgcolor='#464646',
                                plot_bgcolor='#464646',
                            )
            },go.Figure(
                data=data_freq_graph,  # 54b4e4
                layout=layout_freq_graph
            )
    
# wordcloud for primary type defined by rank
def wordcloud_accident( df, rank ):
    text = ' '.join(df['address'])
    wordcloud = WordCloud(max_font_size=400, colormap="Oranges_r",max_words=200, background_color="black",width=2000, height=1000).generate(text)
    plt.figure( figsize=(20,10) )
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    


def clean_address2(x):
    xlist=x.split()
    xnew=list()
    for i in range(len(xlist)):
        curi=xlist[i]
        if curi in ['CL','CLL','CLLE','CCLLE','CALLE']:
            curi='C'
        elif curi in ['CR','CARRERA','CRA']:
            curi='K'
        elif curi in ['AVENIDA','AV']:
            curi='AV'

        xnew.append(curi)
    
    return("".join(xnew))
    
def CountFrequency(my_list): 
  
    # Creating an empty dictionary  
    freq = {} 
    for item in my_list: 
        if (item in freq): 
            freq[item] += 1
        else: 
            freq[item] = 1
    return(freq)

df['address']=df['address'].apply(clean_address2)

########################CALLBACKS##########################
@app.callback(
    Output('this-year', 'children'),
    [Input('date-slider', 'value')]
)
def update_text(year_value):
    if year_value[0]==year_value[1]:
        years=str(year_value[0])
    else:
        years=str(year_value[0])+'-'+str(year_value[1])
    """
    Callbacks for year text col
    """
    return years


@app.callback(
    Output('max-energy', 'children'),
    [Input('date-slider', 'value')]
)
def update_text(year_value):
    """
    Callback for energy digit col
    """    # data from current selected year
    dff = df[(df["year"] >= year_value[0]) & (df["year"] <= year_value[1])]
    return '{} accidents'.format(str(dff.shape[0]))


@app.callback(
    Output('max-velocity', 'children'),
    [Input('date-slider', 'value')]
)
def update_text(year_value):
    """
    Callbacks for velocity digit col
    """
    # data from current selected year
    dff = df[(df["year"] >= year_value[0]) & (df["year"] <= year_value[1])]
    return '{}'.format(str(dff['CANT_HERIDOS_EN _SITIO_ACCIDENTE'].sum()))



@app.callback(
    Output('max-impact-e', 'children'),
    [Input('date-slider', 'value')]
)
def update_text(year_value):
    """
    Callback for impact-e text col
    """
    # data from current selected year
    dff = df[(df["year"] >= year_value[0]) & (df["year"] <= year_value[1])]
    return '{}'.format(str(dff['CANT_MUERTOS_EN _SITIO_ACCIDENTE'].sum()))




@app.callback(
    Output('another-graph', 'figure'),
    [Input('date-slider', 'value'),
     Input('xaxis-dd', 'value'),
     Input('yaxis-type', 'value')]

)
def update_mid(year_value,xaxis,axistype):
    """
    Top Mid graph callback
    """
    marker_color='#333333'

    dff = df[(df["year"] >= year_value[0]) & (df["year"] <= year_value[1])]
    dff=dff[[xaxis,'FECHA_ACCIDENTE','GRAVEDAD_ACCIDENTE','ID','year']]

    dff.dropna()
    dff_xx=dff.groupby([xaxis,"year"], as_index=False).count()

    #dff_xx=dff.groupby([xaxis,'GRAVEDAD_ACCIDENTE'], as_index=False).count()
    list_dff=dff_xx[xaxis].unique()

    #count_dff_danos=[dff[(dff[xaxis]==i) & (dff['GRAVEDAD_ACCIDENTE']=='Solo daños')]['FECHA_ACCIDENTE'].unique().size for i in list_dff]
    #count_dff_heridos=[dff[(dff[xaxis]==i) & (dff['GRAVEDAD_ACCIDENTE']=='Con heridos')]['FECHA_ACCIDENTE'].unique().size for i in list_dff]
    #count_dff_muertos=[dff[(dff[xaxis]==i) & (dff['GRAVEDAD_ACCIDENTE']=='Con muertos')]['FECHA_ACCIDENTE'].unique().size for i in list_dff]

    #y0_danos=dff_xx[dff_xx['GRAVEDAD_ACCIDENTE']=='Solo daños'][['ID',xaxis]]
    #y0_heridos=dff_xx[dff_xx['GRAVEDAD_ACCIDENTE']=='Con heridos'][['ID',xaxis]]
    #y0_muertos=dff_xx[dff_xx['GRAVEDAD_ACCIDENTE']=='Con muertos'][['ID',xaxis]]

    ally=[]
    traces=[]
    for year in range(min(year_value),max(year_value)+1):
        if axistype=='relative':
            count_dff=[dff[(dff[xaxis]==i) & (dff['year']==year)]['FECHA_ACCIDENTE'].unique().size for i in list_dff]
        else:
            count_dff=[1 for i in list_dff]

        y0=dff_xx[dff_xx['year']==year][['ID',xaxis]]

        y=[]
        counter=0

        for i in range(len(list_dff)):
            if counter>=len(y0[xaxis]):
                y.append(pd.Series({'ID':0,xaxis:list_dff[i]}))
            elif y0[xaxis].iloc[counter]==list_dff[i]:
                    y.append(y0.iloc[counter])
                    counter=counter+1
            else:
                y.append(pd.Series({'ID':0,xaxis:list_dff[i]}))
        y=pd.DataFrame(y)
        ally.append(y)

        trace = go.Bar(
            name=year,
            x=y[xaxis].unique(),
            y=y['ID']/count_dff,        
        )
        traces.append(trace)

    
    
    #y_danos=[]
    #counter=0
    #for i in range(len(list_dff)):
    #    if y0_danos[xaxis].iloc[counter]==list_dff[i]:
    #        y_danos.append(y0_danos.iloc[counter])
    #        counter=counter+1
    #    else:
    #        y_danos.append(pd.Series({'ID':0,xaxis:list_dff[i]}))
    #y_danos=pd.DataFrame(y_danos)

    #y_heridos=[]
    #counter=0
    #for i in range(len(list_dff)):
    #    if y0_heridos[xaxis].iloc[counter]==list_dff[i]:
    #        y_heridos.append(y0_heridos.iloc[counter])
    #        counter=counter+1
    #    else:
    #        y_heridos.append(pd.Series({'ID':0,xaxis:list_dff[i]}))
    #y_heridos=pd.DataFrame(y_heridos)

    #y_muertos=[]
    #counter=0
    #for i in range(len(list_dff)):
    #    if y0_muertos[xaxis].iloc[counter]==list_dff[i]:
    #        y_muertos.append(y0_muertos.iloc[counter])
    #        counter=counter+1
    #    else:
    #        y_muertos.append(pd.Series({'ID':0,xaxis:list_dff[i]}))
    #y_muertos=pd.DataFrame(y_muertos)
    #y_muertos
    



    #trace1 = go.Bar(
    #    name='dict',
    #    x=y_danos[xaxis].unique(),
    #    y=y_danos['ID']/count_dff_danos,        
    #)
    #trace2 = go.Bar(
    #    name='with injured persons',
    #    x=y_heridos[xaxis].unique(),
    #    y=y_heridos['ID']/count_dff_heridos,        
    #)
    #trace3 = go.Bar(
    #    name='with fatalities',
    #    x=y_muertos[xaxis].unique(),
    #    y=y_muertos['ID']/count_dff_muertos,        
    #)

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

    return {
        'data': traces,
        #'data':[trace1,trace2,trace3],
        'layout':layout
    }


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
