if [[ $# -ne 2 ]]
then
	echo "Usage : ./envoyerCanalOpti.sh <adresse ip>"
	exit 1
fi
bestChannel=$(sudo iwlist wlan0 scan | grep Channel: | grep -Eo '([1,6,11])'| sort | uniq -c | sort -n | head -1 | awk '{print $2}')
path="$1"
ip=$2
chemin_complet="$path/ChangementCanal/envoiChangementCanal.py"
commEnCours="sudo lsof -i -P -n | grep -q $ip"
nbRepetitions=0
LOG_FILE="$HOME/changementCanal.log"

while [ $nbRepetitions -ne 15 ] 
do
	if !(eval "$commEnCours")
	then
		echo "$(date "+%Y-%m-%d %H:%M:%S") Début de l'execution du changement de canal" >> "$LOG_FILE"
		python3 "$chemin_complet" "$bestChannel" "$ip" "$path" >> "$LOG_FILE" 2>&1
		echo "hello"
		exit 0
	fi
	sleep 1
	((nbRepetitions++))
done
echo "ok"
exit 1
