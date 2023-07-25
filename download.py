import os
import platform
import subprocess

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
        subprocess.run(["tar", "xvf", tarball])

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
