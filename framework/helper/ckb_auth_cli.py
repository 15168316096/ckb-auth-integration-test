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
    return run_command(cmd)


def get_messageForSolana(parseKey):
    """
    xueyanli@xueyanlideMacBook-Pro debug % ./ckb-auth-cli solana generate -p 5592018a45281aa367730a7205a61b9588a59228

    which outputs the message to sign
    6ukfHkjdBDsbF44dYVU8cTcQG8uzSdja884uHs1eVrdC
    """
    cmd = f"{ckb_auth_cli_path} solana generate -p {parseKey}"
    return run_command(cmd)


def verifyMsgForSolana(pubKey, signature, message):
    """
    xueyanli@xueyanlideMacBook-Pro debug % ./ckb-auth-cli solana verify -a 69RyGvuAaCnuKjDgWycQdzDNjz9u2z4JudogjzdG493Z -s 4SXv2jWSqc5d8eyuFndhJnuCSiWgiPMKmd5ypCZWEEpw6ThMZ2vpj3XxJtYr4E4Yjpq9Fy3AwXHkYQfYADzDPXeY -m AQABAkxzUKeyLsP/6vDpIvRUtGh2/aKIgtTuQjJGKzu3dNbcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADg3K/wqsRwM/r1dEUL+Qt5J3ezzj4oTi1rNVml27EqCQEBAgAADAIAAAAAAAAAAAAAAA==
    Signature verification succeeded!
    """
    cmd = f"{ckb_auth_cli_path} solana verify -a {pubKey} -s {signature} -m {message}"
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
    try:
        cmd = f"ckb-auth-cli bitcoin verify -a {address} -s {signMessage} -m {message}"
        result = subprocess.check_output(cmd, shell=True, text=True)
        return result.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")  
        return None  