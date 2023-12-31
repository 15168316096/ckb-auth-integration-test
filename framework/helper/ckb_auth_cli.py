import subprocess

from framework.utils import get_project_root, run_command

ckb_auth_cli_path = f"cd {get_project_root()}/ckb-auth/tools/ckb-auth-cli/target/debug/ && ./ckb-auth-cli "


def get_pubKeyHashForSolana(pubKey):
    """
    xueyanli@xueyanlideMacBook-Pro debug % ./ckb-auth-cli solana parse -a 69RyGvuAaCnuKjDgWycQdzDNjz9u2z4JudogjzdG493Z

    which outputs
    5592018a45281aa367730a7205a61b9588a59228
    """
    cmd = f"{ckb_auth_cli_path} solana parse -a {pubKey}"
    print(f"pubkeyHash:{run_command(cmd)}")
    return run_command(cmd)


def get_messageForSolana(parseKey):
    """
    xueyanli@xueyanlideMacBook-Pro debug % ./ckb-auth-cli solana generate -p 5592018a45281aa367730a7205a61b9588a59228

    which outputs the message to sign
    6ukfHkjdBDsbF44dYVU8cTcQG8uzSdja884uHs1eVrdC
    """
    cmd = f"{ckb_auth_cli_path} solana generate -p {parseKey}"
    return run_command(cmd)


def verifyMsgForSolana(pubKey, signature, msgSigned, msgToSign):
    """
    xueyanli@xueyanlideMacBook-Pro debug % ./ckb-auth-cli solana verify -a 69RyGvuAaCnuKjDgWycQdzDNjz9u2z4JudogjzdG493Z -s 4SXv2jWSqc5d8eyuFndhJnuCSiWgiPMKmd5ypCZWEEpw6ThMZ2vpj3XxJtYr4E4Yjpq9Fy3AwXHkYQfYADzDPXeY -m AQABAkxzUKeyLsP/6vDpIvRUtGh2/aKIgtTuQjJGKzu3dNbcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADg3K/wqsRwM/r1dEUL+Qt5J3ezzj4oTi1rNVml27EqCQEBAgAADAIAAAAAAAAAAAAAAA==
    Signature verification succeeded!
    """
    cmd = f"{ckb_auth_cli_path} solana verify -a {pubKey} -s {signature} --solanamessage {msgSigned} -m {msgToSign}"
    return run_command(cmd)


def get_message_hash_ripple(
        ckb_sign_message="0011223344556677889900112233445566778899001122334455667788990011"):
    try:
        cmd = f"{ckb_auth_cli_path} ripple parse --hex_to_address {ckb_sign_message}"
        print(f"debug555:{cmd}")
        result = subprocess.check_output(cmd, shell=True, text=True)
        ckb_message_hash = result.strip()
        print(f"[debug]ckb_message_hash:{ckb_message_hash}")
        return ckb_message_hash
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None


def verify_ripple_signature(ripple_address_id, tx_blob,
                            ckb_sign_message="0011223344556677889900112233445566778899001122334455667788990011"):
    try:
        cmd = f'{ckb_auth_cli_path} ripple verify -p {ripple_address_id} -s {tx_blob} -m {ckb_sign_message}'
        result = subprocess.check_output(cmd, shell=True, text=True)
        return result.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None

      
def verify_bitcoin_signature(address, signMessage, message):
    
    cmd = f"{ckb_auth_cli_path} bitcoin verify -a {address} -s {signMessage} -m {message}"
    return run_command(cmd)

def sign_message_eth(eth_password_file, eth_privkey_file):
    message="0011223344556677889900112233445500112233445566778899001122334455"
    message_file=f"{get_project_root()}/message_file.bin"
    command = f"{ckb_auth_cli_path} ethereum generate -m {message} --msgfile {message_file}"
    run_command(command)
    cmd = f"ethkey signmessage --msgfile {message_file} --passwordfile {eth_password_file} {eth_privkey_file}"
    result = subprocess.check_output(cmd, shell=True, text=True)
    return result.strip().split("Signature: ")[1]

def verify_message_eth_by_ckbauth(eth_address, eth_signature, message="0011223344556677889900112233445500112233445566778899001122334455"):
    cmd = f"{ckb_auth_cli_path} ethereum verify -a {eth_address} -s {eth_signature} -m {message}"
    result = subprocess.check_output(cmd, shell=True, text=True)
    return result.strip()

def verify_eos_signature(pubkey, signature, chain_id="00112233445566778899aabbccddeeff00000000000000000000000000000000", 
                         message="00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff"):
    cmd = f'{ckb_auth_cli_path} eos verify --pubkey {pubkey} --signature {signature[0]}  --chain_id {chain_id} --message {message}'
    print("-----",cmd)
    result = subprocess.check_output(cmd, shell=True, text=True)
    return result

def verify_tron_signature(account, signature, message="00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff"):
    cmd = f'{ckb_auth_cli_path} tron verify -a {account} -s {signature} -m {message}'
    result = subprocess.check_output(cmd, shell=True, text=True)
    return result
    
def verify_dogecoin_signature(address, signMessage, message):
    
    cmd = f"{ckb_auth_cli_path} dogecoin verify -a {address} -s {signMessage} -m {message}"
    return run_command(cmd)