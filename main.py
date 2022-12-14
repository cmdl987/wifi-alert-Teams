from apscheduler.schedulers.blocking import BlockingScheduler

from wifiDetect import WifiDetector
from read_data import ReadData

# string con el path a nuestro .txt con las redes que queremos que busque.
file_path = "/home/cmdl987/GitHub/wifi-alarm/config.csv"


if __name__ == "__main__":
    last_data_config = ReadData(file_path).get_data()
    launcher = WifiDetector(last_data_config)
    launcher.run_scheduler()
