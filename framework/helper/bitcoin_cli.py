import os
import json
import subprocess
import time
from framework.utils import *
from download import Bitcoin

ckb_auth_path = f"{get_project_root()}/ckb-auth"

def installBitcoinCore():
    blockchain = Bitcoin()
    path = blockchain.install()
    blockchain.chmodCli(path)
    blockchain.start_bitcoind(path)
    blockchain.print_help(path)
    bitcoin_cli = blockchain.get_bitcoin_cli(path)
    return bitcoin_cli

def createWalletAndAddress(bitcoin_cli, walletName="Test"):
    create_wallet_command = f"./bitcoin-cli createwallet {walletName}"
    get_newaddress_command = "./bitcoin-cli getnewaddress label1 legacy"

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
    signMessage =f"./bitcoin-cli -rpcwallet={walletName} signmessage {address} {message}"
    result = subprocess.run(f"cd {bitcoin_cli} && {signMessage}", shell=True, stdout=subprocess.PIPE, text=True)
    output = result.stdout.strip()
    print(f"sign message: {output}")
    return output, message
    
    

