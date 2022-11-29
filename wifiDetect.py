import subprocess
from pprint import pprint

class WifiDetector:
    def __init__(self, my_os, path=""):
        self.network_file = ""
        self.network_list = []
        self.path = path
        self.SSID_list = []
        self.OS = my_os 
        #self.create_networks_file()


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


    def list_generator(self):
        """
        Llama a la función detect_networks() para obtener toda la información 
        de redes, de la cual obtener el nombre de los SSID y guardarlos
        en la lista network_list.
        """
        networks = self.detect_networks().splitlines()
        # Itera por cada línea de la variable networks para guardar el SSID.
        for ssid_line in networks:
            if "BSSID" not in ssid_line:
                ssid = ssid_line.replace("*", "").split()
                self.network_list.append(ssid[1])
        self.network_list = list(set(self.network_list))

        return self.network_list


    # def create_networks_file(self):             # obtener un return path?
    #     """
    #     Limpia el archivo self.networks de caracteres especiales (*, "IN-USE"). 
    #     Genera un archivo .csv con la información obtenida en self.networks.       
    #     """
    #     self.networks_file = open("wifi_networks.csv", "w")
    #     for car in ["*", "IN-USE"]:
    #         networks_clean = self.networks.replace(car, "")
    #     self.networks_file.write(networks_clean)
    #     self.networks_file.close()


    def get_networks_info(self):
        print("Se han detectado {} redes wi-fi:".format(len(self.network_list)))
        for index, ssid in enumerate(self.network_list):
            print("\t", index, "\t", ssid)

 
    def get_network_list(self):
        """
        Abre el archivo con nuestras redes anotadas para devolver una lista de las redes.
        Si el archivo está vacío, nos avisa de que no hay ninguna red anotada.
        """
        network_target = open(self.path, "r", encoding="utf-8")
        network_list = network_target.read().split()
        if len(network_list) < 1:
            print("Atención, no hay ninguna red Wifi anotada en el archivo redes.txt.")
            return None
        else:
            return network_list


    def check_network(self, target_network):
        if target_network in self.network_list:
            print("La red {} se encuentra conectada!".format(target_network))


#####
#TEST
#####
file_path = "/home/cmdl987/GitHub/wifi-alarm/redes.txt"
launcher = WifiDetector("Linux", file_path)    
wifi_networks = launcher.list_generator()
launcher.get_networks_info()
launcher.check_network("Croqueta&Empanadilla")
