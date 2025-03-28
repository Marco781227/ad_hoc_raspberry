if [[ $# -ne 2 ]]
then
	echo "Usage : ./envoyerCanalOpti.sh <chemin_vers_executable> <adresse ip>"
	exit 1
fi

sortedChannels=$(sudo iwlist wlan0 scan | grep Channel: | grep -Eo '([1,6,11])'| sort | uniq -c | sort -n | awk '{print $2}')

bestChannel=$(echo "$sortedChannels" | head -1)

for ch in 1 6 11; do
	if ! echo "$sortedChannels" | grep -q "$ch"; then
		bestChannel=$ch
	fi
done

path="$1"
ip=$2
chemin_complet="$path/ChangementCanal/envoiChangementCanal.py"
LOG_FILE="$HOME/changementCanal.log"

#Si il n'y a pas de communications en cours on peut changer le canal
commEnCours=$(sudo lsof -i -P -n | grep -q $ip)
if [[ $? -ne 0 ]]; then
	sleep 1
	echo "$(date "+%Y-%m-%d %H:%M:%S") Début de l'execution du changement de canal" >> "$LOG_FILE"
	python3 "$chemin_complet" "$bestChannel" "$ip" "$path" >> "$LOG_FILE" 2>&1
	exit 0

else
	echo "$(date "+%Y-%m-%d %H:%M:%S") Communication déjà en cours annulation du changement de canal" >> "$LOG_FILE"
fi

exit 1
