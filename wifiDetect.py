import subprocess
import pandas as pd

class WifiDetector:
    def __init__(self, my_os, path=""):
        self.network_file = ""
        self.path = path
        self.SSID_list = []
        self.OS = my_os 
        #self.networks = self.detect_networks()
        #self.create_networks_file()
        #self.network_list = self.get_network_list()


    def detect_networks(self):
        """
        Obtiene información de las redes detectadas por el equipo.
        """
        if self.OS == "Linux":
            networks = subprocess.check_output(["nmcli", "dev", "wifi"])
            networks = networks.decode("utf-8", errors="ignore")            
        else:
            networks = subprocess.check_output(['netsh', 'wlan', 'show', "networks"])
            networks = networks.decode("utf-8", errors="ignore")
        return networks


    def create_networks_file(self):             # obtener un return path?
        """
        Limpia el archivo self.networks de caracteres especiales (*, "IN-USE"). 
        Genera un archivo .csv con la información obtenida en self.networks.       
        """
        self.networks_file = open("wifi_networks.csv", "w")
        for car in ["*", "IN-USE"]:
            networks_clean = self.networks.replace(car, "")
        self.networks_file.write(networks_clean)
        self.networks_file.close()


    def get_networks_file(self):
        return self.network_file   # opción para descargar archivo. 

 
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


    # #ACABAR ESTAS LINEAS DE ABAJO.
    # def check_network(self):
    #     for red in lista_redes:
    #         if red in launcher:
    #         print("La red {} se encuentra conectada!".format(red))





#####
file_path = "/home/cmdl987/GitHub/wifi-alarm/redes.txt"
launcher = WifiDetector("Linux", file_path)    
wifi_network = launcher.detect_networks()   # devuelve un str.
lines = wifi_network.splitlines()
for line in lines:
    linea = line.split()
    print(linea[1])

#print(wifi_network)
#print(datos_wifi)

# """
# archivo_wifi = open("redes_wifi.csv", "w")
# for car in ["*", "IN-USE"]:
#     datos_wifi = datos_wifi.replace(car, " ")
# archivo_wifi.write(datos_wifi)
# archivo_wifi.close()
# """
# df = pd.read_csv("/home/koper/Documentos/GitHub/wifi-alarm/redes_wifi.csv", 
#                            sep="\s+", index_col=False, 
#                            usecols=[1])

# print(df)
# """
# print(df["SSID"][0])
# lista_SSID = [i for i in archivo_wifi["SSID"]]
# print(lista_SSID)
# if "THOM_ONO4601" in lista_SSID:
#     print("True")
# else: 
#     print("False")
# """