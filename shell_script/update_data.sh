#!/usr/bin/env bash

set -e

# Télécharge l'historique des données
bash -x ./download_history.sh

# Effectue la récupération des nouvelles données
python3 ./sources/fetch_data.py

# Met à jour la release sur GitHub
bash -x ./update_release.sh