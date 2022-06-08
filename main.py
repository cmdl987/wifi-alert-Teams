import subprocess 
import platform

from wifiDetect import network

#detectamos el SO desde el que corremos el .py
launcher = network(platform.system())         

