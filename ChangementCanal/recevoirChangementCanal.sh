#!/bin/bash

# Vérifie le nombre d'arguments donnés
if [[ $# -ne 2 ]]; then
    echo "Usage : ./recevoirChangementCanal.sh <chemin> <adresse_ip>"
    exit 1
fi

# Définit les chemins vers les fichiers nécessaires
path=$1  # Chemin du répertoire contenant les scripts
chemin_complet="$path/ChangementCanal/receptionChangementCanal.py"  # Chemin du script Python de réception du changement de canal
ip=$2  # Adresse IP cible
LOG_FILE="$HOME/receptionCanal.log"  # Fichier de log pour suivre l'exécution

# Log l'événement de démarrage du script
echo "$(date "+%Y-%m-%d %H:%M:%S") Début de l'exécution du changement de canal" >> "$LOG_FILE"

# Exécute le script Python pour récevoir et appliquer le changement de canal et log la sortie
python3 "$chemin_complet" "$ip" "$path" >> "$LOG_FILE" 2>&1

