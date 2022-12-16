'''
Este módulo se encarga de leer los datos almacenados en la última configuración,
dentro del archivo config.csv
'''
from datetime import datetime

class ReadData:
    def __init__(self, path="config.csv"):
        self.path = path
        self.data_config = self.get_data()

    def add_new_data(self):
        """
        Genera una nueva línea de datos, abriendo el archivo, preguntando al
        usuario, y guardando los datos en nuestro archivo .csv.
        """
        with open(self.path, "a") as file:
            file.write("\n")
            timestamp = str(datetime.now().strftime("%Y-%m-%d %H:%M"))
            user_ssid = input("Introduzca SSID a buscar. Si es más de una sepárela con ','.\n").strip().replace(" ", "")
            user_time = str(input("Introduzca la hora en formato HH:MM en que quiere que se detecte la red.\n"))
            user_webhook = str(input("Introduzca el webhook copiado de su grupo de Teams.\n"))
            user_data = (timestamp, user_ssid, user_time, user_webhook)
            user_data = ";".join(user_data)
            file.writelines([user_data])

    
    def generate_csv(self):
        """
        Genera un nuevo archivo .csv en el path dado con ese header.
        """
        #print("Generado nuevo archivo.")
        with open(self.path, "w") as file:
            header = "ts; SSID_list; alarm_time; web_hook\n"
            file.writelines([header])
        self.add_new_data()


    def get_data(self):
        """Abrimos el archivo config.csv para obtener los parámetros."""
        try:
            with open(self.path) as file:
                # Lee el archivo
                lines = file.readlines() 
                
                # Selecciona la última línea que es la última configuración.
                last_line = lines[-1].split(";")
                
                # Genera diccionario con los valores del .csv.
                data_config = {"last_ts": last_line[0],
                                "last_SSID": last_line[1].split(),
                                "last_time_config": last_line[2],
                                "last_webhook": last_line[3],
                                }
                
                # Muestra en pantalla la última configuración cargada.
                print("-"*70)
                print("Última vez configurado: {}".format(
                                            data_config["last_ts"]))
                print("Última red configurada: {}".format(
                                            data_config["last_SSID"]))
                print("Última hora configurada: {}".format(
                                            data_config["last_time_config"]))
                shorted_webhook = data_config["last_webhook"][-10:]
                print("Último webhook configurado: ...{}".format(
                                                shorted_webhook))
                print("-"*70)
                
                # Pregunta al usuario si quiere seguir con esa configuración.
                # Si responde Y, devuelve configuración.
                # Si responde N, preguntando a usuario por nuevos datos.
                user_selection = ""
                while user_selection not in ["Y", "y", "N", "n"]:
                    user_selection = input("¿Desea utilizar la configuración actual? Y/N. ")
                    if user_selection in ["Y", "y"]:
                        return data_config

                    elif user_selection in ["N", "n"]:
                        print("Seleccione nueva configuración.")
                        self.add_new_data()
                        self.get_data()

                            
        except FileNotFoundError:
            print("Archivo no encontrado.")
            self.generate_csv()


# string con el path a nuestro .txt con las redes que queremos que busque.
#file_path = "/home/cmdl987/GitHub/wifi-alarm/config2.csv"
#last_data_config = ReadData()