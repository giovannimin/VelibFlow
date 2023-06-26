# -*- coding: utf-8 -*-
"""
Created on 26/06/2023 15:26
@author: GiovanniMINGHELLI
"""
from sources.config_token import token
from sources.data_pipeline import get_availablity_bikes
import plotly.express as px
import pandas as pd


def show_map(dataset: pd.DataFrame = get_availablity_bikes(), color_by: str = 'availableBikesRate'):
    px.set_mapbox_access_token(token())
    fig = px.scatter_mapbox(dataset, lat="lat", lon="lon", color=color_by,
                            color_continuous_scale=px.colors.sequential.Brwnyl, size_max=15, zoom=9.5,
                            range_color=(0, 100))
    fig.show()
