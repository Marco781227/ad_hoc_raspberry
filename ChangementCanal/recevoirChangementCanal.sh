if [[ $# -ne 1 ]]
then
	echo "Usage : ./recevoirChangementCanal.sh <adresse ip>"
fi

python3 ~/Desktop/projet/ad_hoc_raspberry/ChangementCanal/receptionChangementCanal.py $1 >> /home/m1info20/receptionChangementCanal.log 2>&1
