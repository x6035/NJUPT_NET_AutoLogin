import os
import requests
from urllib.parse import urlencode
import socket
import time
import datetime

def get_current_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 使用连接到外部服务器的套接字来获取本地IP
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

current_ip = get_current_ip()


# Load usernames and passwords from the configuration file
def load_config(file_path):
    if not os.path.exists(file_path):
        print("配置文件不存在！")
        input()
        raise FileNotFoundError(f"配置文件不存在！: {file_path}")
    

    credentials = {}
    with open(file_path, 'r',encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip():
                if not line.startswith(';'):
                    key, value = line.split('=')
                credentials[key.strip()] = value.strip()
    return credentials

# Function to login to the server
def login_to_server(credentials, ip_address):
    base_url = "https://p.njupt.edu.cn:802/eportal/portal/login"
    params = {
        "callback": "dr1003",
        "login_method": "1",
        "user_password": credentials.get("password", ""),
        "wlan_user_ip": ip_address,
        "wlan_user_ipv6": "",
        "wlan_user_mac": "000000000000",
        "wlan_ac_ip": "",
        "wlan_ac_name": "",
        "jsVersion": "4.1.3",
        "terminal_type": "1",
        "lang": "zh-cn",
        "v": "10407",
        "lang": "zh"
    }

    if(credentials.get("type", "") == '1'):
        params["user_account"] = ',0,'+ f"{credentials.get('username', '')}"+'@njxy'
    elif(credentials.get("type", "") == '0'):
        params["user_account"] = ',0,'+ f"{credentials.get('username', '')}"
    else:
        params["user_account"] = ',0,'+ f"{credentials.get('username', '')}"+'@cmcc'
    
    url = f"{base_url}?{urlencode(params)}"

    response = requests.get(url, verify=True)
    
    if response.status_code == 200:
        print("网络连接正常...")
        # print(f" {response.text}")
        start_index = response.text.find('"msg":"') + len('"msg":"')
        end_index = response.text.find('","', start_index)
        msg_value = response.text[start_index:end_index]

        if(msg_value == 'AC999'):
            print("当前已登录！")
        elif(msg_value == 'Portal协议认证成功！'):
            print('登录成功！')
        else:
            print(msg_value)
    else:
        print(f"网络异常！状态码: {response.status_code}")
        

# Main function to load credentials and login
def main():
    # credentials_file_path = "./config.ini"  # Update this path
    credentials_file_path = "D:/wifi/config.txt"  # Update this path

    while(True):
        credentials = load_config(credentials_file_path)
        current_time = datetime.datetime.now()
        print("**********************************")
        print("时间:", current_time)
        login_to_server(credentials, current_ip)
        time.sleep(60)  # Pause for 60 seconds

if __name__ == "__main__":
    main()
