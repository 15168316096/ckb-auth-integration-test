from framework.utils import *


ckb_auth_path = f"{get_project_root()}/ckb-auth"

def install_ethereum():
    command = "git clone https://github.com/ethereum/go-ethereum.git && cd go-ethereum && make all"
    subprocess.run(f"{command}", shell=True)
    command = f"sudo cp -rf {get_project_root()}/go-ethereum/build/bin/ethkey geth /usr/local/bin/"
    subprocess.run(f"{command}", shell=True)