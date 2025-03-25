if [[ $# -ne 1 ]]
then
	echo "Usage : ./envoyerCanalOpti.sh <adresse ip>"
fi
bestChannel=$(sudo iwlist wlan0 scan | grep Channel: | grep -Eo '([1,6,11])'| sort | uniq -c | sort -n | head -1 | awk '{print $2}')
ip=$1
commEnCours="sudo lsof -i -P -n | grep -q $ip"
nbRepetitions=0
LOG_FILE="$HOME/changementCanal.log"

while [ $nbRepetitions -ne 15 ] 
do
	if !(eval "$commEnCours")
	then
		python3 ~/Documents/tp_rsf/ChangementCanal/envoiChangementCanal.py $bestChannel $ip >> "$LOG_FILE" 2>&1
		exit 0
	fi
	sleep 1
	((nbRepetitions++))
done
echo "ok"
exit 1
