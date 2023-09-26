from framework.utils import *


ckb_auth_path = f"{get_project_root()}/ckb-auth"

def install_ethereum():
    # command = f"cd {get_project_root()} && git clone https://github.com/ethereum/go-ethereum.git && cd go-ethereum && make all"
    # subprocess.run(f"{command}", shell=True)
    command = f"cd {get_project_root()}/go-ethereum/build/bin/ && sudo cp -rf ethkey geth /usr/local/bin/"
    print(f"env:{command}")
    subprocess.run(f"{command}", shell=True)

def account_new():
    eth_password_file = "password.txt"
    with open(eth_password_file, "w") as password_file:
        password_file.write(str(random.randint(0, 999999999)))  # 使用随机数作为密码

    eth_account_dir = "account"
    subprocess.run(f"rm -rf {eth_account_dir}", shell=True)
    subprocess.run(f"mkdir -p {eth_account_dir}", shell=True)
    subprocess.run(f"geth account new --password {eth_password_file} --keystore {eth_account_dir}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    geth_command = f"geth account list --keystore {eth_account_dir}"
    result = subprocess.run(geth_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    eth_address = re.search(r'\{[a-f0-9]+\}', result.stdout).group(0)[1:-1]
    eth_privkey_file_path = re.search(r'keystore://[^ ]+', result.stdout).group(0).split("keystore:")[1]
    eth_password_file_path = f"{get_project_root()}/testcases/password.txt"
    print("Address:", eth_address)
    print("PrivateKeyFile:", eth_privkey_file_path)
    return eth_address, eth_privkey_file_path, eth_password_file_path

def verify_message_by_ethkey(eth_address, eth_signature, message_file=f"{get_project_root()}/message_file.bin"):
    cmd = f"ethkey verifymessage --msgfile {message_file} {eth_address} {eth_signature}"
    result = subprocess.check_output(cmd, shell=True, text=True)
    return result.strip()