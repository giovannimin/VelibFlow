#!/usr/bin/env bash

set -e

base="https://api.github.com/repos/giovannimin/VelibFlow/releases/latest"

# Récupère les URL de téléchargement des fichiers depuis l'API GitHub
urls=$(
    curl --fail --retry 8 --retry-delay 0 "$base" |
    jq -r '.assets|sort_by(.updated_at)|reverse[]|.browser_download_url'
)

outfile=velib_data.zip

# Parcourt les URLs de téléchargement jusqu'à trouver un fichier valide
for url in $urls; do
    # Télécharge le fichier ZIP depuis l'URL
    curl --location --fail --retry 8 --retry-delay 0 --output "$outfile" "$url" &&
    # Décompresse le fichier ZIP
    unzip -o $outfile &&
    # Sort de la boucle si le téléchargement et la décompression ont réussi
    break || continue
done

# Supprime le fichier ZIP
rm $outfile