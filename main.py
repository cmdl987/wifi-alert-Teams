import subprocess 
import platform

from wifiDetect import WifiDetector

# string con el path a nuestro .txt con las redes que queremos que busque.
file_path = "/home/koper/Documentos/GitHub/wifi-alarm/redes.txt"
# detectamos el SO desde el que corremos el .py
my_os = platform.system()
launcher = WifiDetector(my_os, file_path)         




    
