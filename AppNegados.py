import dash
from dash import html, dcc, callback,Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import date
import locale
global contador1, contador2
import hana_ml.dataframe as dataframe

contador1 = None
contador2 = None

# Set español
locale.setlocale(locale.LC_ALL,'es_ES.UTF-8')

# Leer el dataframe desde la tabla de la base de datos
conn = dataframe.ConnectionContext(
    address='548b50f4-1fe9-4725-baea-e9f96bb4f092.hana.prod-us10.hanacloud.ondemand.com',
    port='443',
    user='michfrec',
    password='Inicio2022',
    encrypt='true',
    sslValidateCertificate='false')

df = conn.sql('SELECT * FROM COLSUBSIDIO_SSS.T_CSV_SOLICITUDES_NEGADAS').collect()
df.columns
df = df[['SOLICITUD', 'PROCESO ACTUAL', 'HOMOLOGACION FINAL', 'CATEGORIA']]
conn.close()

# Crear la aplicación Dash y agregar estilos modernos usando Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.themes.GRID])

# Crear el diseño de la aplicación
app.layout = html.Div([

html.Div([
    dbc.Row(html.Img(src='assets\header.png', alt='BI', disable_n_clicks=True, width='95%', height='80%'), justify="center"),
    html.Hr(style={'borderWidth': "0.3vh", "width": "100%", "backgroundColor": "#B4E1FF","opacity":"1"}), 
    html.Label('Información actualizada a corte: ' + str(date.today().strftime('%A %d de %B de %Y')), style={'size':'7'} ),
    html.Br(),
    ]),

html.Div(dbc.Col([
    dbc.Row([
        dbc.Col([
            html.Img(src="assets/negado.png", style={'width': '80%', 'margin-top':'20px', 'height':'70%'}),
            html.Br(),], width=3),
        
        dbc.Col([html.H5("Ficha Técnica"),html.Br(),
            html.H6("Objetivo:"),
            html.P("Desarrollar una App de consulta para solicitudes de crédito negadas a fin de brindar información a cliente según las homologaciones definidas por el área de Riesgo."),
            html.H6("Tipo Análisis:"),
            html.P("Descriptivo"),
            html.H6("Metodología:"),
            html.P("App de consulta de información"), 
            html.H6("Fuentes de Información:"),
            html.Div("SIIF, Maestro de Agencias, Maestro de Asesores"), 
            html.P("NOTA: La información se actualizará diariamente con las solicitudes de los últimos seis meses."),
            html.H6("Frecuencia Actualización:"),
            html.P("Diaria"),
            ], width=5),
        dbc.Col([
            dbc.Button(children=dbc.Row([dbc.Col(html.Div("Ir a Consulta -->"), width=6), 
                                         dbc.Col(html.Div(className="fa-solid fa-forward"), width=2)], 
                className="text-center g-0 align-items-center"), className="btn btn-info col-10", id="IrPagina2"),
            html.Br(),html.Br(),html.H6("Alcance:"),
            html.P("Puntos de crédito y Centros de Servicio"),
            html.H6("Elaborado por: "),
            html.P("Área BI"), 
            html.H6("Desarrollador:"),
            html.P("Michael Andrés Fresneda Culma"), 
            html.H6("Responsable de actualización:"),
            html.P("Michael Andrés Fresneda Culma"), 
            html.H6("Fecha Despliegue:"),
            html.P("11/04/2023"),
            html.H6("Correo contacto:"),
            html.Div(html.A("michael.fresneda@colsubsidio.com",href ="mailto:michfrec@colsubsidio.com")),                               
            html.Div(html.A("solicitudes_bi@colsubsidio.com",href ="mailto:solicitudes_bi@colsubsidio.com")),
            ], width=3)
            ], style = {'margin-top':'7px'})
            ], style = {'margin-left':'5px', 'margin-top':'7px', 'margin-right':'5px'}), style={'display':'block'}, id="Pagina1"),

html.Div([
    dbc.Button("Regresar", id='IrPagina1', outline=True, color="primary", 
        style={'margin-left':'800px','margin-top':'10px','align':'rigth'}),
    dbc.Row(
        dbc.Input(id="input-value", placeholder="Digite solicitud...", type='number'), justify="center", 
        style={'width':'300px','heigth':'50px'}),
    html.Br(),
    dbc.Row(
        dbc.Button(id="submit-button", children="Buscar"), justify="center",
        style={'width':'300px','heigth':'50px'}),
    html.Br(),
    dbc.Row(
        html.Div(id="output-container")),
    ], 
      style = {'margin-left':'20px', 'margin-top':'20px', 'margin-right':'20px', 'margin-bottom':'20px', 'display':'none'}, id="Pagina2")
], style={'margin-left':'20px', 'margin-top':'20px', 'margin-right':'20px', 'margin-bottom':'20px'}, className="shadow p-3 mb-5 bg-white rounded")


@callback(
    Output(component_id='output-container', component_property='children'),
    Input(component_id='submit-button', component_property='n_clicks'),
    [State(component_id="input-value",component_property="value")]
)

def search(n_clicks, input_value):
    filtered_df = df[df['SOLICITUD'] == input_value]
    table = dbc.Table.from_dataframe(filtered_df, striped=True, bordered=True, hover=True)
    return table

@callback(
    [Output('Pagina1', 'style'),
    Output('Pagina2', 'style')],
    [Input('IrPagina1', "n_clicks"),
     Input('IrPagina2', "n_clicks")],
    prevent_initial_call=True
)

def cambiar_tablero(ir,volver):
    global contador1, contador2
    if contador1 != ir:
        contador1=ir
        return {'display': 'block'},{'display': 'none'}
    if contador2 != volver:
        contador2 = volver
        return {'display': 'none'},{'display': 'block'}

def plantilla ():
    return 

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
