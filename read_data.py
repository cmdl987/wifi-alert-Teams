'''
Este módulo se encarga de leer los datos almacenados en la última configuración,
dentro del archivo config.csv
'''
from datetime import datetime


class ReadData:
    def __init__(self, path="config.csv"):
        self.path = path
        self.data_config = None 
        self.set_data()

    def get_data_config(self):
        return self.data_config

    def add_new_data(self):
        """
        Genera una nueva línea de datos, abriendo el archivo, preguntando al
        usuario, y guardando los datos en nuestro archivo .csv.
        """
        timestamp = str(datetime.now().strftime("%Y-%m-%d %H:%M"))
        
        # Assigns a user input to user_ssid
        user_ssid = input("Introduzca SSID a buscar. Si es más de una "
                            "sepárela con ','.\n").strip().replace(" ", "")
        
        while True:
            # Assigns a user input to user_time and checks if the input is an integer.
            user_time = str(input("Introduzca la hora en formato HH:MM en que "
                            "quiere que se detecte la red.\n"))
            try: 
                user_hour = int(user_time[:2])
                user_min = int(user_time[-2:])
                if user_hour > 23 or user_min > 59:
                    raise ValueError("ERROR. This is not a valid time format.")
                else: 
                    break
                    
            except ValueError:
                print("ERROR. This is not a valid time format.")

        # Assigns a input to user_webhook.
        user_webhook = str(input("Introduzca el webhook copiado de su grupo "
                            "de Teams.\n"))

        # Combine all user inputs in order to write the data into the file.
        user_data = (timestamp, user_ssid, user_time, user_webhook)
        user_data = ";".join(user_data)
        
        # Write down all the user_data into config.csv file.
        with open(self.path, "a") as file:
            file.write(user_data+"\n")
        
        self.set_data()

    
    def generate_csv(self):
        """
        Genera un nuevo archivo .csv en el path dado con ese header.
        """
        #print("Generado nuevo archivo.")
        with open(self.path, "w") as file:
            header = "ts; SSID_list; alarm_time; web_hook\n"
            file.write(header)


    def set_data(self):
        """
        Abrimos el archivo config.csv para configurar los parámetros.
        """
        try:
            with open(self.path, "r") as file:
                # Lee el archivo
                lines = file.readlines() 

            # Checks the lenght of config.csv. In case it is minor than 2, 
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
                    
                    # Print on screen the lastest used parameters.
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
                        user_selection = input("¿Desea utilizar la "
                                                "configuración actual? Y/N. ")
                        if user_selection in ["Y", "y"]:
                            self.data_config = data_config

                        elif user_selection in ["N", "n"]:
                            print("Seleccione nueva configuración.")
                            self.add_new_data()
                    
                break

        except FileNotFoundError:
            print("Archivo no encontrado.")
            self.generate_csv()
            self.set_data()        
        
        #return data_config