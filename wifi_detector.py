#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 
wifi_detector.py
This source code is part of Wifi-Alert program.
It is involved in checking for wifi networks from our wireless adapter. It also verifies if the targeted networks we are keen to detect are active or not, and 
send an alert message to a Microsoft Teams group using a webhook.

__author__: Cristobal Moreno (@cmdl987)
__modified__: 19/12/2022
"""

from datetime import datetime
import subprocess
import platform
import json
import warnings
from time import sleep

from apscheduler.schedulers.blocking import BlockingScheduler
import requests

warnings.filterwarnings("ignore")


class TeamsWebhookException(Exception):
    """
    Own exception that raise when there was an error sending the message via 
    Teams. It happens when the response after calling to the webhook is not 200.
    """
    pass


class WifiDetector:
    """ 
    Class that detects wifi networks, crosscheck with our configuration data and
    send a personalized message to a specific Microsoft Teams group.
    """

    def __init__(self, data_config):
        self.last_config_ts = data_config["last_ts"]
        self.selected_SSID = data_config["last_SSID"]
        self.selected_time = data_config["last_time_config"]
        self.selected_webhook = str(data_config["last_webhook"]).strip()
        self.log_path = "logs.csv"
        self.json_content = "content.json"
        self.personalized_json_content = "personalized_content.json"
        self.msg_delivered = None
        self.timestamp = str(datetime.now().strftime("%Y-%m-%d"))

    def set_content(self, target_ssid):
        """Read the content.json where all the information is allocated to 
        correctly send the message to Teams.

        Args:
            target_ssid (str): SSID name target that is detected

        Returns:
            str: personalized content to send as a message via Teams.
        """
        # Loads the .json file with the message content
        with open(self.json_content, "r") as file:
            content = json.load(file)

        try:
            # Loads the .json file with personalized data content for message.
            with open(self.personalized_json_content, "r") as file:
                p_content = json.load(file)

            if target_ssid in p_content.keys():
                content["sections"][0]["activityTitle"] = p_content[target_ssid]["title"]
                content["sections"][0]["activityImage"] = p_content[target_ssid]["image"]
                content["sections"][0]["activitySubtitle"] = p_content[target_ssid]["location"]

        except FileNotFoundError:
            print("Network info for this SSID was not found into personalized_content.json file.")
            print("-" * 70)

        content["sections"][0]["facts"][0]["value"] = target_ssid
        return content

    @staticmethod
    def detect_networks():
        """Run a subprocess according to the OS where the program is launched from.
        It gets all the networks detected from the network adapter.

        Returns:
            str: String containing all the networks descriptions.
        """
        user_OS = platform.system()
        if user_OS == "Linux":
            networks_info = subprocess.check_output(["nmcli", "dev", "wifi"])
            networks_info = networks_info.decode("utf-8", errors="ignore")
        else:
            networks_info = subprocess.check_output(['netsh', 'wlan', 'show', "networks"])
            networks_info = networks_info.decode("utf-8", errors="ignore")

        return networks_info

    def tolist_network(self):
        """Call to the detect_networks() method to obtain all the networks info,
        to generate a list with all the SSID names.
        
        Returns:
            list: List with all the wi-fi networks detected.
        """
        networks = self.detect_networks().splitlines()
        network_list = []

        # Iterate for each detected line to add SSIDs to the detected list.
        for ssid_line in networks:
            if "BSSID" not in ssid_line and "--" not in ssid_line:
                ssid = ssid_line.replace("*", "").split()
                network_list.append(ssid[1])

        # Delete any SSID could be duplicated because of multiple AP used.
        network_list = list(set(network_list))
        return network_list

    def __str__(self):
        """
        Print on screen the configuration is going to be used.
        """
        print("-" * 70)
        print("CONFIGURATION LOADED")
        print("\tSSIDs: {ssid}\tTime alarm: {alarm}\tWebhook: {webh}".format(
            ssid=self.selected_SSID,
            alarm=self.selected_time,
            webh="..." + self.selected_webhook[-10:]
        ))
        print("-" * 70)

    def get_networks_info(self):
        """
        Print on screen the networks detected.
        """
        listed_networks = self.tolist_network()
        print("It has been detected {} wi-fi networks:".format(len(listed_networks)))
        for index, ssid in enumerate(listed_networks):
            print("\t", index, "\t", ssid)

    def send_teams(self, webhook, content):
        """
        Sends and message to the Teams group linked with the webhook.
        self.selected_webhook y self.content.         

        Args:
            webhook (str): link with the Webhook
            content (str): personalized content for each target SSID 

        Raises:
            TeamsWebhookException: If status_code is not 200.

        """
        response = requests.post(
            url=webhook,
            headers={"Content-Type": "application/vnd.microsoft.card.hero"},
            json=content,
        )
        if response.status_code == 200:
            self.msg_delivered = True

        else:
            self.msg_delivered = False
            raise TeamsWebhookException(response.reason)

    def _logger(self, detected_ssids):
        """
        Open the log file in order to write the results after running the task. 
        """
        with open(self.log_path, "a") as path_file:
            data_log = (self.last_config_ts, self.timestamp, self.selected_time,
                        str(self.selected_SSID), str(detected_ssids),
                        self.selected_webhook, str(self.msg_delivered),
                        )
            log_line = ";".join(data_log)
            path_file.write(log_line + "\n")

    def _check_networks(self):
        """
        Checks if the networks that has been selected are detected. When the 
        target network is detected, it execute the method in order to send a
        message via Teams.
        """
        ssid_list = self.tolist_network()
        detected_ssids = []

        # Iterate for each SSID target.
        for target_ssid in self.selected_SSID:

            # Add to the list if the SSID is detected
            if target_ssid in ssid_list:
                print(f"Network {target_ssid} has been detected!")
                detected_ssids.append(target_ssid)

                # Send a message to the Teams group after checking SSID is ON.
                try:
                    self.send_teams(self.selected_webhook, self.set_content(target_ssid))

                except TeamsWebhookException:
                    print("It could not be possible to reach the Teams group.",
                          "Please, check the webhook selected is correct.")
                sleep(0.5)
            else:
                print(f"Network {target_ssid} has not been detected.")

        # Save the logs with the detected SSIDs from the previous list.
        self._logger(detected_ssids)

    def run_scheduler(self):
        """
        Run the scheduler every day at the selected time, in order to launch the method to check if the selected SSIDs are turned on.
        """
        selected_hour = int(self.selected_time[:2])
        selected_min = int(self.selected_time[-2:])
        scheduler = BlockingScheduler()
        scheduler.add_job(self._check_networks, "cron",
                          day="*",
                          hour=selected_hour,
                          minute=selected_min,
                          )
        print(f"Scheduler running. Next check at {self.selected_time}.")
        print("-" * 70)
        scheduler.start()
