import subprocess   

class network:
    def __init__(self, sistema):
        self.set_networks(sistema)


    def set_networks(self, sistema):
        if sistema == "Linux":
            networks = subprocess.check_output(["nmcli", "dev", "wifi"])
            self.networks = networks.decode("utf-8", errors="ignore")            
        else:
            networks = subprocess.check_output(['netsh', 'wlan', 'show', "networks"])
            self.networks = networks.decode("utf-8", errors="ignore")

    def show_networks(self):
        print(self.networks)


objetivo = network("Linux")
objetivo.show_networks()
