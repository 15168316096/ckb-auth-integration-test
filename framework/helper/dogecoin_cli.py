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
    try:
        if blockchain.check_dogecoind_running():
            blockchain.print_help(path)
            dogecoin_cli = blockchain.get_dogecoin_cli(path)
            return dogecoin_cli
        else:print("start dogecoin Core failed")
    except Exception as e:
        print(e)



def get_dogecoin_address(dogecoin_cli):
    try:
        # cmd = f'cd {dogecoin_cli} && ./dogecoin-cli getaddressesbyaccount ""'
        # print(f"cmd:{cmd}")
        # result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        # addresses = result.stdout.strip().replace('[', '').replace(']', '').replace('"', '').split(', ')
        # return addresses[0]
        return "DDjoXsNFMo8iu59mkKF45ddcFoECUehovB"
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.returncode}")


def generateSignature(dogecoin_cli, address):
    # message = generateBytes()
    # print(f"message:{message}")
    # signMessage = f"cd {dogecoin_cli} && ./dogecoin-cli signmessage {address} {message}"
    # result = subprocess.run(f"{signMessage}", shell=True, stdout=subprocess.PIPE, text=True)
    # output = result.stdout.strip()
    # print(f"sign message: {output}")
    # return output, message
    return "IMdNZFx8IJpU0Omshlh//2HmqjbN89I29NK7zg6CvDByLR2Mq2zBoL864EY6XBdf4e2fmBobwtRghEeSq/fVWnA=", \
    "3d3f948b1f62a577673d489adbd1ab7a0da9d39e58938d1a20e598d041da1b5c"

def stopDogecoind():
    blockchain = Dogecoin()
    blockchain.stop_dogecoind()
