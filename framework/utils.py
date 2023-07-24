import json
import os
import re
import subprocess
import time


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