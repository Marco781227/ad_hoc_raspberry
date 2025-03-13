bestChannel=$(sudo iwlist wlan0 scan | grep Channel: | grep -Eo '([1,6,11])'| sort | uniq -c | sort -n | head -1 | awk '{print $2}')
ip=$1
python3 /home/marco/Documents/tp_rsf/envoiChangementCanal.py $bestChannel $ip

