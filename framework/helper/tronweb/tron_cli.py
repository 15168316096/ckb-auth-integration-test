import subprocess
import sys, re
sys.path.append('..') 
from framework.utils import get_project_root

tron_shell_path = f"cd {get_project_root()}/framework/helper/tronweb/"



def getSignatureOfTron():
    global sign, address
    cmd = f"{tron_shell_path} && node main.js"
    result = subprocess.check_output(cmd, shell=True, text=True)
    sign_match = re.search(r"sign: (0x[0-9a-fA-F]+)", result)
    if sign_match:
        sign = sign_match.group(1)
        print(f"\nSign: {sign} \n")

    address_match = re.search(r"address: ([A-Za-z0-9]+)", result)

    if address_match:
        address = address_match.group(1)
        print(f"Address: {address}")

    return sign, address    