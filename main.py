import os, platform
import subprocess
import configparser
import requests

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
        self.file_path = self.config['FILE'].get('FilePath')
        # self.avm_name = self.config['AVM'].get('AVM_Name')
        # self.frida_script_path = self.config['Frida'].get('Frida_Script')
        self.encryption_method = self.config['Encryption_method'].get('encryption_method')   

    def start_mobsf(self):
        os_name = platform.system()
        if os_name == "Windows":
            setup_script_path = os.path.join(self.mobsf_path, 'setup.bat')
            run_script_path = os.path.join(self.mobsf_path, 'run.bat')
        elif os_name == "Linux" or os_name == "Darwin":
            setup_script_path = os.path.join(self.mobsf_path, 'setup.sh')
            run_script_path = os.path.join(self.mobsf_path, 'run.sh')
        else:
            print("Unknown operating system.")
            return
        if not os.path.exists(setup_script_path) or not os.path.exists(run_script_path):
            print(f"Error: Invalid Path: {self.mobsf_path}")
            return
        
        print("Starting MobSF...")
        setup_process = subprocess.Popen(setup_script_path, shell=True, cwd=self.mobsf_path)
        setup_process.communicate()        
        process = subprocess.Popen(run_script_path, shell=True, cwd=self.mobsf_path)
        print("MobSF is runnining!")
        return process

    # def get_status(self): #Print the contents of the config.ini
    #     print("=========================HERE=========================")      
    #     if hasattr(self, 'server_ip'):
    #         print("\nMobSF server IP: {}".format(self.server_ip))
    #     else:
    #         print("\nMobSF server IP is not set.")

    #     if hasattr(self, 'api_key'):
    #         print("MobSF API KEY: {}".format(self.api_key))
    #     else:
    #         print("MobSF API KEY is not set.")

    #     if hasattr(self, 'file_path'):
    #         if self.file_path:
    #             print("Target file path ({}): {}".format(len(self.file_path), ', '.join(self.file_path)))
    #         else:
    #             print("Target file path is not set.\n")
    #     else:
    #         print("Target file path is not set.\n")
        
    #     if hasattr(self, 'mobsf_path'):
    #         print("MobSF Path: {}\n".format(self.mobsf_path))
    #     else:
    #         print("MobSF Path: MobSF Path is not set.")

    #     print("=========================HERE=========================")

    def server_is_running(self):
        try:
            response = requests.get(self.server_ip)
            if response.status_code == 200:
                return True
            else:
                print(f"Warning: The server responded with an unexpected status code: {response.status_code}. Please check the server.")
                return False
        except requests.ConnectionError:
            print("Failed to connect to the server.")
            return False

    def nested_check(self):
        print("Checking nested apk...")

        current_dir_path = os.getcwd()

        zip_file_path = self.file_path.split('/')[-1] + ".zip"
        shutil.copy(selected_file_path, zip_file_path)

        zip_dir_path = current_dir_path + "\\nested_apk\\analysis"
        if not os.path.exists(zip_dir_path):
            os.makedirs(zip_dir_path, exist_ok=True)
        else:
            print("Directory already exists")
    
        with zipfile.ZipFile(zip_file_path, 'r') as unzip:
            unzip.extractall(zip_dir_path)
    
        apk_files = []
        if os.path.exists(zip_dir_path):
            for root, dirs, files in os.walk(zip_dir_path):
                for file in files:
                    if file.endswith('.apk'):
                        file_path = os.path.join(root, file)
                        apk_files.append(file_path)
        else:
            print("Directory does not exist")
        
        if apk_files:
            print(len(apk_files), "nested apks were found.")
            print("---------------------------------------------------------------")
            return apk_files
        else:
            print("nested apk was not found.")

if __name__ == "__main__":
    main = Main()
    main.start_mobsf()