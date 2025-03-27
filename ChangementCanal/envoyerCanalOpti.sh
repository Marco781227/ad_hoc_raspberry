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

echo $chemin_complet
while [ $nbRepetitions -ne 15 ] 
do
	if !(eval "$commEnCours")
	then
		echo "hello"
		python3 "$chemin_complet" "$bestChannel" "$ip" >> "$LOG_FILE" 2>&1
		exit 0
	fi
	sleep 1
	((nbRepetitions++))
done
echo "ok"
exit 1
