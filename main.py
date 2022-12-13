import platform

from apscheduler.schedulers.blocking import BlockingScheduler

from wifiDetect import WifiDetector
from read_data import ReadData

# string con el path a nuestro .txt con las redes que queremos que busque.
file_path = "/home/koper/Documentos/GitHub/wifi-alarm/redes.txt"

def load_last_config(file_path):
    last_config = ReadData(file_path)
    data_config = last_config.get_data()
    return data_config



if __name__ == "__main__":
    last_data_config = load_last_config(file_path)
    launcher = WifiDetector(last_data_config)     



    
