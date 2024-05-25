import os, platform
import subprocess
import configparser
import requests
import shutil
from Crypto.Cipher import AES #pip install pycryptodome
from Crypto.Util.Padding import unpad

class Main:
    def __init__(self):
        self.load_config()
        self.output_dir_path = ''

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
        self.encryption_key = self.config['ENCRYPTION'].get('Key')
        self.apktool = self.config['APKTOOL'].get('Apktool')

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
        
    #################################
    ############Decompile############
    #################################

    def create_path(self):
        output_folder_name = 'sample3'
        output_dir_path = os.path.join(os.path.dirname(__file__), output_folder_name)
        os.makedirs(output_dir_path, exist_ok=True)
        return output_dir_path

    def decompile_apk(self, file_path, output_dir_path):
        self.output_dir_path = self.create_path()
        try:
            subprocess.run([self.apktool, 'd', '-r', '-s', '-f', file_path, '-o', output_dir_path], check=True)
            print(f"APK DECOMPILE SUCEESS! ROUTE IS HERE: {self.output_dir_path}")
            print('==============================================================')
            return True
        except subprocess.CalledProcessError as e:
            print("APK DECOMPILE FAILED")
            return False
        
    def find_and_decompile_nested_apks(self, directory=None):
        if directory is None:
            directory = self.output_dir_path  # 시작 디렉토리가 제공되지 않은 경우, 최근에 생성된 출력 디렉토리를 사용
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.apk'):
                    nested_apk_path = os.path.join(root, file)
                    nested_output_dir = os.path.join(root, '' + os.path.splitext(file)[0])
                    os.makedirs(nested_output_dir, exist_ok=True)
                    print(f"Nested APK found: {nested_apk_path}")
                    print('==============================================================')
                    if self.decompile_apk(nested_apk_path, nested_output_dir):  # 중첩된 APK 디컴파일 시도
                        self.decrypt_dex_files(nested_output_dir)
                        self.remove_dex_files(nested_output_dir)
                        self.repackage_apk(nested_output_dir)
                        self.find_and_decompile_nested_apks(nested_output_dir) # 디컴파일이 성공하면, 해당 디렉토리에서 더 찾기
    
    def remove_dex_files(self, directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if 'kill' in file and file.endswith('.dex'):
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    print("==============================================================")
                    print("Complete the file removal")

    #################################
    ###########Decryption############
    #################################

    def decrypt_dex_files(self, directory):
        key_bytes = self.encryption_key.encode()  # 문자열 키를 바이트로 변환
        cipher = AES.new(key_bytes, AES.MODE_ECB)  # ECB 모드로 AES 객체 생성

        for root, dirs, files in os.walk(directory):
            dex_count = 1  # 각 디렉토리별 dex 파일 번호
            for file in files:
                if file.endswith('.dex'):
                    file_path = os.path.join(root, file)
                    # 파일 존재 여부 확인
                    if not os.path.exists(file_path):
                        print(f"File does not exist: {file_path}")
                        continue

                    try:
                        with open(file_path, 'rb') as f:
                            file_data = f.read()
                    except IOError as e:
                        print(f"Error opening file {file_path}: {str(e)}")
                        continue

                    # 'dex' 헤더 검사
                    if not file_data.startswith(b'dex'):
                        try:
                            decrypted_data = cipher.decrypt(file_data)
                            # 패딩이 적용되었을 경우 제거
                            try:
                                decrypted_data = unpad(decrypted_data, AES.block_size)
                            except ValueError:
                                pass  # 패딩이 없으면 넘어감
                            if decrypted_data.startswith(b'dex'):
                                new_file_name = f'dexclasses{dex_count}.dex'
                                new_file_path = os.path.join(root, new_file_name)
                                with open(new_file_path, 'wb') as f:
                                    f.write(decrypted_data)
                                print(f"Decrypted and saved as {new_file_path}")
                                dex_count += 1  # 다음 파일 번호로 업데이트
                            else:
                                print(f"Decryption did not produce a valid dex file: {file_path}")
                        except (ValueError, KeyError) as e:
                            print(f"Decryption failed for {file_path}: {str(e)}")
                    else:
                        print(f"Valid dex file (no decryption needed): {file_path}")


    #################################
    ############Repackage############
    #################################

    def repackage_apk(self, directory):
        apk_name = os.path.basename(directory) + '.apk'
        parent_directory = os.path.dirname(directory)
        output_apk_path = os.path.join(parent_directory, apk_name)
        try:
            subprocess.run([self.apktool, 'b', '-f', directory, '-o', output_apk_path], check=True)
            print(f"APK successfully repackaged: {output_apk_path}")
            # 디렉토리 내의 파일 삭제, 단 생성된 APK 파일은 제외
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                if file_path != output_apk_path:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
            print(f"Cleaned up directory: {directory}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to repackage APK in {directory}: {str(e)}")

    

if __name__ == "__main__":
    main = Main()
    #main.start_mobsf()
    initial_output_dir = main.create_path()
    initial_apk_path = main.file_path
    main.decompile_apk(initial_apk_path, initial_output_dir)
    main.find_and_decompile_nested_apks(initial_output_dir)
    main.decrypt_dex_files(initial_output_dir)
    main.remove_dex_files(initial_output_dir)
    main.repackage_apk(initial_output_dir)
