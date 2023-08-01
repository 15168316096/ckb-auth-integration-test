import json
import subprocess
import time
from framework.utils import get_project_root, check_container_status, get_container_name_from_output, \
    stop_and_remove_container

ckb_auth_path = f"{get_project_root()}/ckb-auth"


def start_service():
    start_ripple_cmd = f"bash {ckb_auth_path}/tools/rippled/start_rippled.sh"
    print(f"cmd: {start_ripple_cmd}")
    script_output = subprocess.run(start_ripple_cmd, shell=True, text=True, capture_output=True)
    if script_output.returncode == 0:
        docker_rippled_name = script_output.stdout.strip()
        print(f"DOCKER_RIPPLED_NAME: {docker_rippled_name}")
        return docker_rippled_name
    else:
        print(f"Error starting service: {script_output.stderr}")
        return None


def stop_service(container_name="ripple"):
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


def get_account_id_and_master_seed(DOCKER_RIPPLED_NAME):
    cmd = f"docker exec -i {DOCKER_RIPPLED_NAME} rippled -a wallet_propose"
    try:
        print(f"debug: {cmd}")
        # 休眠5秒，允许`rippled`容器完全启动和初始化。
        time.sleep(5)

        # 将`docker exec`命令的超时时间增加到30秒。
        result = subprocess.check_output(cmd, shell=True, text=True, timeout=30)

        # 从输出中提取JSON部分
        json_start = result.find("{")
        json_end = result.rfind("}")
        json_str = result[json_start:json_end+1]

        output_json = json.loads(json_str)
        account_id = output_json["result"]["account_id"]
        master_seed = output_json["result"]["master_seed"]
        print(f"debug222: {account_id, master_seed}")
        return account_id, master_seed
    except subprocess.TimeoutExpired as e:
        print(f"执行命令时发生超时：{e}")
        return None, None
    except subprocess.CalledProcessError as e:
        print(f"执行命令时出错：{e}")
        return None, None
    except KeyError as e:
        print(f"解析JSON输出时出错：{e}")
        return None, None


def get_tx_blob_from_rippled_sign(master_seed, ckb_message_hash, DOCKER_RIPPLED_NAME):
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

        cmd = f'docker exec -i {DOCKER_RIPPLED_NAME} rippled -a sign {master_seed} \'{json.dumps(tx_json)}\' offline'
        print(f"debug: {cmd}")
        # 休眠5秒，允许`rippled`容器完全启动和初始化。
        time.sleep(5)

        # 将`docker exec`命令的超时时间增加到30秒。
        result = subprocess.check_output(cmd, shell=True, text=True, timeout=30)

        # 查找JSON部分的开始和结束位置
        json_start = result.find("{")
        json_end = result.rfind("}")
        json_str = result[json_start:json_end + 1]

        # 尝试解析JSON部分
        output_json = json.loads(json_str)
        tx_blob = output_json["result"]["tx_blob"]
        print(f"[debug]tx_blob: {tx_blob}")
        return tx_blob
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None
    except KeyError as e:
        print(f"Error parsing JSON output: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

