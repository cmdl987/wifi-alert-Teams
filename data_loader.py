#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
read_data.py
This source code is part of Wifi-Alert program.
It contains the code for accessing the config and log data files, creating them 
in case they do not exist.

__author__: Cristobal Moreno (@cmdl987)
__modified__: 19/12/2022
"""

from datetime import datetime
from pathlib import Path


class DataLoader:
    """
    Class for checking, creating and reading config data from different files.
    """

    def __init__(self, config_path="config.csv", log_path="logs.csv"):
        self.config_path = config_path
        self.log_path = self._log_file_checker(log_path)
        self.data_config = None
        self.set_data()

    @staticmethod
    def _set_alarm_time():
        """
        Assigns a user input to user_time and checks if the input 
        is an integer.

        Returns:
            str : string with the user time separated by ':'

        """
        while True:
            user_time = str(input("Enter a time when you want to detect the"
                                  "networks using the format HH:MM.\n"))
            try:
                user_hour = int(user_time[:2])
                user_min = int(user_time[-2:])
                if user_hour > 23 or user_min > 59:
                    raise ValueError("ERROR. This is not a valid time format.")
                elif ":" not in user_time:
                    raise ValueError("ERROR. This is not a valid time format.")
                else:
                    break

            except ValueError:
                print("ERROR. This is not a valid time format.")

        return user_time

    @staticmethod
    def _set_SSID():
        """Assigns a str input to user_ssid.

        Returns:
            string : Name of the SSID the user wants to detect.
        """

        user_ssid = input("Enter the SSID you want to check. If there is more"
                          "than one, please separate them with ','.\n") \
            .strip().replace(" ", "")

        return user_ssid

    @staticmethod
    def _set_webhook_link():
        """Assigns a input to user_webhook and checks if the link is correct.

        Returns:
            str : string with the webhook copied by the user.
        """
        while True:
            user_webhook = str(input("Enter the copied webhook from your Teams group:\n"))
            if user_webhook.startswith("https://"):
                break
            else:
                print("Webhook format is not valid. Please, enter it again.")

        return user_webhook

    def get_data_config(self):
        """Method that returns the data config loaded previously.

        Returns:
            dict: dictionary with following keys: last_ts, last_SSID, 
            last_time_config, last_webhook.
        """
        return self.data_config

    def add_new_data(self):
        """
        Makes a timestamp, create a new line of data after asking the user 
        to input the new configuration and save them all into a config file 
        which path is chosen from the class attribute self.config_path.
        """
        timestamp = str(datetime.now().strftime("%Y-%m-%d %H:%M"))

        # Assigns a str input to user_ssid.
        user_ssid = self._set_SSID()

        # Assigns an alarm time to user_time.
        user_time = self._set_alarm_time()

        # Assigns a input to user_webhook.
        user_webhook = self._set_webhook_link()

        # Combine all user inputs in order to write the data into the file.
        user_data = (timestamp, user_ssid, user_time, user_webhook)
        user_data = ";".join(user_data)

        # Write down all the user_data into config.csv file.
        with open(self.config_path, "a") as file:
            file.write(user_data + "\n")

        # Call the function again.
        self.set_data()

    @staticmethod
    def _log_file_checker(log_path):
        """
        Checks if a logfile exists. In case not, create a new file with the
        following header string: 'Config_time;Date;Time_alarm;SSIDs_target;SSIDs_detected;webhook;msg_delivered'.
        In case it does exist, return the log path.

        Args:
            log_path (str): default path is '/logs.csv'.

        Returns:
            str: returns the path provided.
        """
        path = Path(log_path)
        if not path.is_file():
            with open(log_path, "w") as log_file:
                header = "config_time;date;time_alarm;SSIDs_target;SSIDs_detected;" \
                         "webhook;delivery_status\n"
                log_file.writelines(header)
            print(f"A new log file has been created as {log_path}.")

        return log_path

    def _generate_config_file(self):
        """
        Create a new config file using the file path of the class object 
        config_path, that contains the following header: 'ts; SSID_list; 
        alarm_time; webhook'.
        """
        with open(self.config_path, "w") as file:
            header = "ts; SSID_list; alarm_time; webhook\n"
            file.write(header)

        print(f"A new config file has been created as {self.log_path}.")

    def set_data(self):
        """
        Checks if a config file exists. In case not, raise and error that 
        triggers a method to create it. 
        In case it does exist, read the last line and ask the user to continue 
        with the selected configuration.
        """
        try:
            with open(self.config_path, "r") as file:
                # Read the file
                lines = file.readlines()

            # Checks the length of config.csv. In case it is minor than 2,
            # launch add_new_data method.              
            while True:
                if len(lines) == 1:
                    print("There is no previous configuration available.")
                    self.add_new_data()
                    break

                else:
                    # Select config.csv last line with last parameters.
                    last_line = lines[-1].split(";")

                    # Generate a dict with the values from the config.csv.
                    data_config = {"last_ts": last_line[0],
                                   "last_SSID": last_line[1].replace(" ", "").split(","),
                                   "last_time_config": last_line[2],
                                   "last_webhook": last_line[3],
                                   }

                    # Print statement of the previous used parameters.
                    print("-" * 70, "\nLAST USED CONFIGURATION\n", "-" * 70)
                    print("\tLast config from: {}".format(
                        data_config["last_ts"]))
                    print("\tLast networks:\t  {}".format(
                        data_config["last_SSID"]))
                    print("\tLast alarm time:  {}".format(
                        data_config["last_time_config"]))
                    shorted_webhook = data_config["last_webhook"][-10:]
                    print("\tLast webhook:\t ...{}".format(
                        shorted_webhook))
                    print("-" * 70)

                    # Ask the user to continue with this configuration.
                    # In case of Y, returns the configuration.
                    # In case of N, launch the method to ask user for new data.
                    user_selection = ""
                    while user_selection not in ["Y", "y", "N", "n"]:
                        user_selection = input("Would yo like to use the last configuration? Y/N. ")
                        if user_selection in ["Y", "y"]:
                            self.data_config = data_config

                        elif user_selection in ["N", "n"]:
                            print("Please, insert a new configuration.")
                            self.add_new_data()

                break

        except FileNotFoundError:
            self._generate_config_file()
            self.set_data()
