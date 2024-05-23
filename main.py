import os
import configparser

class Main:
    def __init__(self):
        self.load_config()

    def load_config(self):
        self.config = configparser.ConfigParser()
        config_file_path = os.path.join(os.path.dirname(__file__), 'config.ini')
        
        self.config.read(config_file_path)
        self.mobsf_path = os.path.join(os.path.dirname(__file__), self.config['MobSF']['MobSF'])
        self.server_ip = self.config['SERVER'].get('ServerIP', self.config['DEFAULT']['ServerIP'])
        self.api_key = self.config['API'].get('ApiKey', self.config['DEFAULT']['ApiKey'])
        self.file_path = self.config['FILE'].get('FilePath', self.config['DEFAULT']['FilePath']).split(',')
        self.avm_name = self.config['AVM'].get('AVM_Name', self.config['DEFAULT']['AVM_Name'])
        self.frida_script_path = self.config['Frida'].get('Frida_Script', self.config['DEFAULT']['Frida_Script'])
        self.encryption_method = self.config['Encryption_method'].get('encryption_method', self.config['DEFAULT']['Encryption_method'])   

    def save_config(self):
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)


if __name__ == "__main__":
    main = Main()
    main.start()