import json
import subprocess

from framework.utils import get_project_root, check_container_status, get_container_name_from_output, \
    stop_and_remove_container

ckb_auth_path = f"cd {get_project_root()}/ckb-auth"


def start_service():
    start_ripple_cmd = f"source {ckb_auth_path}/tools/rippled/start_rippled.sh"
    subprocess.run(start_ripple_cmd, shell=True, capture_output=True, text=True)
    if check_container_status("ripple"):
        print(f"start ripple service succ!!")
    else:
        print(f"start fail and check env!!")

def stop_service(container_name = "ripple"):
    cmd = "docker ps -a | grep " + container_name
    try:
        result = subprocess.check_output(cmd, shell=True, text=True)
        container_name = get_container_name_from_output(result)
    except subprocess.CalledProcessError as e:
        print(f"Error checking container status: {e}")
        return

    if container_name:
        if check_container_status(container_name):
            if stop_and_remove_container(container_name):
                print(f"Container '{container_name}' stopped and removed successfully.")
            else:
                print(f"Failed to stop or remove container '{container_name}'.")
        else:
            print(f"Container '{container_name}' is not running.")
    else:
        print(f"Container '{container_name}' not found.")


def get_account_id_and_master_seed():
    cmd = "RIPPLED_CMD wallet_propose"
    try:
        result = subprocess.check_output(cmd, shell=True, text=True)
        output_json = json.loads(result)
        account_id = output_json["result"]["account_id"]
        master_seed = output_json["result"]["master_seed"]
        return account_id, master_seed
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None, None
    except KeyError as e:
        print(f"Error parsing JSON output: {e}")
        return None, None


def get_tx_blob_from_rippled_sign(master_seed, ckb_message_hash):
    try:
        tx_json = {
            "TransactionType": "Payment",
            "Account": ckb_message_hash,
            "Destination": "ra5nK24KXen9AHvsdFTKHSANinZseWnPcX",
            "Amount": {
                "currency": "USD",
                "value": "1",
                "issuer": ckb_message_hash
            },
            "Sequence": 360,
            "Fee": "10000"
        }

        cmd = f'RIPPLED_CMD sign {master_seed} \'{json.dumps(tx_json)}\' offline'
        result = subprocess.check_output(cmd, shell=True, text=True)
        tx_blob = json.loads(result)["result"]["tx_json"]["tx_blob"]
        return tx_blob
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None
    except KeyError as e:
        print(f"Error parsing JSON output: {e}")
        return None



