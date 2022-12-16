from apscheduler.schedulers.blocking import BlockingScheduler

from wifiDetect import WifiDetector
from read_data import ReadData


if __name__ == "__main__":
    # Lee config.csv y obtiene la última configuración guardada.
    last_data_config = ReadData().data_config
    print(last_data_config)
    launcher = WifiDetector(last_data_config)
    #launcher.run_scheduler()
