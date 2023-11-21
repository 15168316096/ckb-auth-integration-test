import os
import time
import platform
import subprocess
from framework.utils import get_project_root

os_type = platform.system()


class Blockchain:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def download_tarball(tarball_url):
        tarball = tarball_url.split("/")[-1]
        subprocess.run(["wget", "-O", tarball, tarball_url])
        return tarball

    @staticmethod
    def extract_tarball(tarball):
        subprocess.run(["tar", "xvf", tarball, "-C", f"{get_project_root()}"])
        subprocess.run(["rm", tarball])

    @staticmethod
    def copy_files_to_path(src_dir, dest_path):
        dir_name = os.path.basename(src_dir)
        if os_type == "Linux":
            subprocess.run(["sudo", "cp", "-r", f"{src_dir}/*", dest_path])
        elif os_type == "Darwin":
            password = "Xue123"
            cmd = f'echo {password} | sudo -S cp -r {src_dir}/* {dest_path}'
            subprocess.run(cmd, shell=True)
        return dir_name

    def install(self):
        if os_type == "Linux":
            tarball_url = self.get_linux_tarball_url()
        elif os_type == "Darwin":
            tarball_url = self.get_darwin_tarball_url()
        else:
            raise NotImplementedError(f"Unsupported OS: {os_type}")

        tarball = self.download_tarball(tarball_url)
        self.extract_tarball(tarball)
        print(f"chain:{self.name}")
        print(f"{get_project_root()}/{tarball.split('-')[0]}-{tarball.split('-')[1]}/")
        if self.name == "bitcoin":
            command = f"sed -i.bak 's/^#networkactive=1/networkactive=0/' {get_project_root()}/bitcoin-25.0/bitcoin.conf"
            subprocess.run(command, shell=True)
        return f"{get_project_root()}/{tarball.split('-')[0]}-{tarball.split('-')[1]}/"
        # if f"{self.name}".find("monero") != -1:
        #     self.copy_files_to_path(f"{self.name}-*", "/usr/local/bin/")
        # else:
        #     self.copy_files_to_path(f"{self.name}-*", "/usr/local/")

    def print_help(self):
        raise NotImplementedError

    def get_linux_tarball_url(self):
        raise NotImplementedError

    def get_darwin_tarball_url(self):
        raise NotImplementedError


class Solana(Blockchain):
    def __init__(self):
        super().__init__("solana")

    def get_linux_tarball_url(self):
        return "https://github.com/solana-labs/solana/releases/download/v1.16.5/solana-release-x86_64" \
               "-unknown-linux-gnu.tar.bz2"

    def get_darwin_tarball_url(self):
        return "https://github.com/solana-labs/solana/releases/download/v1.16.4/solana-release-aarch64" \
               "-apple-darwin.tar.bz2"

    def print_help(self):
        print("use solana by abspath")
        # subprocess.run(["solana", "--help"])


class Monero(Blockchain):
    def __init__(self):
        super().__init__("monero")

    def get_linux_tarball_url(self):
        return "https://downloads.getmonero.org/cli/monero-linux-x64-v0.18.2.2.tar.bz2"

    def print_help(self):
        print("use monero-wallet-cli by abspath")
        # subprocess.run(["monero-wallet-cli", "--help"])


class Litecoin(Blockchain):
    def __init__(self):
        super().__init__("litecoin")

    def get_linux_tarball_url(self):
        return "https://download.litecoin.org/litecoin-0.21.2.2/linux/litecoin-0.21.2.2-x86_64-linux-gnu.tar.gz"

    def print_help(self):
        print("use litecoin-cli by abspath")
        # subprocess.run(["litecoin-cli", "--help"])

class Bitcoin(Blockchain):
    def __init__(self):
        super().__init__("bitcoin")

    def get_linux_tarball_url(self):
        return "https://bitcoincore.org/bin/bitcoin-core-25.0/bitcoin-25.0-x86_64-linux-gnu.tar.gz"

    def chmodCli(self, tarball_abspath):
        command = f"cd {tarball_abspath}bin/ && chmod +x bitcoin-cli && chmod +x bitcoind"
        subprocess.run(command, shell=True)

    def print_help(self, tarball_abspath):
        print(f"use bitcoind by abspath:{tarball_abspath}")

    def start_bitcoind(self, tarball_abspath):
        command = f"cd {tarball_abspath}bin/ &&  ./bitcoind -chain=regtest -daemonwait"
        print(f"command:{command}")
        max_wait_time = 300
        start_time = time.time()
        while True:
            output = subprocess.check_output(command, shell=True).decode("utf-8")
            time.sleep(10)
            if "Bitcoin Core starting" in output:
                print("bitcoin node is running")
                break
            elif time.time() - start_time > max_wait_time:
                print("Timeout: Bitcoin Core RPC server did not become available.")
                break
            else: 
                print("bitcoin node is not running")
                time.sleep(10)

    def check_bitcoind_running(self):
        ps_command = "ps -ef | grep bitcoind | grep -v grep"
        ps_output = subprocess.check_output(ps_command, shell=True).decode("utf-8")
        if "./bitcoind" in ps_output:
            return True
        else:
            return False    

    def get_bitcoin_cli(self, tarball_abspath):
        return f"{tarball_abspath}bin/"   

    def stop_bitcoind(self):
         command = "pkill bitcoind"
         subprocess.run(command, shell=True)


class Dogecoin(Blockchain):
    def __init__(self):
        super().__init__("dogecoin")

    def get_linux_tarball_url(self):
        return "https://github.com/dogecoin/dogecoin/releases/download/v1.14.6/dogecoin-1.14.6-x86_64-linux-gnu.tar.gz"

    def chmodCli(self, tarball_abspath):
        command = f"cd {tarball_abspath}bin/ && chmod +x dogecoin-cli && chmod +x dogecoind"
        subprocess.run(command, shell=True)

    def print_help(self, tarball_abspath):
        print(f"use dogecoind by abspath:{tarball_abspath}")

    def start_dogecoind(self, tarball_abspath):
        command = f"cd {tarball_abspath}bin/ &&  ./dogecoind -daemon -server=1 -waitforblockheight=10 &"
        print(f"command: {command}")
        subprocess.run(command, shell=True)

    def check_dogecoind_running(self):
        ps_command = "ps -ef | grep dogecoind | grep -v grep"
        ps_output = subprocess.check_output(ps_command, shell=True).decode("utf-8")
        if "./dogecoind" in ps_output:
            return True
        else:
            return False    

    def get_dogecoin_cli(self, tarball_abspath):
        return f"{tarball_abspath}bin/"   

    def stop_dogecoind(self):
         command = "pkill dogecoind"
         subprocess.run(command, shell=True)         
