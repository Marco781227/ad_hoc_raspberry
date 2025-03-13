"""
import gps

session = gps.gps(mode=gps.WATCH_ENABLE)
#gpsd.connect()


try :
	while True :
		report = session.next()
		if report['class']=='TPV':
			latitude = getattrr(report, 'lat', "N/A")
			longitude = getattrr(report, 'lon', "N/A")
			altitude = getattrr(report, 'alt', "N/A")
			print(f"Latitude : {latitude}, Longitude : {longitude}, Altitude : {altitude}")
except KeyboardInterrupt:
	print("Arrêt du script GPS")
"""


import gpsd

#session = gps.gps(mode=gps.WATCH_ENABLE)
gpsd.connect()


try :
	while True :
		packet = gpsd.get_current()
		if packet.mode >=2:
			latitude, longitude = packet.position()
			altitude = packet.altitude()
			print(f"Latitude : {latitude}, Longitude : {longitude}, Altitude : {altitude}")
		else :
			print(f"aucune donnée GPS reçue")
			
except KeyboardInterrupt:
	print("Arrêt du script GPS")
