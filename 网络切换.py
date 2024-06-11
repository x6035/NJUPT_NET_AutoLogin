import subprocess
import pywifi
from pywifi import const
import time
import os

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

def is_ethernet_disabled(interface_name):
    result = subprocess.run(f'netsh interface show interface "{interface_name}"', capture_output=True, text=True, shell=True)
    if "Disabled" in result.stdout:
        return True
    else:
        return False

def disable_ethernet(interface_name):
    subprocess.run(f'netsh interface set interface "{interface_name}" admin=disable', shell=True)
    print(f"Disabled Ethernet interface: {interface_name}")

def enable_ethernet(interface_name):
    subprocess.run(f'netsh interface set interface "{interface_name}" admin=enable', shell=True)
    print(f"Enabled Ethernet interface: {interface_name}")

def connect_to_wifi(ssid, password):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    iface.disconnect()
    time.sleep(1)

    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)

    iface.connect(tmp_profile)
    time.sleep(10)  # Wait for the connection to establish

    if iface.status() == const.IFACE_CONNECTED:
        print(f"Connected to WiFi: {ssid}")
    else:
        print(f"Failed to connect to WiFi: {ssid}")

def disconnect_wifi():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    iface.disconnect()
    time.sleep(1)

    if iface.status() in [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]:
        print("Disconnected from WiFi")
    else:
        print("Failed to disconnect from WiFi")

def main():
    config_file_path = "./config.ini"  # Update this path
    # config_file_path = "D:/wifi/config.txt"  # Update this path
    config = load_config(config_file_path)

    ethernet_interface = config.get("ethernet_interface", "")
    wifi_ssid = config.get("wifi_ssid", "")
    wifi_password = config.get("wifi_password", "")

    if is_ethernet_disabled(ethernet_interface):
        enable_ethernet(ethernet_interface)
        disconnect_wifi()
    else:
        disable_ethernet(ethernet_interface)
        connect_to_wifi(wifi_ssid, wifi_password)

    input()

if __name__ == "__main__":
    main()
