from datetime import datetime

time_now = datetime.now()
time_now = time_now.strftime("%Y-%m-%d %H:%M")
print(time_now)

with open("config.csv") as file:
    lines = file.readlines() 
    if (len(lines)) == 1:
        print("Esto está vacío")
        #Función para dar valores a config.
    else:
        last_line = lines[-1].split(";")
        last_ts = last_line[0]
        last_ssids = last_line[1].split()
        last_time_config = last_line[2]
        last_webhook = last_line[3]
        print(f"Última vez configurado: {last_ts}")
        print(f"Última red configurada: {last_ssids}")
        print(f"Última hora configurada: {last_time_config}")
        print(f"Último webhook configurado: {last_webhook}")
        
