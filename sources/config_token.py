# -*- coding: utf-8 -*-
"""
Created on 26/06/2023 15:18
@author: GiovanniMINGHELLI
"""
import os


def token():
    project_path = os.getcwd()
    while os.path.basename(project_path) != "VelibFlow":
        project_path = os.path.dirname(project_path)
        os.chdir(project_path)
    if os.path.exists("token.txt"):
        with open("token.txt", "r") as file:
            return file.read()
    return print("VelibFlow/token.txt does not exist, could get one here :  https://plotly.com/.")


if __name__ == '__main__':
    token()
