bestChannel=$(sudo iwlist wlan0 scan | grep Channel: | grep -Eo '([1,6,11])'| sort | uniq -c | sort -n | head -1 | awk '{print $2}')
ip=$1
commEnCours="sudo lsof -i -P -n | grep -q $ip"
nbRepetitions=0

while [ $nbRepetitions -ne 15 ] 
do
	if !(eval "$commEnCours")
	then
		python3 ~/Documents/tp_rsf/ChangementCanal/envoiChangementCanal.py $bestChannel $ip
		exit 0
	fi
	sleep 1
	((nbRepetitions++))
done
exit 1
