'''
2) LOS VALORES DEL CONTENT (MENSAJE A ENVIAR POR TEAMS) QUIERO QUE ESTÉ EN 
UN ARCHIVO .TXT, PARA QUE SE PUEDA EDITAR Y LEER DIRECTAMENTE DESDE AHÍ.
OJO CON LOS VALORES DE VARIABLES, PARA NOMBRAR LAS REDES {}. 
HAY QUE HACER PRUEBAS.
'''


import subprocess
import platform
import json
import warnings

from apscheduler.schedulers.blocking import BlockingScheduler
import requests

warnings.filterwarnings("ignore")

class TeamsWebhookException(Exception):
    """
    Excepción propia para obtener error tras fallo en llamada a nuestro
    webhook. Aparece cuando la respuesta del requests.post es diferente a 200.
    """

class WifiDetector:
    def __init__(self, data_config):
        self.selected_SSID = data_config["last_SSID"]
        self.selected_time = data_config["last_time_config"]
        self.selected_webhook = str(data_config["last_webhook"]).strip()
        self.target_ssid = ""
        self.content = None
        self.network_list = []
        self.SSID_list = []

      
    def set_content(self, target_ssid):
        """
        Lee el contenido de content.json, donde se encuentra la información
        del mensaje que se va a enviar a través del grupo de Teams.
        """
        with open ("content.json", "r") as file:
            content = json.load(file)
        
        # Checks the target SSID and change the title for every given SSID.
        if target_ssid == "Wifi-Prof":           #"MMP0366":
            content["sections"][0]["activityTitle"] = "El simulador **METI** está encendido."
            content["sections"][0]["activityImage"] = "https://i.imgur.com/2kLtKTy.jpg"

        elif target_ssid == "RV":                  #"mfs2135":
            content["sections"][0]["activityTitle"] = "El simulador **LUCINA** está encendido."
            content["sections"][0]["activityImage"] = "https://i.imgur.com/Z7wwX6l.jpg."
            
        content["sections"][0]["facts"][0]["value"] = target_ssid
        print("*"*50)
        print(content)
        print("*"*50)
        return content

    def detect_networks(self):
        """
        Obtiene información de las redes detectadas por el equipo,
        según el sistema operativo.
        """
        user_OS = platform.system()
        if user_OS == "Linux":
            networks_info = subprocess.check_output(["nmcli", "dev", "wifi"])
            networks_info = networks_info.decode("utf-8", errors="ignore")            
        else:
            networks_info = subprocess.check_output(['netsh', 'wlan', 'show', "networks"])
            networks_info = networks_info.decode("utf-8", errors="ignore")
        return networks_info

    def tolist_network(self):
        """
        Llama a la función detect_networks() para obtener toda la información 
        de redes, de la cual generar una lista con todos los nombres de los SSID.
        Devuelve una lista.
        """
        networks = self.detect_networks().splitlines()
        # Itera por cada línea de la variable networks para guardar el SSID.
        for ssid_line in networks:
            if "BSSID" not in ssid_line and "--" not in ssid_line:
                ssid = ssid_line.replace("*", "").split()
                self.network_list.append(ssid[1])
        # Eliminamos posibles duplicados (diferentes AP con misma red).
        self.network_list = list(set(self.network_list))
        return self.network_list

          
    def __str__(self):
        """
        Devuelve en pantalla los resultados para la última configuración cargada.
        """
        print("-"*70)
        print("ÚLTIMA CONFIGURACIÓN USADA")
        print("\tSSID: {ssid}\tAlarma: {alarm}\tWebhook: {webh}".format(
                                ssid=self.selected_SSID,
                                alarm=self.selected_time,
                                webh="..."+self.selected_webhook[-10:]
                                ))
        print("-"*70)

    def get_networks_info(self):
        """
        Muestra en pantalla las redes wi-fi detectadas.
        """
        self.tolist_network()
        print("Se han detectado {} redes wi-fi:".format(len(self.network_list)))
        for index, ssid in enumerate(self.network_list):
            print("\t", index, "\t", ssid)

    def send_teams(self, webhook, content):
        """
        Ejecuta el envío del aviso por Teams, a partir de los parámetros de clase
        self.selected_webhook y self.content.        
        """ 
        response = requests.post(
            url=webhook,
            headers={"Content-Type": "application/vnd.microsoft.card.hero"},
            json=content,
            )
        if response.status_code == 200:
            return True
        else: 
            raise TeamsWebhookException(response.reason)

    def check_network(self):
        """
        Tras detectar las redes existentes, comprueba que nuestras redes objetivo
        estén en la lista de redes detectadas. De ser correcto, envía mensaje
        por teams. 
        """
        ssid_list = self.tolist_network()
        for target_ssid in self.selected_SSID:
            if target_ssid in ssid_list:
                print(f"La red {target_ssid} se encuentra conectada!")
                self.send_teams(self.selected_webhook, self.set_content(target_ssid))

            else:
                print(f"No se han encontrado la red {target_ssid}")

    def run_scheduler(self):
        """
        Método que ejecuta la tarea en el tiempo indicado.
        """
        selected_hour = int(self.selected_time[:2])
        selected_min = int(self.selected_time[-2:])
        scheduler = BlockingScheduler()
        scheduler.add_job(self.check_network, "cron", 
                        hour=selected_hour, 
                        minute=selected_min,
                        )
        print(f"Scheduler running. Next check: {self.selected_time}.")
        scheduler.start()