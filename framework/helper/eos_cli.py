import subprocess
import json
from framework.utils import *

ckb_auth_path = f"{get_project_root()}/ckb-auth"

def acccount_new():
    cmd = "cleos create key --to-console"
    result = subprocess.check_output(cmd, shell=True, text=True)
    private_key = None
    public_key = None
    lines = result.strip().split('\n')
    for line in lines:
        if line.startswith("Private key:"):
            private_key = line.split("Private key: ")[1].strip()
        elif line.startswith("Public key:"):
            public_key = line.split("Public key: ")[1].strip()
    return public_key, private_key

def sign_transaction(private_key, chain_id="0112233445566778899aabbccddeeff00000000000000000000000000000000",
                      message="0112233445566778899aabbccddeeff00112233445566778899aabbccddeeff"):
    message = message.strip()
    if len(message) % 2 != 0:
        message = '0' + message
    cmd = f'cleos sign -k {private_key} -c {chain_id} "{{ \\"context_free_data\\": [\\"{message}\\"] }}"'
    print(f"cmd:{cmd}")
    result = subprocess.check_output(cmd, shell=True, text=True)
    try:
        parsed_output = json.loads(result)
        signatures = parsed_output.get('signatures', [])
        if signatures:
            return signatures
    except json.JSONDecodeError:
        pass
    return None



def validate_signatures(signatures, chain_id="00112233445566778899aabbccddeeff00000000000000000000000000000000", message=["00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff"]
):
    cmd = f'cleos validate signatures -c {chain_id} "{{ \\"signatures\\": {json.dumps(signatures)}, \\"context_free_data\\": {json.dumps(message)} }}"'
    pattern = r'\["SIG_K1_[^"]+"\]'
    cmd = re.sub(pattern, lambda x: x.group().replace('"', '\\"'), cmd)
    result = subprocess.check_output(cmd, shell=True, text=True)
    return result.strip().split('\n')