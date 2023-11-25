#!/usr/bin/env python3
import os
import getpass
import sys
import tempfile

# Check if we are root
if(getpass.getuser() != "root"):
    print("Please run this script as root..")
    exit(-1)
if(not os.path.exists("/opt/NoIpUpdater")):
    os.mkdir("/opt/NoIpUpdater")

os.system("cp -r src/* /opt/NoIpUpdater")

os.system("cp NoIpUpdater.service /etc/systemd/system/")

os.chdir("/opt/NoIpUpdater")

username = input("Enter your username:")
password = input("Enter your password:")
hostname = input("Enter your hostname:")

f = tempfile.NamedTemporaryFile()
f.write(password.encode())
f.flush()
systemd_creds_command = f"systemd-creds --name=noip encrypt {f.name} noip.cred"
# print(systemd_creds_command)
assert(os.system(systemd_creds_command)==0)
f.close()

f=open("env","w")
f.write("NOIP_HOSTNAME="+hostname+"\n")
f.write("NOIP_USERNAME="+username+"\n")
f.close()

