#!/bin/bash

# Vérifie si le bon nombre d'arguments est donné
if [[ $# -ne 2 ]]; then
    echo "Usage : ./envoyerCanalOpti.sh <chemin_vers_executable> <adresse_ip>"
    exit 1
fi

# Recherche des canaux utilisés sur wlan0 et trie les résultats pour déterminer les moins utilisés par le 1, 6 et 11
sortedChannels=$(sudo iwlist wlan0 scan | grep Channel: | grep -Eo '([1,6,11])' | sort | uniq -c | sort -n | awk '{print $2}')

# Sélectionne le canal le moins occupé
bestChannel=$(echo "$sortedChannels" | head -1)

# Vérifie si l'un des canaux (1, 6, 11) n'est pas utilisé, et le sélectionne en priorité
for ch in 1 6 11; do
    if ! echo "$sortedChannels" | grep -q "$ch"; then
        bestChannel=$ch
    fi
done

path="$1"  # Chemin vers le répertoire contenant les script
ip=$2  # Adresse IP cible
chemin_complet="$path/ChangementCanal/envoiChangementCanal.py"  # Chemin du script Python d'envoi et changement de canal
LOG_FILE="$HOME/changementCanal.log"  # Fichier de log pour suivre l'exécution

# Vérifie s'il y a des communications en cours sur l'adresse IP cible
commEnCours=$(sudo lsof -i -P -n | grep -q $ip)

if [[ $? -ne 0 ]]; then  # Si aucune communication en cours
    sleep 1  # Pause pour laisser le temps aux récepteurs d'écouter sur le socket
    echo "$(date "+%Y-%m-%d %H:%M:%S") Début de l'exécution du changement de canal" >> "$LOG_FILE" # Renseigne la date et l'heure pour le log
    
    # Exécute le script Python pour appliquer le changement de canal et log la sortie
    python3 "$chemin_complet" "$bestChannel" "$ip" "$path" >> "$LOG_FILE" 2>&1 
    exit 0
else
    # Si une communication est détectée, annule le changement et log l'événement
    echo "$(date "+%Y-%m-%d %H:%M:%S") Communication déjà en cours, annulation du changement de canal" >> "$LOG_FILE"
fi

exit 1  # Sortie avec code d'erreur si le changement de canal n'a pas pu être effectué

