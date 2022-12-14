import subprocess
import platform

from apscheduler.schedulers.blocking import BlockingScheduler
import requests

class WifiDetector:
    def __init__(self, data_config):
        self.selected_SSID = ""
        self.selected_time = ""
        self.selected_webhook = ""
        self.OS = self.os_detector()
        self.get_data_config(data_config)
        self.network_list = []
        self.SSID_list = []
        self.title = "ALARMA WIFI"
        self.content = """
            Ojito, el simulador está  <i>encendido</i>.<br>
            😍
            """

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

    def get_data_config(self, data_config):
        """Genera atributos de clase con los datos pasados a la clase de la última configuración disponible."""
        self.selected_SSID = data_config[0]
        self.selected_time = data_config[1]
        self.selected_webhook = data_config[2]
          
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

    def send_teams(self, webhook_url:str, content:str, title:str, color:str="000000") -> int:
        """
        Recibe los parámetros webhook_url, content, title y color, para realizar el envío de mensaje a través de Teams.        
        """
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

    def check_network(self):
        """
        Tras detectar las redes existentes, comprueba que nuestras redes objetivo
        estén en la lista de redes detectadas. De ser correcto, envía mensaje
        por teams. 
        """
        ssid_list = self.tolist_network()
        for target_ssid in self.selected_SSID:
            if target_ssid in ssid_list:
                print("La red {} se encuentra conectada!".format(target_ssid))
                self.send_teams(self.selected_webhook, self.content, self.title)
            else:
                print("No se han encontrado las redes {ssid}".format(
                                                    ssid=target_ssid),
                                                )

    def run_scheduler(self):
        """
        Método que ejecuta la tarea en el tiempo indicado.
        """
        selected_hour = int(self.selected_time[:3])
        selected_min = int(self.selected_time[-2:])
        scheduler = BlockingScheduler()
        scheduler.add_job(self.check_network, "cron", 
                        hour=selected_hour, 
                        minute=selected_min,
                        second=00,      # Para hacer pruebas. Eliminar.
                        )
        print("Scheduler running. Next check: {hora}.".format(
                                                    hora=self.selected_time),
                                                    )
        scheduler.start()