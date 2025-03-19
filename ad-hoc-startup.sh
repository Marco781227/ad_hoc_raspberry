#!/bin/bash
if [[ $# -ne 2 ]] 
then
	echo "Usage : ./ad_hoc_startup <channel wifi> <ip ad_hoc>"
	exit 1
fi

sudo systemctl stop NetworkManager
sudo ip link set wlan0 down
sudo iwconfig wlan0 mode ad-hoc
sudo iwconfig wlan0 essid "ama"
sudo iwconfig wlan0 channel $1
sudo ifconfig wlan0 $2 netmask 255.255.255.0 up
sudo iwconfig
echo "Connection ad-hoc au channel $1 à l'adresse ip $2 effectuée"
exit 0
