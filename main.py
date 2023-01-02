"""
DESDE .SEND_TEAMS() ENVÍA EL POST CON EL WEBHOOK Y EL CONTENT MANUAL, PERO NO
LO HACE DESDE LA PROPIA CLASE. 
TENGO QUE REVISAR.
"""

from wifiDetect import WifiDetector
from data_loader import DataLoader 

if __name__ == "__main__":
    # Lee config.csv y obtiene la última configuración guardada.
    new_data = DataLoader()
    last_data_config = new_data.get_data_config()
    launcher = WifiDetector(last_data_config)
    launcher.run_scheduler()

# https://myuax.webhook.office.com/webhookb2/2ef9a78a-7c32-49da-be6d-5fc4968811cd@8344d72d-e21b-485a-b9a1-52078e79010e/IncomingWebhook/43d6a479f4cb4db0842af2fd763b690b/14d96f44-0bf8-4c09-859d-68edc4681dd5