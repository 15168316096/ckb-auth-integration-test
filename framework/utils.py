import json
import os
import re
import subprocess
import time
import secrets

def get_project_root():
    current_path = os.path.dirname(os.path.abspath(__file__))
    pattern = r"(.*ckb-auth-integration-test)"
    matches = re.findall(pattern, current_path)
    if matches:
        root_dir = max(matches, key=len)
        return root_dir
    else:
        raise Exception("not found ckb-auth-integration-test dir")


def run_command(cmd):
    if cmd[-1] == "&":
        cmd1 = "{cmd} echo $! > pid.txt".format(cmd=cmd)
        print("cmd:{cmd}".format(cmd=cmd1))

        process = subprocess.Popen(cmd1, shell=True)
        time.sleep(1)
        print("process PID:", process.pid)
        with open("pid.txt", "r") as f:
            pid = int(f.read().strip())
            print("PID:", pid)
            return pid + 1

    print("cmd:{cmd}".format(cmd=cmd))
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    exit_code = process.returncode
    if exit_code != 0:
        print("Command failed with exit code:", exit_code)
        if stderr:
            print("Error:", stderr.decode('utf-8'))
        raise Exception(stderr.decode('utf-8'))
    if stderr.decode('utf-8') != "" and stdout.decode('utf-8') != "":
        print("wain:{result}".format(result=stderr.decode('utf-8')))
        print("result:{result}".format(result=stdout.decode('utf-8')))
        return stdout.decode('utf-8')
    print("result:{result}".format(result=stdout.decode('utf-8')))
    return stdout.decode('utf-8')


def clean(chain):
    run_command(f"rm -rf {chain}-*")


def process_solana_output(output):
    data = json.loads(output)

    # 获取message对应的值
    message_value = data["message"]

    # 获取signers中的公钥和签名
    signers = data["signers"]
    public_keys = []
    signatures = []

    for signer in signers:
        pubkey, signature = signer.split("=")
        public_keys.append(pubkey)
        signatures.append(signature)

    return message_value, public_keys, signatures


def check_container_status(container_name):
    cmd = f"docker ps -a | grep {container_name}"
    try:
        result = subprocess.check_output(cmd, shell=True, text=True)
        if "Up" in result:
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False


def get_container_name_from_output(output):
    try:
        container_info = output.strip().split()
        container_name = container_info[-1]
        return container_name
    except Exception as e:
        print(f"Error extracting container name: {e}")
        return None


def stop_and_remove_container(container_name):
    try:
        stop_cmd = f"docker stop {container_name}"
        subprocess.run(stop_cmd, shell=True, text=True, check=True)
        remove_cmd = f"docker rm {container_name}"
        subprocess.run(remove_cmd, shell=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error stopping or removing container: {e}")
        return False



def generateBytes(num=32):
    # 生成32个随机字节
    random_bytes = secrets.token_bytes(num)
    # 将随机字节转换为十六进制表示
    message = random_bytes.hex()
    print(message)
    return message