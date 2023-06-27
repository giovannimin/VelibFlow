# -*- coding: utf-8 -*-
"""
Created on 27/06/2023 19:13
@author: GiovanniMINGHELLI
"""
import os

from sources.data_pipeline import get_availablity_bikes


def fetch():
    velib_data = get_availablity_bikes()
    velib_data.to_csv('update_data.csv', header=False, mode='a', date_format='%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    fetch()
