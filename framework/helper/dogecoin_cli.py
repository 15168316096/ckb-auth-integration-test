import os
import json
import subprocess
import time
from framework.utils import *
from download import Dogecoin

ckb_auth_path = f"{get_project_root()}/ckb-auth"

def installBitcoinCore():
    blockchain = Dogecoin()
    path = blockchain.install()
    blockchain.chmodCli(path)
    blockchain.start_dogecoind(path)
    blockchain.print_help(path)
    dogecoin_cli = blockchain.get_dogecoin_cli(path)
    return dogecoin_cli

def generateAddress(dogecoin_cli):
    get_newaddress_command = f"./dogecoin-cli getaddressesbyaccount """
    print(f"address:{get_newaddress_command}")
    # 创建钱包
    subprocess.run(f"cd {bitcoin_cli} && {create_wallet_command}", shell=True)

    # 获取新地址
    result = subprocess.run(f"cd {bitcoin_cli} && {get_newaddress_command}", shell=True, stdout=subprocess.PIPE, text=True)
    output = result.stdout.strip()

    print(f"new_address: {output}")
    return output, walletName 

def generateSignature(bitcoin_cli, address, walletName):
    message = generateBytes()
    print(f"message:{message}")
    signMessage =f"./bitcoin-cli -chain=regtest -rpcwallet={walletName} signmessage {address} {message} "
    result = subprocess.run(f"cd {bitcoin_cli} && {signMessage}", shell=True, stdout=subprocess.PIPE, text=True)
    output = result.stdout.strip()
    print(f"sign message: {output}")
    return output, message
    
def stopBitcoind():
     blockchain = Bitcoin()
     blockchain.stop_bitcoind()   
    

