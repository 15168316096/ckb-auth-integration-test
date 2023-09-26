import os
import json
import subprocess
import time
from framework.utils import *
from download import Bitcoin

ckb_auth_path = f"{get_project_root()}/ckb-auth"

def installBitcoinCore():
    blockchain = Bitcoin()
    # path = blockchain.install()
    # blockchain.chmodCli(path)
    path = "/workspaces/ckb-auth-integration-test/bitcoin-25.0/"
    blockchain.start_bitcoind(path)
    # max_wait_time = 300  # 最大等待时间，单位秒
    # start_time = time.time()
    # while not blockchain.check_bitcoind_running():
    #     if time.time() - start_time > max_wait_time:
    #         print("wait timeout, bitcoind server not run")
    #         break
    #     time.sleep(5)

    # if blockchain.check_bitcoind_running():
    #     print("bitcoind server running")
    # else:
    #     print("wait timeout, bitcoind server not run")
    blockchain.print_help(path)
    bitcoin_cli = blockchain.get_bitcoin_cli(path)
    return bitcoin_cli

def createWalletAndAddress(bitcoin_cli, walletName="Test"):
    create_wallet_command = f"./bitcoin-cli  -chain=regtest createwallet {walletName}"
    get_newaddress_command = "./bitcoin-cli -chain=regtest getnewaddress label1 legacy"
    print(f"wallet:{create_wallet_command}")
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
    

