if [[ $# -ne 2 ]]
then
	echo "Usage : ./recevoirChangementCanal.sh <chemin> <adresse ip>"
fi

path=$1
chemin_complet="$path/ChangementCanal/receptionChangementCanal.py"
ip=$2
LOG_FILE="$HOME/receptionCanal.log"

echo "$(date+%Y-%m-%d %H:%M:%S") Début de l'execution du changement de canal" >> "$LOG_FILE"
python3 "$chemin_complet" "$ip" "$path" >> "$LOG_FILE" 2>&1 
