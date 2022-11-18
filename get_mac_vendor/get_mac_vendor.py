# for each line in a cisco switch mac address table, this script appends the mac address vendor description

from getpass import getpass
import netmiko
from netmiko import ConnectHandler
import time
import re
import os
from datetime import date

formatted_mac_list = []
output_list = []
input_list = formatted_mac_list
wireshark_list = open("wireshark.txt", "r").readlines()
wireshark_new_list = [] 
macAddressRegex = re.compile(r'([0-9a-z]{4}.){2}[0-9a-z]{4}')
i = 0
j = 0
z = 0
p = 0
q = 0

newfile_dir = "mac_address_output/%s/"%date.today().strftime("%d-%m-%Y")
try:
    print("[**info**] Creating new folder at %s\n"%newfile_dir)
    os.mkdir(newfile_dir)
except FileExistsError:
    print("[**error**] folder %s xxists!\n"%newfile_dir)

net_connect = ConnectHandler(
    device_type="cisco_ios",
    host=input("Please enter IP address: "),
    #host="10.0.0.1",
    #username="$CISCO_SW_USER",
    username = input("Please enter usename: "),
    password = getpass(),
)

net_connect

hostname = net_connect.send_command('show run | i hostname').split(' ')[1]
output = net_connect.send_command("show mac address-table")
output2 = output.split("\n")
output2.pop()
output2 = output2[5:]

while p < len(output2):
    try:
        x = macAddressRegex.search(output2[p])
        formatted_mac_list.append(x.group())
        q += 1
    except:
        print("[**info**] no matching mac address found on line " + str(p))
    p += 1

while j < len(wireshark_list):
    wireshark_new_list.append(wireshark_list[j].split()[0])
    j += 1

for item in input_list:
    while i < len(input_list):
        x = input_list[i].upper().replace('.', '')[0:7]
        y = x[:2] + ':' + x[2:4] + ':' + x[4:6]
        try:
            z = wireshark_new_list.index(y)
            output_list.append(output2[i].strip() + " >>>>> " + re. sub('\s+',' ', wireshark_list[z].strip()))
        except:
            output_list.append(output2[i].strip() + " >>>>> " "mac address not found in Wireshark's vendor list")
        i += 1

with open(newfile_dir+'/'+hostname+'.txt','w+') as nfd:
    for item in output_list:
        nfd.write("%s\n" % item)
