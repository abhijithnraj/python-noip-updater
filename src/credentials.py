import os
hostname = os.environ["NOIP_HOSTNAME"]
username = os.environ["NOIP_USERNAME"]
cred_loc = os.environ["CREDENTIALS_DIRECTORY"]
with open(os.path.join(cred_loc,"noip"),"r") as f:
    password = f.read().strip()

