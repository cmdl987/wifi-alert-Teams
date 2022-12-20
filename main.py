"""
DESDE .SEND_TEAMS() ENVÍA EL POST CON EL WEBHOOK Y EL CONTENT MANUAL, PERO NO
LO HACE DESDE LA PROPIA CLASE. 
TENGO QUE REVISAR.
"""

from wifiDetect import WifiDetector
from read_data import ReadData


if __name__ == "__main__":
    # Lee config.csv y obtiene la última configuración guardada.
    data_reader = ReadData()
    last_data_config = data_reader.data_config
    launcher = WifiDetector(last_data_config)
    launcher.run_scheduler()
