import json

from wifiDetect import WifiDetector
from read_data import ReadData


if __name__ == "__main__":
    # Lee config.csv y obtiene la última configuración guardada.
    last_data_config = ReadData().data_config
    #print(last_data_config)
    launcher = WifiDetector(last_data_config)
    with open("content.json") as file:
        content = json.load(file)
        print(content["sections"][0]["activityTitle"])
        content["sections"][0]["activityTitle"] = "METI"
        print(content["sections"][0]["activityTitle"])



    #mensaje = launcher.content_reader()
    webhook = "https://myuax.webhook.office.com/webhookb2/2ef9a78a-7c32-49da-be6d-5fc4968811cd@8344d72d-e21b-485a-b9a1-52078e79010e/IncomingWebhook/43d6a479f4cb4db0842af2fd763b690b/14d96f44-0bf8-4c09-859d-68edc4681dd5"
    response = launcher.send_teams(webhook, content, "ALARMA WIFI")
    #launcher.run_scheduler()
