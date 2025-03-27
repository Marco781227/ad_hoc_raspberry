if [[ $# -ne 2 ]]
then
	echo "Usage : ./recevoirChangementCanal.sh <chemin> <adresse ip>"
fi

chemin_complet="$1/ChangementCanal/receptionChangementCanal.py"
ip=$2
LOG_FILE="$HOME/receptionCanal.log"

python3 "$chemin_complet" $ip >> "$LOG_FILE" 2>&1 
