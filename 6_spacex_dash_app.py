# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children = [ html.H1('Space Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),

                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                options=[ 
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'site1', 'value': 'CCAFS LC-40'},
                                    {'label': 'site2', 'value': 'VAFB SLC-4E'},
                                    {'label': 'site3', 'value': 'KSC LC-39A'},
                                    {'label': 'site4', 'value': 'CCAFS SLC-40'},
                                    ],
                                value='ALL',
                                placeholder="place holder here",
                                searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div([dcc.RangeSlider(min_payload, max_payload, 1000, value=[0, 10000], id='payload-slider'),
                                ]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                            ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))



def get_pie_chart(entered_site):
    
    filtered_df = spacex_df

    succ_ratio = {}
    if entered_site == 'ALL':
       for i in filtered_df['Launch Site'].unique():
           t = sum(filtered_df[filtered_df['Launch Site']==i]['class']==1)/filtered_df.shape[0]
           succ_ratio.update({i: t})
        
       df_sucess = pd.DataFrame.from_dict(succ_ratio, orient='index').reset_index()
       df_sucess.columns = ['Launch Site','Succ Ratio']


       fig = px.pie(df_sucess, 
       values='Succ Ratio', 
       names='Launch Site', 
       title='Total success launches by site')
    else:

        # return the outcomes piechart for a selected site
       df_site = filtered_df[filtered_df['Launch Site']==entered_site].groupby('class', as_index=False).agg({'Launch Site': 'count'})
       print(df_site)
       fig = px.pie(df_site, 
       values='Launch Site', 
       names='class', 
       title='Total success launches for site '+entered_site)



    return fig




# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'), 
[Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])

def get_scatter_plot(entered_site, weight_range):

    
    filtered_df = spacex_df

    filtered_df_tmp = filtered_df[ filtered_df['Payload Mass (kg)'].between(weight_range[0] , weight_range[1] )]
    print(filtered_df_tmp['class'].value_counts()[1]/(filtered_df_tmp['class'].value_counts()[0]+filtered_df_tmp['class'].value_counts()[1]))

    if entered_site == 'ALL':
        fig = px.scatter(filtered_df_tmp, x='Payload Mass (kg)', y="class", color="Booster Version Category")

    else:
        filtered_df_tmp = filtered_df_tmp[filtered_df_tmp['Launch Site']==entered_site]
        fig = px.scatter(filtered_df_tmp, x='Payload Mass (kg)', y="class", color="Booster Version Category")
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()

#Which site has the largest successful launches? KSC LC-39A
#Which site has the highest launch success rate?
#Which payload range(s) has the highest launch success rate?
#All
#3-4 0.72

#Which payload range(s) has the lowest launch success rate?
0-1 0.2

#Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest launch success rate?
#FT



