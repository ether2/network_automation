# network_automation
collection of sanitized scripts I use to programtically complete network tasks

## cisco_sw_backup.py
script reads device_list.txt file, runs commands from command_list_switch.txt via netmiko's ssh connect handler. The output is saved to a local file at /day-month-year/hostname.txt

## firewall_reboot.yml
ansible playbook that reboots a FortiGate firewall remotely, waits for it to come back online and saves VPN tunnel info - name, remote gateway ip, status (up/down) to a hostname.txt file
