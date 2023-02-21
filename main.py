#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 
main.py
This is the main part of the Wifi-Alert program.
It is involved in the development of the running program.

__author__: Cristobal Moreno (@cmdl987)
__modified__: 19/12/2022
"""

from wifi_detector import WifiDetector
from data_loader import DataLoader 

if __name__ == "__main__":

    # Read the data config file and get the latest configuration.
    new_data = DataLoader()
    last_data_config = new_data.get_data_config()

    # Send the config data and start the scheduler
    launcher = WifiDetector(last_data_config)
    launcher.run_scheduler()