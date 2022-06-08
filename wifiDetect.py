import subprocess
import pandas as pd

class network:
    def __init__(self, sistema):
        self.network_file = ""
        self.SSID_list = []
        self.OS = sistema 
        self.get_system_networks()


    def get_system_networks(self):
        """
        Obtiene información de las redes detectadas por el equipo.
        """
        if self.OS == "Linux":
            networks = subprocess.check_output(["nmcli", "dev", "wifi"])
            self.networks = networks.decode("utf-8", errors="ignore")            
        else:
            networks = subprocess.check_output(['netsh', 'wlan', 'show', "networks"])
            self.networks = networks.decode("utf-8", errors="ignore")
        return self.networks

    def create_networks_file(self):             # obtener un return path?
        """
        Limpia el archivo self.networks de caracteres especiales (*, "IN-USE"). 
        Genera un archivo .csv con la información obtenida en self.networks.       
        """
        self.networks_file = open("wifi_networks.csv", "w")
        car_a_reemp = ["*", "IN-USE"]
        for car in car_a_reemp:
            networks_clean = self.networks.replace(car, "")
        self.networks_file.write(networks_clean)
        self.networks_file.close()

    def get_networks_file(self):
        return network_file   # opción para descargar archivo. 


    def show_networks_file(self):               # que path mandarle a leer¿?
        """
        Leer el archivo generado con pandas para obtener listado.
        Genera a su vez una lista con las SSID para utilizar de búsqueda."""
        self.networks_pd_file = pd.read("/home/koper/Documentos/GitHub/wifi-alarm/wifi_networks.csv",
                                        sep="\\s+", index_col=False)
        print(self.networks_pd_file)
        self.SSID_list = [SSID for SSID in self.networks_pd_file["SSID"]]
    
    def select_list(self, SSID):
        """
        Selecciona por el índice, la SSID que queremos añadir a nuestra
        lista para que nos salte la alarma.
        """




#####
objetivo = network("Linux")
datos_wifi = objetivo.get_system_networks()   # devuelve un str.
#print(datos_wifi)

archivo_wifi = open("redes_wifi.csv", "w")
car_a_reemp = ["*", "IN-USE"]
for car in car_a_reemp:
    datos_wifi = datos_wifi.replace(car, " ")
archivo_wifi.write(datos_wifi)
archivo_wifi.close()

archivo_wifi = pd.read_csv("/home/koper/Documentos/GitHub/wifi-alarm/redes_wifi.csv", 
                           sep="\s+", index_col=False)

print(archivo_wifi["SSID"][0])
lista_SSID = [i for i in archivo_wifi["SSID"]]
print(lista_SSID)
if "THOM_ONO4601" in lista_SSID:
    print("True")
else: 
    print("False")




