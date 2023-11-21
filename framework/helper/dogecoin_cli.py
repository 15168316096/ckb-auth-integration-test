import os
import json
import subprocess
import time
from framework.utils import *
from download import Dogecoin

ckb_auth_path = f"{get_project_root()}/ckb-auth"


def installDogecoinCore():
    blockchain = Dogecoin()
    path = blockchain.install()
    blockchain.chmodCli(path)
    blockchain.start_dogecoind(path)
    blockchain.print_help(path)
    dogecoin_cli = blockchain.get_dogecoin_cli(path)
    return dogecoin_cli


def get_dogecoin_address(dogecoin_cli):
    try:
        cmd = f'cd {dogecoin_cli} && ./dogecoin-cli getaddressesbyaccount ""'
        print(f"cmd:{cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        addresses = result.stdout.strip().replace('[', '').replace(']', '').replace('"', '').split(', ')
        return addresses[0]
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.returncode}")
        print(e.output)


def generateSignature(dogecoin_cli, address):
    message = generateBytes()
    print(f"message:{message}")
    signMessage = f"./dogecoin-cli signmessage {address} {message}"
    result = subprocess.run(f"cd {dogecoin_cli} && {signMessage}", shell=True, stdout=subprocess.PIPE, text=True)
    output = result.stdout.strip()
    print(f"sign message: {output}")
    return output, message


def stopDogecoind():
    blockchain = Dogecoin()
    blockchain.stop_dogecoind()
