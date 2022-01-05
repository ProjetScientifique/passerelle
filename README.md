Install Mosquitto Broker MQTT (machin eclipse)
Install Telegraf + launch via powershell (./telegraf.exe --config fichier.confg ==> besoin de faire un fichier de conf)
Install InfluxDB + launch via powershell (./influxd.exe et config sur le lien localhost:8086) 
Install Grafana et config sur le lien localhost:3000

Puis pour conf entre les trucs faut faire à la main :
    - Ajout de la config mqtt sur le conf de telegraf (voir fichier pts.conf sur mon pc portable)
    - Requête sur InfluxDB pour avoir le script de requête
    - Copier coller sur Grafana après avoir config InfluxDB comme source de Data