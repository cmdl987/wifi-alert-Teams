""" 
main.py
This is the main part where is intented to run the Wifi-Alert program.
__author__: Cristobal Moreno (@cmdl987)
__modified__: 19/12/2022
"""

from wifi_detector import WifiDetector
from data_loader import DataLoader 

if __name__ == "__main__":
    # Lee config.csv y obtiene la última configuración guardada.
    new_data = DataLoader()
    last_data_config = new_data.get_data_config()
    launcher = WifiDetector(last_data_config)
    launcher.run_scheduler()

# https://myuax.webhook.office.com/webhookb2/2ef9a78a-7c32-49da-be6d-5fc4968811cd@8344d72d-e21b-485a-b9a1-52078e79010e/IncomingWebhook/43d6a479f4cb4db0842af2fd763b690b/14d96f44-0bf8-4c09-859d-68edc4681dd5