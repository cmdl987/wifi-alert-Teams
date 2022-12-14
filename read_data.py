'''
Este módulo se encarga de leer los datos almacenados en la última configuración,
dentro del archivo config.csv
'''

class ReadData:
    def __init__(self, path):
        self.path = path

    def get_data(self):
        """Abrimos el archivo config.csv para obtener los parámetros."""
        with open(self.path) as file:
            lines = file.readlines() 
            if (len(lines)) == 1:
                print("Esto está vacío")

            else:
                last_line = lines[-1].split(";")
                last_ts = last_line[0]
                last_ssids = last_line[1].split()
                last_time_config = last_line[2]
                last_webhook = last_line[3]
                print("-"*70)
                print(f"Última vez configurado:   {last_ts}")
                print(f"Última red configurada:   {last_ssids}")
                print(f"Última hora configurada: {last_time_config}")
                print(f"Último webhook configurado: ...{last_webhook[-10:]}")
                print("-"*70)
        
        return last_ssids, last_time_config, last_webhook
