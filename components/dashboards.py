from dash import html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar
from globals import *
from app import app

from dash_bootstrap_templates import template_from_url, ThemeChangerAIO

card_icon = {
    "color": "white",
    "textAlign": "center",
    "fonteSize": 30,
    "margin": "auto",
}

graph_margin=dict(l=25, r=25, t=25, b=0)

# =========  Layout  =========== #
layout = dbc.Col([
    dbc.Row([

    # Saldo Total    
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend("Saldo"),
                    html.H5("R$ -", id="p-saldo-dashboards"),
                ], style={"padding-left": "20px", "padding-top": "10px"}),

                dbc.Card(
                    html.Div(className="fa fa-university", style=card_icon),
                    color="warning",
                    style={"maxWidth": 75, "height": 100, "margin-left": "-10px"},                        
                )])
        ], width=4),

    # Receita Total    
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend("Receita"),
                    html.H5("R$ -", id="p-receita-dashboards"),
                ], style={"padding-left": "20px", "padding-top": "10px"}),

                dbc.Card(
                    html.Div(className="fa fa-smile-o", style=card_icon),
                    color="success",
                    style={"maxWidth": 75, "height": 100, "margin-left": "-10px"},                        
                )])
        ], width=4),

    # Despesas Total    
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend("Despesas"),
                    html.H5("R$ -", id="p-despesa-dashboards"),
                ], style={"padding-left": "20px", "padding-top": "10px"}),

                dbc.Card(
                    html.Div(className="fa fa-meh-o", style=card_icon),
                    color="danger",
                    style={"maxWidth": 75, "height": 100, "margin-left": "-10px"},                        
                )])
        ], width=4),  
    
    ], style={"margin": "10px"}),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                    html.Legend("Filtrar lançamentos", className="card-title"),
                    html.Label("Categorias de receitas"),
                    html.Div(
                        dcc.Dropdown(
                            id="dropdown-receita",
                            clearable=False,
                            style={"width": "100%"},
                            persistence=True,
                            persistence_type="session",
                            multi=True)
                    ),
                        
                    html.Label("Categorias de despesas", style={"margin-top": "10px"}),
                    dcc.Dropdown(
                        id="dropdown-despesa",
                        clearable=False,
                        style={"width": "100%"},
                        persistence=True,
                        persistence_type="session",
                        multi=True
                    ),

                    html.Legend("Período de Análise", style={"margin-top": "10px"}),
                    dcc.DatePickerRange(
                        month_format='Do MMM, YY',
                        end_date_placeholder_text='Data...',
                        start_date=datetime.today(),
                        end_date=datetime.today() + timedelta(days=31),
                        with_portal=True,
                        updatemode='singledate',
                        id='date-picker-config',
                        style={'z-index': '100'})],
                    style={'height': '100%', 'padding': '20px'}),        
        ], width=4),

        dbc.Col(
            dbc.Card(dcc.Graph(id='graph1'), style={'height': '100%', 'padding': '10px'}), width=8
        )
    ], style={'margin': '10px'}),

    dbc.Row([
        dbc.Col(dbc.Card(dcc.Graph(id='graph2'), style={'padding': '10px'}), width=6),
        dbc.Col(dbc.Card(dcc.Graph(id='graph3'), style={'padding': '10px'}), width=3),
        dbc.Col(dbc.Card(dcc.Graph(id='graph4'), style={'padding': '10px'}), width=3),    
    ])
])

# =========  Callbacks  =========== #
# Dropdown Receita
@app.callback([Output("dropdown-receita", "options"),
               Output("dropdown-receita", "value"),
               Output("p-receita-dashboards", "children")],
               Input("store-receitas", "data"))
def populate_dropdownvalues(data):
    df = pd.DataFrame(data)
    valor = df['Valor'].sum()
    val = df.Categoria.unique().tolist()

    return ([{"label": x, "value": x} for x in val], val, f"R$ {valor}")

# Dropdown despesas               
@app.callback([Output("dropdown-despesa", "options"),
               Output("dropdown-despesa", "value"),
               Output("p-despesa-dashboards", "children")],
               Input("store-despesas", "data"))
def populate_dropdownvalues(data):
    df = pd.DataFrame(data)
    valor = df['Valor'].sum()
    val = df.Categoria.unique().tolist()

    return ([{"label": x, "value": x} for x in val], val, f"R$ {valor}")

# VALOR - saldo
@app.callback(
    Output("p-saldo-dashboards", "children"),
    [Input("store-despesas", "data"),
    Input("store-receitas", "data")])
def saldo_total(despesas, receitas):
    df_despesas = pd.DataFrame(despesas)
    df_receitas = pd.DataFrame(receitas)

    valor = df_receitas['Valor'].sum() - df_despesas['Valor'].sum()

    return f"R$ {valor}"

# Gráfico 1
@app.callback(
    Output('graph1', 'figure'),

    [Input('store-despesas', 'data'),
    Input('store-receitas', 'data'),
    Input("dropdown-despesa", "value"),
    Input("dropdown-receita", "value"),]
)
def update_output(data_despesa, data_receita, despesa, receita):
    df_despesas = pd.DataFrame(data_despesa).set_index("Data")[["Valor"]]
    df_ds = df_despesas.groupby("Data").sum().rename(columns={"Valor": "Despesa"})

    df_receitas = pd.DataFrame(data_receita).set_index("Data")[["Valor"]]    
    df_rc = df_receitas.groupby("Data").sum().rename(columns={"Valor": "Receita"})

    df_acum = df_ds.join(df_rc, how="outer").fillna(0)
    df_acum["Acum"] = df_acum["Receita"] - df_acum["Despesa"]
    df_acum["Acum"] = df_acum["Acum"].cumsum()

    fig = go.Figure()

    fig.add_trace(go.Scatter(name="Fluxo de caixa", x=df_acum.index, y=df_acum["Acum"], mode="lines"))

    fig.update_layout(margin=graph_margin, height=400)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')

    return fig