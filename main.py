import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table  # #
import dash_daq as daq
import pandas as pd
import plotly.graph_objects as go
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
from dash import no_update
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import time
from usp.tree import sitemap_tree_for_homepage
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

BS = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
app = dash.Dash(__name__, external_stylesheets=[BS], update_title='Loading...',
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=2.0, maximum-scale=1.2, minimum-scale=0.5'}],
                )

server = app.server
app.config.suppress_callback_exceptions = True
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])
page_content = html.Div([html.Div([

                   html.Div([
                        daq.PowerButton(id='my-toggle-switch',
                                                   label={'label': 'Connection','style': {'fontSize': '22px','fontWeight': 'bold'}},
                                                   labelPosition='bottom', on=False, size=100,
                                                   color="green",
                                                   className='dark-theme-control'),
                       dcc.Dropdown(id='urlName',
                                    options=[{'label': i, 'value': i} for i in ['https://www.amsterdam.nl/en/']],
                                    multi=False,
                                    style={'cursor': 'pointer', 'marginTop': '2rem'},
                                    clearable=True,
                                    placeholder='Select URL',
                                    ),
                        html.P('Enter interval value', style = {'marginTop': '2rem'}),
                       dbc.Input(id='interval',
                                 type="text",
                                 debounce=True,
                                 value = '10',
                                 bs_size="mr",
                                 style={'width': '14rem',},
                                 autoFocus=True,
                                 placeholder="Enter a Interval as Second"),
                        dcc.Interval(
                              id='interval_component',
                              disabled=True,
                              interval=1 * 1000,  # in milliseconds
                              n_intervals=0)
                   ], className='aadb'),

                ], className='abcdb'),
     dcc.Store(id='memory-output'),

     html.Div([html.Div([html.Div([html.Div(dcc.Graph(id="getgraph",
                                            config={'displayModeBar': True,
                                                    'scrollZoom': True,
                                                    'modeBarButtonsToAdd': [
                                                        'drawline',
                                                        'drawrect',
                                                        'drawopenpath',
                                                        'select2d',
                                                        'eraseshape',
                                                    ]},
                                            style={'marginTop': '20px', },
                                            figure={
                                                'layout': {'legend': {'tracegroupgap': 0},

                                                           }
                                            }

                                            ), ),
                         html.Div(daq.Slider(id="sliderHeight",
                                             max=2100,
                                             min=400,
                                             value=530,
                                             step=100,
                                             size=400,
                                             vertical=True,
                                             updatemode='drag'), style={'margin': '20px'})], className='abcdb_graph'),


                        html.Div(daq.Slider(id="sliderWidth",

                                             max=2000,
                                             min=600,
                                             value=1000,
                                             step=100,
                                             size=600,
                                             updatemode='drag'),style = {'marginLeft' : '22rem'}),
                            ], className='aadb', style = {'marginLeft' : '15rem'}),
               html.Div(id="hiddendb1", children=[], style={'display': 'None'}),
               html.Div(id="hiddendb2", style={'display': 'None'}),
               html.Div(id="hiddendb3", children=[], style={'display': 'None'}),
               html.Div(id="hiddendb4", children=[], style={'display': 'None'}),
               html.Div(id="hiddendb5", children=[], style={'display': 'None'}),


               ],className='four-columns-div-user-controlsreel' ), ], ),
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):

    if pathname == '/':
        return page_content

@app.callback(Output('interval_component', 'disabled'),
              [Input("my-toggle-switch", "on")],
              )
def intervalcontrol(on):
    if on == 1:
        return False
    else:
        return True


@app.callback([Output('interval_component', 'interval'),Output('hiddendb3', 'children'),],
              [Input("interval", "value")],[State('hiddendb3', 'children')]
              )
def intervalcontrol2(val,grouphidden):
    if val != None or val != '' :
        val = int(val) * 1000
        x = 0
        if x in grouphidden :
            pass
        else : grouphidden.append(x)
    return val,grouphidden
    # else : raise PreventUpdate




@app.callback(Output('hiddendb2', 'children'),
              [Input('urlName', 'value'), Input('interval_component', 'n_intervals')],
              [State("my-toggle-switch", "on")]
              )
def getvalue(val,interval,on):
    if val == None :
        raise PreventUpdate
    if on ==1:
        for i in [val] :
            url = i
            b = []
            def time_url(driver, url):
                driver.get(url)

                        # Use the browser Navigation Timing API to get some numbers:
                        # https://developer.mozilla.org/en-US/docs/Web/API/Navigation_timing_API
                navigation_start = driver.execute_script(
                            "return window.performance.timing.navigationStart")
                dom_complete = driver.execute_script(
                            "return window.performance.timing.domComplete")
                total_time = dom_complete - navigation_start
                b.append(total_time)
                if total_time > 1000 :
                    try:
                        mail = smtplib.SMTP("smtp.gmail.com", 587)
                        mail.ehlo()
                        mail.starttls()
                        mail.login("marketingdatascientist@gmail.com", "klmisthebest.01")

                        mesaj = MIMEMultipart()
                        mesaj["From"] = "marketingdatascientist@gmail.com"  # Gönderen
                        mesaj["To"] = "marketingdatascientist@gmail.com"  # alan
                        mesaj["Subject"] = "your total_time is huge"  # Konusu

                        body = """

                        your total_time is huge

                        """

                        body_text = MIMEText(body, "plain")  #
                        mesaj.attach(body_text)

                        mail.sendmail(mesaj["From"], mesaj["To"], mesaj.as_string())
                        print("Mail is sent by success.")
                        mail.close()
                    except:
                        print("Error:", sys.exc_info()[0])


            driver = webdriver.Chrome(ChromeDriverManager().install())

            try:

                time_url(driver, url)

            finally:
                driver.close()
                        # print(total)
                        # total.append(final_score)


            return b
    else: raise PreventUpdate

@app.callback(Output('hiddendb5', 'children'),
              [Input('urlName', 'value'),Input('hiddendb2', 'children')],[State('hiddendb5', 'children')]
              )
def valhandlerl(data,data2,handler):
    if data == None :
        raise PreventUpdate
    handler.append(data)
    print('handler1', handler)
    return handler

@app.callback(Output('hiddendb4', 'children'),
              [Input('hiddendb2', 'children')],[State('hiddendb4', 'children'),State('hiddendb5', 'children'), State('urlName', 'value')]
              )
def valhandlerl(data,handler, hiddenparametre,value):
    if data == None :
        raise PreventUpdate

    print('ve burasinda durm ne', value)
    handler+=data
    return handler

# @app.callback(Output('urlName', 'options'),
#               [Input('hiddendb1', 'children')],[State("my-toggle-switch", "on")]
#               )
# def optionsval(data,on):
#     if data == None :
#         raise PreventUpdate
#
#     if on == 1:
#         df = pd.DataFrame(data, columns=['URL'])
#         return [{'label': i, 'value': i} for i in df['URL'].unique()]
#     else : no_update


@app.callback(Output('getgraph', 'figure'),
              [Input('hiddendb1', 'children'),
               Input('hiddendb4', 'children'),
               Input('hiddendb5', 'children'),
               Input('urlName', 'value'),
               Input('sliderWidth', 'value'),
               Input('sliderHeight', 'value')])
def graphreelTime(param,group, val,url, sliderwidth, sliderheight):
    if val == None or group == None:
        raise PreventUpdate
    print('param', param)
    print('group', group)
    a = list(zip(val, group))
    df = pd.DataFrame(a, columns=['URL', 'Times'])
    print('problem burda ',df)
    y = df[df['URL'] == url]['Times']
    print('y',y)
    x = [i for i in range(len(y))]
    fig = go.Figure()
    fig.add_trace(go.Scattergl(y=df[df['URL'] == url]['Times'], x = x, mode='lines',
                                   marker=dict(line=dict(width=0.2, color='white')), name="{}".format(val),
                                   ))
    fig.update_layout(
        autosize=False,
        width=sliderwidth,
        height=sliderheight,

        margin=dict(
            l=50,
            r=50,
            b=100,
            t=50,
            pad=4
        ),
        paper_bgcolor="LightSteelBlue",
        template="plotly_white"
    ),

    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)