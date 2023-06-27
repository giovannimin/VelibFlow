#!/usr/bin/env bash
set -e
set -o pipefail

# Vérifie si la variable d'environnement $GITHUB_TOKEN est définie
if [ -z "$GITHUB_TOKEN" ]
then
  echo "Missing \$GITHUB_TOKEN"
  exit 1
fi

# Crée une archive zip contenant le fichier update_data.csv
zip -r velib_data.zip update_data.csv

# URL de l'API GitHub pour le référentiel cible
GAPI=https://api.github.com/repos/giovannimin/VelibFlow

# En-tête d'autorisation pour les requêtes API GitHub
AUTH="-HAuthorization: token $GITHUB_TOKEN"

# Fichier temporaire pour stocker les informations sur la dernière version de sortie
LAST_RELEASE_JSON=$(mktemp)

# Télécharge les informations sur la dernière version de sortie de l'API GitHub
echo "Downloading last release information"
curl -sS "$AUTH" "$GAPI/releases/latest" > "$LAST_RELEASE_JSON"

# Récupère l'URL de téléchargement de la dernière version de l'API GitHub
UPLOAD_URL=$(
    < "$LAST_RELEASE_JSON" \
    jq -r '.upload_url' |
    sed 's/{.*}//'
)

# Télécharge la nouvelle version de l'archive zip sur GitHub
echo "Uploading new version"
NEW_ASSET_ID=$(
  curl -sS --fail "$AUTH" \
    --retry 7 --retry-delay 0 \
    -H "Content-Type: application/zip" \
    "$UPLOAD_URL?name=velib_data-$(date -u +"%Y-%m-%dT%H%MZ").zip" \
    --data-binary "@velib_data.zip" |
  jq -r '.id'
)

# Supprime l'ancienne ressource (asset) de la version précédente
echo "Removing old release asset"
curl -sS -XDELETE "$AUTH" \
  "$GAPI/releases/assets/$(
      <"$LAST_RELEASE_JSON" \
      jq -r '.assets[]|select(.name == "velib_data.zip")|.id'
  )"

# Renomme le fichier de la nouvelle ressource (asset)
echo "Renaming asset file"
curl -sS --fail --retry 7 --retry-delay 0 -XPATCH "$AUTH" \
  "$GAPI/releases/assets/$NEW_ASSET_ID" \
  --data-binary "{\"name\":\"velib_data.zip\",\"label\":\"Latest data per station as of $(date)\"}"

# Nettoie le fichier temporaire contenant les informations sur la dernière version de sortie
rm "$LAST_RELEASE_JSON"