import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app

from datetime import datetime, date
import plotly.express as px
import numpy as np
import pandas as pd






# ========= Layout ========= #
layout = dbc.Col([
                html.H1("MyBudget", className="text-primary"),
                html.P("by Ésley(ASIMOV)", className="text-info"),
                html.Hr(),

    # Seção de PERFIL ---------------
                dbc.Button(id='botao_avatar',
                    children=[html.Img(src='/assets/img_hom.png', id='avatar_change', alt='Avatar', className='perfil_avatar')
                ], style={'background-color': 'transparent', 'border-color': 'transparent'}),


    # Seção de BOTOES --------------- 
                dbc.Row([
                    dbc.Col([
                        dbc.Button(color='success', id='open-novo-receita',
                                children=['+ Receita'])
                    ], width=6),

                    dbc.Col([
                        dbc.Button(color='danger', id='open-novo-despesa',
                                children=['- Despesa'])
                    ], width=6)
                ]),

                # Modal Receita
                dbc.Modal([
                    dbc.ModalHeader(dbc.ModalTitle('Adicionar receita')),
                    dbc.ModalBody([

                    ])
                ], id='modal-novo-receita'),

                # Modal Despesa
                dbc.Modal([
                    dbc.ModalHeader(dbc.ModalTitle('Adicionar despesa')),
                    dbc.ModalBody([

                    ])
                ], id='modal-novo-despesa'),

    # Seção NAV --------------- 

                html.Hr(),
                dbc.Nav(
                [
                    dbc.NavLink("Dashboard", href="/dashboards", active="exact"),
                    dbc.NavLink("Extratos", href="/extratos", active="exact"),
                ], vertical=True, pills=True, id='nav_buttons', style={"margin-bottom": "50px"}),

                ])


# =========  Callbacks  =========== #
# Pop-up receita
@app.callback(
    Output('modal-novo-receita', 'is_open'),
    Input('open-novo-receita', 'n_clicks'),
    State('modal-novo-receita', 'is_open')
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    
# Pop-up despesa
@app.callback(
    Output('modal-novo-despesa', 'is_open'),
    Input('open-novo-despesa', 'n_clicks'),
    State('modal-novo-despesa', 'is_open')
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open