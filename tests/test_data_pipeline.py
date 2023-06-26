# -*- coding: utf-8 -*-
"""
Created on 26/06/2023 18:54
@author: GiovanniMINGHELLI
"""
import pytest
from sources.data_pipeline import make_request


@pytest.mark.parametrize("url", ["https://velib-metropole-opendata.smoove.pro/opendata/Velib_Metropole"
                                 "/station_information.json",
                                 "https://velib-metropole-opendata.smoove.pro/opendata/Velib_Metropole/station_status"
                                 ".json"])
def test_make_requests(url):
    assert make_request(path=url).status_code == 200
