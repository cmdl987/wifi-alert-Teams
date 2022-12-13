import subprocess
import platform

import requests

class WifiDetector:
    def __init__(self, data_config):
        self.selected_SSID = ""
        self.selected_time = ""
        self.selected_webhook = ""
        self.OS = self.os_detector()
        self.get_data_config(data_config)
        self.network_file = ""
        self.network_list = []
        self.SSID_list = []
        self.webhook = webhook 
        self.title = "ALARMA WIFI"
        self.content = """
            Ojito, el simulador está  <i>encendido</i>.<br>
            😍
            """
        #self.create_networks_file()

    def os_detector(self):
        """
        Comprueba el sistema operativo sobre el que se está ejecutando el
        módulo.
        """
        return platform.system()


    def detect_networks(self):
        """
        Obtiene información de las redes detectadas por el equipo,
        según el SO pasado en la clase.
        """
        if self.OS == "Linux":
            networks_info = subprocess.check_output(["nmcli", "dev", "wifi"])
            networks_info = networks_info.decode("utf-8", errors="ignore")            
        else:
            networks_info = subprocess.check_output(['netsh', 'wlan', 'show', "networks"])
            networks_info = networks_info.decode("utf-8", errors="ignore")
        return networks_info


    def network_detector(self):
        """
        Llama a la función detect_networks() para obtener toda la información 
        de redes, de la cual obtener el nombre de los SSID y guardarlos
        en la lista network_list.
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


    def get_data_config(self, data_config):
        self.selected_SSID = data_config[0]
        self.selected_time = data_config[1]
        self.selected_webhook = data_config[2]
        
    
    def get_data_config(self):
        """
        Devuelve en pantalla los resultados para la última configuración cargada.
        """
        print("-"*70)
        print("ÚLTIMA CONFIGURACIÓN USADA")
        print("\tSSID: {ssid}\tAlarma: {alarm}\tWebhook: {webh}".format(
                                ssid=self.selected_SSID,
                                alarm=self.selected_time,
                                webh="..."+self.selected_webhook[:-5]
                                ))
        print("-"*70)


    def get_networks_info(self):
        print("Se han detectado {} redes wi-fi:".format(len(self.network_detector)))
        for index, ssid in enumerate(self.network_list):
            print("\t", index, "\t", ssid)

 

    def send_teams(self, webhook_url:str, content:str, title:str, color:str="000000") -> int:
        response = requests.post(
            url=webhook_url,
            headers={"Content-Type": "application/json"},
            json={
                "themeColor": color,
                "summary": title,
                "sections": [{
                    "activityTitle": title,
                    "activitySubtitle": content
                }],
            },
        )
        return response.status_code   # Debe ser 200


    def check_network(self, target_network):
        """
        Tras detectar las redes existentes, comprueba que nuestras redes objetivo
        estén en la lista de redes detectadas. De ser correcto, envía mensaje
        por teams. 
        """
        self.network_detector()
        if target_network in self.network_list:
            print("La red {} se encuentra conectada!".format(target_network))
            self.send_teams(self.webhook, self.content, self.title)



#####
#TEST
#####
webhook = "https://myuax.webhook.office.com/webhookb2/2ef9a78a-7c32-49da-be6d-5fc4968811cd@8344d72d-e21b-485a-b9a1-52078e79010e/IncomingWebhook/43d6a479f4cb4db0842af2fd763b690b/14d96f44-0bf8-4c09-859d-68edc4681dd5"
file_path = "/home/cmdl987/GitHub/wifi-alarm/redes.txt"
launcher = WifiDetector("Linux", file_path, webhook)    
wifi_networks = launcher.list_generator()
launcher.get_networks_info()
launcher.check_network("MMP0366")