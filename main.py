import os, platform, subprocess
import configparser

class Main:
    def __init__(self):
        self.load_config()

    def load_config(self):
        self.config = configparser.ConfigParser()
        config_file_path = os.path.join(os.path.dirname(__file__), 'config.ini')
        
        self.config.read(config_file_path)
        self.mobsf_path = os.path.join(os.path.dirname(__file__), self.config['MobSF']['MobSF'])
        self.server_ip = self.config['SERVER'].get('ServerIP')
        self.api_key = self.config['API'].get('ApiKey')
        self.file_path = self.config['FILE'].get('FilePath').split(',')
        # self.avm_name = self.config['AVM'].get('AVM_Name')
        # self.frida_script_path = self.config['Frida'].get('Frida_Script')
        self.encryption_method = self.config['Encryption_method'].get('encryption_method')   

    # def save_config(self):
    #     with open('config.ini', 'w') as configfile:
    #         self.config.write(configfile)

    def run_mobsf(self):
        os_platform = platform.system()
        print(os_platform)
        run_script_path = os.path.join(self.mobsf_path, 'setup.sh') # bat / sh
        if not os.path.exists(run_script_path):
            print(f"Error: Invalid Path - {self.mobsf_path}")
            print("Please run MobSF Manually")
            return  
        process = subprocess.Popen(run_script_path, shell=True, cwd=self.mobsf_path)        
       
        print("MobSF is starting! you can now enter next commands:")

        return process 


if __name__ == "__main__":
    main = Main()
    main.run_mobsf()