import json
import requests
import time
import os
import pprint

SERVER = 'http://127.0.0.1:8000'
FILE = '/Users/halinlee/Desktop/sandbox/sample2.apk'
API_KEY = 'b8d75e09550939c951acc7f9545e2260f559eee8c51c9e237c4cce2472d4fb81'
REPORT_PATH = '/Users/halinlee/Desktop/sandbox'
FRIDA_BYPASS_CODE = '''
//fridatest.js
Java.perform(function () {
    var TargetClass = Java.use('com.ldjSxw.heBbQd.a.b');
    TargetClass.k.implementation = function () {
        console.log('inject');
        return false;
    };
});
'''
def create_path(): #리포트 저장 경로. 없으면 만듦
    if not os.path.exists(REPORT_PATH):
        os.mkdir(REPORT_PATH)
    else:
        print('start---')

def get_app(): 
    print('[+] get app...')
    # print('data',data)
    headers = {'Authorization' : API_KEY}
    response = requests.get(url=SERVER+'/api/v1/dynamic/get_apps',headers=headers)
    res_dict = json.loads(response.content.decode('utf-8'))
    if response.status_code == 200:
        # print(res_dict['identifier'],res_dict['apps'][0]['MD5'])
        return res_dict['identifier'],res_dict['apps'][0]['MD5']
    else:
        print("[-] Error Get Apps")
        exit(0)

def mobsfy_api(identifier):
    print("[+] MobSFying Start")
    data = {'identifier' : identifier}
    headers = {'Authorization' : API_KEY}
    response = requests.post(url=SERVER+'/api/v1/android/mobsfy',data=data,headers=headers)
    res_dict = json.loads(response.content.decode('utf-8'))
    if res_dict['status'] == "ok":
        print("[+] MobSFying Completed!")
        return True
    else:
        print(f"[-] {res_dict['error']}")

def start_dynamic_analysis(hash):
    print("[+] start_dynamic_analysis")
    data = {'hash' : hash}
    headers = {'Authorization' : API_KEY}
    response = requests.post(url=SERVER+'/api/v1/dynamic/start_analysis',data=data,headers=headers)
    res_dict = json.loads(response.content.decode('utf-8'))

    if response.status_code == 200:
        print("[+] Testing Environment is Ready")
    else:
        print(f"[-] {res_dict['error']}")

def frida_instrument(hash):
    print("[+] Frida Instrument")
    data = {'hash':hash,'default_hooks':'api_monitor,ssl_pinning_bypass,root_bypass,debugger_check_bypass','auxiliary_hooks':'','frida_code':FRIDA_BYPASS_CODE}
    print('ins',data)
    headers = {'Authorization' : API_KEY}
    response = requests.post(url=SERVER+'/api/v1/frida/instrument',data=data,headers=headers)
    res_dict = json.loads(response.content.decode('utf-8'))
    if response.status_code == 200:
        print("[+] Frida Works ")
    else:
        print(f"[-] {res_dict['error']}")

def frida_log(hash):
    data = {'hash':hash}
    headers = {'Authorization' : API_KEY}
    response = requests.post(url=SERVER+'/api/v1/frida/logs',data=data,headers=headers)
    print(response)
    res_dict = json.loads(response.content.decode('utf-8'))
    if response.status_code == 200:
        pprint.pprint(res_dict)
    else:
        print(f"[-] {res_dict['error']}")

def stop_dynamic_anaylsis(hash):
    headers = {'Authorization' : API_KEY}
    data = {'hash':hash}
    res = requests.post(url=SERVER+'/api/v1/dynamic/stop_analysis', headers=headers,data=data)
    res_dict = json.loads(res.content)
    if res.status_code == 200:
        print("[+] Dynamic Analysis Stoped")
    else:
        print(f"[-] {res_dict['error']}")

def get_frida_script(script='',device='android'):
    print("[+] get_frida_script")
    headers = {'Authorization' : API_KEY}
    data = {'scripts[]' : script, 'device':device}
    res = requests.post(url=SERVER+'/api/v1/frida/get_script', headers=headers,data=data)
    print('res',res.content)
    res_dict = json.loads(res.content.decode('utf-8'))
    print(res_dict)
    if res.status_code == 200:
        print("[+] get_frida_script")
    else:
        print(f"[-] {res_dict['error']}")

def frida_list_script(device='android'):
    print("[+]frida_list_script")
    headers = {'Authorization' : API_KEY}
    data = {'device':device}
    res = requests.post(url=SERVER+'/api/v1/frida/list_scripts', headers=headers,data=data)
    res_dict = json.loads(res.content.decode('utf-8'))
    print(res_dict)
    if res.status_code == 200:
        pass
    else:
        print(f"[-] {res_dict['error']}")

def get_dependencies(hash):
    print("[+]get_dependencies")
    headers = {'Authorization' : API_KEY}
    data = {'hash':hash}
    res = requests.post(url=SERVER+'/api/v1/frida/get_dependencies', headers=headers,data=data)
    res_dict = json.loads(res.content.decode('utf-8'))
    print(res_dict)
    if res.status_code == 200:
        pass
    else:
        print(f"[-] {res_dict['error']}")

def activity_ex(hash,test='exported'):
    print("[+]activity_exported")
    headers = {'Authorization' : API_KEY}
    data = {'hash':hash,'test':test}
    res = requests.post(url=SERVER+'/api/v1/android/activity', headers=headers,data=data)
    res_dict = json.loads(res.content.decode('utf-8'))
    print(res_dict)
    if res.status_code == 200:
        pass
    else:
        print(f"[-] {res_dict['error']}")

def activity_ac(hash,test='activity'):
    print("[+]activity_activity")
    headers = {'Authorization' : API_KEY}
    data = {'hash':hash,'test':test}
    res = requests.post(url=SERVER+'/api/v1/android/activity', headers=headers,data=data)
    res_dict = json.loads(res.content.decode('utf-8'))
    print(res_dict)
    if res.status_code == 200:
        pass
    else:
        print(f"[-] {res_dict['error']}")

def tls_tests(hash):
    print("[+]tls_tests")
    headers = {'Authorization' : API_KEY}
    data = {'hash':hash}
    res = requests.post(url=SERVER+'/api/v1/android/tls_tests', headers=headers,data=data)
    res_dict = json.loads(res.content.decode('utf-8'))
    print(res_dict)
    if res.status_code == 200:
        pass
    else:
        print(f"[-] {res_dict['error']}")

def make_json(hash):
    print('[+] json result')
    headers = {'Authorization' : API_KEY}
    data = {'hash':hash}
    response = requests.post(SERVER+'/api/v1/dynamic/report_json',data=data,headers=headers)
    with open(f"{REPORT_PATH}\\dinamicres.json", 'wb') as flip:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                flip.write(chunk)

if __name__ == "__main__":
    create_path()
    identifier,hash = get_app()
    mobsfy_api(identifier)
    start_dynamic_analysis(hash)
    get_frida_script()
    # frida_list_script()
    # get_dependencies(hash)  
    # tls_tests(hash)

    frida_instrument(hash)
    # time.sleep(7)
    # activity_ac(hash)
    # activity_ex(hash)

    frida_log(hash)
    # stop_dynamic_anaylsis(hash)

    make_json(hash)
