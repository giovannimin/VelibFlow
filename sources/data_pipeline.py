# -*- coding: utf-8 -*-
"""
Created on 26/06/2023 14:52
@author: GiovanniMINGHELLI
"""
import pandas as pd
import requests


def get_availablity_bikes():
    # Requêtes API Velib
    stations_information_response = requests.get('https://velib-metropole-opendata.smoove.pro/opendata'
                                                 '/Velib_Metropole/station_information.json')
    stations_status_response = requests.get('https://velib-metropole-opendata.smoove.pro/opendata/Velib_Metropole'
                                            '/station_status.json')
    stations_information = pd.DataFrame(stations_information_response.json()['data']['stations'])
    stations_status = pd.DataFrame(stations_status_response.json()['data']['stations'])

    # Fonction pour extraire les valeurs entières des dictionnaires
    def extract_integer(dictionary_list, key):
        for dictionary in dictionary_list:
            if key in dictionary:
                return dictionary[key]
        return None

    # Extraction des valeurs entières pour les colonnes "mechanical" et "ebike"
    stations_status['mechanical'] = stations_status['num_bikes_available_types'].apply(lambda x:
                                                                                       extract_integer(x, 'mechanical'))
    stations_status['ebike'] = stations_status['num_bikes_available_types'].apply(lambda x: extract_integer(x, 'ebike'))

    # Suppression de la colonne d'origine
    stations_status.drop('num_bikes_available_types', axis=1, inplace=True)

    # Conversion en entier des codes station StationCode
    stations_status['stationCode'] = stations_status['stationCode'].astype(int)
    stations_information['stationCode'] = stations_information['stationCode'].astype(int)

    # Merge des deux tables
    stations = stations_information.merge(stations_status, on=['station_id', 'stationCode'])

    # Conversion d'un timestamp en datetime
    stations['last_reported'] = pd.to_datetime(stations['last_reported'], unit='s')

    # Creation de KPIs
    stations['availableBikesRate'] = (stations['numBikesAvailable'] / stations['capacity']) * 100
    stations['availableDocksRate'] = (stations['numDocksAvailable'] / stations['capacity']) * 100
    stations['availableMechanicalBikesRate'] = (stations['mechanical'] / stations['capacity']) * 100
    stations['availableElectricRate'] = (stations['ebike'] / stations['capacity']) * 100

    # Remplacement des NaN par 0 dans les colonnes KPIs
    stations['availableBikesRate'] = stations['availableBikesRate'].fillna(0)
    stations['availableDocksRate'] = stations['availableDocksRate'].fillna(0)
    stations['availableMechanicalBikesRate'] = stations['availableMechanicalBikesRate'].fillna(0)
    stations['availableElectricRate'] = stations['availableElectricRate'].fillna(0)

    return stations


if __name__ == '__main__':
    stations_table = get_availablity_bikes()
