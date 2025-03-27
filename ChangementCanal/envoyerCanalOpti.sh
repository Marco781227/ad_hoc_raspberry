if [[ $# -ne 2 ]]
then
	echo "Usage : ./envoyerCanalOpti.sh <adresse ip>"
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
commEnCours="sudo lsof -i -P -n | grep -q $ip"
nbRepetitions=0
LOG_FILE="$HOME/changementCanal.log"

if !(eval "$commEnCours")
then
	sleep 1
	echo "$(date "+%Y-%m-%d %H:%M:%S") Début de l'execution du changement de canal" >> "$LOG_FILE"
	python3 "$chemin_complet" "$bestChannel" "$ip" "$path" >> "$LOG_FILE" 2>&1
	exit 0
fi

echo "ok"
exit 1
