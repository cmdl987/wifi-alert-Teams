import subprocess 
import platform

from wifiDetect import network

sistema = platform.system()         #detectamos el SO desde el que corremos el .py
launcher = network(sistema)         

