from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import csv
import sqlite3
import sqlalchemy

# fetch data from SQlite database abd create a dataframe
con = sqlite3.connect("./falcon9.db")
cur = con.cursor()

sql_query = "SELECT * FROM `falcon9_tbl`"

df = pd.read_sql(sql=sql_query, con=con)
df['Flight_No'] = range(1, df.shape[0] + 1)
df['Class'] = [1 if landing_status ==
               'Success' else 0 for landing_status in df['Booster_Landing']]

colors = {
    'background': '#111111',
    'text': '#839496'
}

binary_class_palette = ['#DE3163', '#50C878']

# prepare launch sites options for selectbox


def getLaunchSitesOptions():
    launchSitesOptions = [{"label": "All Launch Sites", "value": "All"}]
    for launchSite in df['Launch_Site'].unique():
        launchSitesOptions.append({"label": launchSite, "value": launchSite})

    return launchSitesOptions


def getBoosterVersions():
    boosterVersionOptions = [{'label': 'All Booster Versions', 'value': 'All'}]
    for boosterVersion in df['Version_Booster'].unique():
        boosterVersionOptions.append(
            {'label': boosterVersion, 'value': boosterVersion})

    return boosterVersionOptions


app = Dash(external_stylesheets=[dbc.themes.SOLAR])  # Dash(__name__)

app.layout = html.Div(
    [
        dbc.Container(
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                html.Img(
                                    src=app.get_asset_url('Falcon_9_logo.png'),
                                    width=100,
                                    style={
                                        'margin-bottom': '20px',
                                    })),

                            dbc.Col(
                                [
                                    dbc.Label("Launch Site"),
                                    dcc.Dropdown(
                                        id='launch_site',
                                        options=getLaunchSitesOptions(),
                                        value="All",
                                        placeholder="Select Launch Site",
                                    ),

                                    html.Hr(),

                                    dbc.Label("Flight Number"),
                                    dcc.RangeSlider(
                                        id="flight_number",
                                        min=0, max=df['Flight_No'].max() + 1, step=25,
                                        value=[df['Flight_No'].min(),
                                               df['Flight_No'].max()]
                                    ),

                                    html.Hr(),

                                    dbc.Label("Payload Mass (kg)"),
                                    dcc.RangeSlider(
                                        id="payload_mass",
                                        min=0, max=df['Payload_Mass'].max() + 1, step=1000,
                                        value=[df['Payload_Mass'].min(),
                                               df['Payload_Mass'].max()]
                                    ),

                                    html.Hr(),

                                    dbc.Label("Booster Version"),
                                    dcc.Dropdown(
                                        id="booster_version",
                                        options=getBoosterVersions(),
                                        value="All",
                                        searchable=True,
                                        placeholder="Select a Booster Version"
                                    ),
                                ]
                            ),
                        ],

                        width=3),

                    dbc.Col(

                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Div(
                                            dcc.Graph(
                                                id="success_launchsite_pie_chart")
                                        ),
                                        width=5
                                    ),

                                    dbc.Col(
                                        html.Div(
                                            dcc.Graph(
                                                id="launch_site_v_payload_mass")
                                        ),
                                        width=7
                                    )
                                ]
                            ),

                            dbc.Row(
                                [
                                    dbc.Col(

                                    )
                                ]
                            )

                        ],

                        width=9)
                ]
            ),
            fluid=True
        )

    ],
    style={
        'padding': 10,
    }
)


@app.callback(
    Output(component_id="success_launchsite_pie_chart",
           component_property="figure"),
    Input(component_id="launch_site", component_property="value"),
    Input('flight_number', 'value'),
    Input('payload_mass', 'value'),
    Input('booster_version', 'value'),
)
def getSuccessPieChart(launch_site, flight_number, payload_mass, booster_version):
    filtered_df = df[((df['Flight_No'] >= flight_number[0]) & (df['Flight_No'] <= flight_number[1]))
                     & ((df['Payload_Mass'] >= payload_mass[0]) & (df['Payload_Mass'] <= payload_mass[1]))]

    chart_title = "Success launche percentage by Launch Site"
    chart_sub_title = ""

    # filter by booster versoin
    if booster_version != "All":
        filtered_df = df[df['Version_Booster']
                         == booster_version]

        chart_sub_title = "<br><sup>Booster %s</sup>" % booster_version

    filtered_df = filtered_df[['Launch_Site', 'Class']]

    if launch_site == None or launch_site == "All":
        fig = px.pie(filtered_df,
                     values='Class',
                     names='Launch_Site',
                     title=chart_title + chart_sub_title,
                     color_discrete_sequence=px.colors.qualitative.Antique,
                     hole=.3)

    else:
        filtered_df = filtered_df[filtered_df['Launch_Site'] ==
                                  launch_site].value_counts().to_frame().reset_index()

        chart_title = "Landing outcome for Launch Site %s" % launch_site

        # print(filtered_df)
        fig = px.pie(filtered_df,
                     values='count',
                     names=['Success', 'Failure'],
                     title=chart_title + chart_sub_title,
                     color_discrete_sequence=px.colors.qualitative.Dark2,
                     hole=.3,)

    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font_color=colors['text'],
        title_x=0.5,
        autosize=False,
        height=400
    )

    return fig


@app.callback(
    Output(component_id='launch_site_v_payload_mass',
           component_property='figure'),
    Input(component_id="launch_site", component_property="value"),
    Input('flight_number', 'value'),
    Input('payload_mass', 'value'),
    Input('booster_version', 'value')
)
def getLaunchSiteVsPayloadMass(launch_site, flight_number, payload_mass, booster_version):
    filtered_df = df[((df['Flight_No'] >= flight_number[0]) & (df['Flight_No'] <= flight_number[1]))
                     & ((df['Payload_Mass'] >= payload_mass[0]) & (df['Payload_Mass'] <= payload_mass[1]))]

    chart_title = "Landing outcome of Launch Site for against Payload Mass"
    chart_sub_title = ""

    # filter by booster versoin
    if booster_version != "All":
        filtered_df = df[df['Version_Booster']
                         == booster_version]

        chart_sub_title += "<sup>Booster: %s</sup>" % booster_version

    if launch_site == None or launch_site == "All":
        fig = px.scatter(filtered_df, x='Payload_Mass', y='Class', color='Launch_Site',
                         labels={
                             "Payload_Mass": "Payload Mass (kg)",
                             "Launch_Site": "Launch Site",
                             "Class": "Landing Outcome"
                         },
                         color_discrete_sequence=px.colors.qualitative.Dark2,
                         height=300,
                         )
    else:
        filtered_df = filtered_df[filtered_df['Launch_Site'] == launch_site]
        fig = px.scatter(filtered_df, x='Payload_Mass', y='Class', color='Launch_Site',
                         labels={
                             "Payload_Mass": "Payload Mass (kg)",
                             "Launch_Site": "Launch Site",
                             "Class": "Landing Outcome"
                         },
                         color_discrete_sequence=px.colors.qualitative.Dark2,
                         height=300,
                         )

        chart_title = "Landing outcome of Launch Site %s against Payload Mass" % (
            launch_site)

    fig.update_yaxes(zeroline=False,
                     tickvals=[0, 1], linecolor=colors['text'], gridcolor=colors['text'])
    fig.update_xaxes(zeroline=False, linecolor=colors['text'],
                     gridcolor=colors['text'])
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0.2)',
        font_color=colors['text'],
        title_text=chart_title + chart_sub_title,
        title_x=0.5,
    )

    return fig


if __name__ == '__main__':
    app.run(debug=True)
