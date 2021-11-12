import base64
import io
import dash
import datetime
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_daq as daq
import dash_bootstrap_components as dbc
from django.http import HttpResponseRedirect

from ML_DIR import ML_Model as mf
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output, State

import pandas as pd
import plotly.express as px
from ML_DIR import ML_Function
df = px.data.gapminder().query("country=='India'")

# 예측
next_year_population = mf.get_next_LinearRegression() # LinearRegression 결과
next_year_population_2 = mf.get_next_SVR()

external_stylesheets= "https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css"


# Important: Define Id for Plotly Dash integration in Django
app = DjangoDash('dash_integration_id')

app.css.append_css({
"external_url": external_stylesheets
})


#-------------------------------------------------------------#

app.layout = html.Div(children=[
    # Total division 1
    html.Div([
        # Adding one extra Div
        # 1구간 시작
        html.Div([
            html.H2(children='Indian Population predcition over time',style={'textAlign': 'center'}),
            #html.Div(children='Type AI name which Make prediction result'),
        ], className = 'row'),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
        html.Div(id='output-data-upload'),
        # 1구간 종료

        # 2구간 시작
        html.Div([
            #-----------모델 SELECT AND check predict result------------------------------------#

            html.Div([dcc.Graph(id='bar-chart')]), # 사용자 입력에 따라 그래프변환을 위해  Graph 클래스 선언만 해놓은 후 id로 접근

            # dcc.Input(id='my-input', type='text', value="None"),
            dcc.RadioItems(id='my-input',
                       options=[
                           {'label': 'LinearRegression', 'value': 'lr'},
                           {'label': 'SVR', 'value': 'svr'}
                       ], style={'textAlign': 'right', 'padding':30},
                       value='lr',  # default 값
                       labelStyle={'display': 'inline-block'}),
            #----------------------------------------------------------------------------------#

            #---------toglle to show and hide dataframe----------------------------------------#
            html.Div([
                daq.ToggleSwitch(id='toggle', value=False),
                html.Div(id='my-toggle-switch-output')
            ]),

            html.Div([
                dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in df.columns],
                        data=df.to_dict('records'),
                        style_cell_conditional=[
                            {
                                'textAlign': 'center'
                            }
                        ],
                        style_data={
                            'color': 'black',
                            'backgroundColor': 'white'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(220, 220, 220)',
                            }
                        ],
                        style_header={
                            'backgroundColor': 'rgb(210, 210, 210)',
                            'color': 'black',
                            'fontWeight': 'bold'
                        }
                    )], style={'padding': 10}),
            ])
        # 2구간 종료
    ], style={'display': 'block','width': '88%','padding':20},className='row')
    ]
)

#-------------------------모델 별 시각화--------------------------#
@app.expanded_callback(
    Output("bar-chart",'figure'),
    Input("my-input", "value"))
def update_graph(input_value):
    if input_value=="svr":
        fig = px.bar(x=df['year'].append(pd.Series(df["year"][-1:]+5)).reset_index(drop = True), y=df["pop"].append(pd.Series(next_year_population_2[0])).reset_index(drop=True))
        fig.update_layout(transition_duration=500)
    else:
        fig = px.bar(x=df['year'].append(pd.Series(df["year"][-1:]+5)).reset_index(drop = True), y=df["pop"].append(pd.Series(next_year_population[0])).reset_index(drop=True))
        fig.update_layout(transition_duration=500) # Update시 딜레이 시간
    return fig

#--------------------------------------------------------------#

#-----------------------file upload----------------------------#

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            ML_Function.parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children
#--------------------------------------------------------------#

#-------------------------CSV 데이터 표현-----------------------#
@app.expanded_callback(
    Output("table",'data'),
    Input("toggle", "value"))
def update_data_show(toggle_value):
    #return df.to_dict(orient='records')[:5]
    return df.to_dict(orient='records')


if __name__ == '__main__':
    app.run_server(8052, debug=False)
