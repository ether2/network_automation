# script reads device_list.txt file, runs commands from command_list_switch.txt via netmiko's ssh connect handler
# The output is saved to a local file at /day-month-year/hostname.txt

from getpass import getpass
import netmiko
from netmiko import ConnectHandler
import time
import re
import os
from datetime import date

def open_ssh_conn(ip,device_function,username,password,enable,newfile_dir):
    print('[**info**] backing up device %s....'%ip)
    try: 
        cisco_rtsw = {
            'device_type': 'cisco_ios',
            'host': ip,
            'username': username,
            'password': password,
            'secret': enable,
        }   
        conn = ConnectHandler(**cisco_rtsw)
        conn.enable()
        hostname = conn.send_command('show run | i hostname').split(' ')[1]
        if device_function == "router":
            selected_cmd_file = open('command_list_router.txt', 'r')
            selected_cmd_file.seek(0)
        elif device_function == "switch":
            selected_cmd_file = open('command_list_switch.txt', 'r')
            selected_cmd_file.seek(0)

        new_f = open(newfile_dir+'/'+hostname+'.txt','w+')
        for each_line in selected_cmd_file.readlines():
            new_f.write('%s#%s\n'%(hostname,each_line))
            if re.search('% Invalid input detected at', conn.send_command(each_line)):
                print('[**info**] invalid \"%s\" syntax device %s' %(each_line.replace('\n',''),hostname))
            else:
                new_f.write(conn.send_command(each_line))
        selected_cmd_file.close()
        new_f.close()
        conn.disconnect()
        print('[**info**] done for device %s (%s)\n'%(hostname,ip))
    except netmiko.NetmikoAuthenticationException:
        print("[[**error**] invalid username or password]"%(ip))
    except netmiko.NetmikoTimeoutException:
        print("[**error**] connection timeout"%(ip))
    except ValueError:
        print("[**error**] failed to enter priv mode"%(ip))

if __name__ == '__main__':
    device_list = open('device_list.txt','r')
    ip,device_function, = [],[]
    newfile_dir = "/Users/gmcomie/Desktop/netmiko/%s/"%date.today().strftime("%d-%m-%Y")
    try:
        print("[**info**] creating new folder %s\n"%newfile_dir)
        os.mkdir(newfile_dir)
    except FileExistsError:
        print("[**error**] Folder %s exists!\n"%newfile_dir)
    for x in range(len(device_list.readlines())):
        device_list.seek(0)
        ip.append(device_list.readlines()[x].split(',')[0].rstrip('\n'))
        device_list.seek(0)
        device_function.append(device_list.readlines()[x].split(',')[1].rstrip('\n'))     
    device_list.close()
    my_user = input("Please enter username: ")
    print()
    my_pass = getpass("Please enter enable pass: ")
    print()
    try:
        for x in range(len(ip)):
            open_ssh_conn(ip[x],device_function[x],my_user,my_pass,my_pass,newfile_dir)
            if x == len(ip)-1:
                print('[**info**] backup is complete')
    except KeyboardInterrupt:
        print("[**error**] backup task cancelled - keyboard interrupt]")
