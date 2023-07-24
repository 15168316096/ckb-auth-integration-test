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
        subprocess.run(["tar", "xvzf", tarball])

    @staticmethod
    def copy_files_to_path(src_dir, dest_path):
        dir_name = os.path.basename(src_dir)
        subprocess.run(["sudo", "cp", "-r", f"{src_dir}/*", dest_path])
        return dir_name

    def install(self):
        raise NotImplementedError

    def print_help(self):
        raise NotImplementedError


class Solana(Blockchain):
    def __init__(self):
        super().__init__("solana")
        if os_type == "Linux":
            self.tarball_url = "https://github.com/solana-labs/solana/releases/download/v1.16.5/solana-release-x86_64" \
                               "-unknown-linux-gnu.tar.bz2"
        elif os_type == "Dariwn":
            self.tarball_url = "https://github.com/solana-labs/solana/releases/download/v1.16.4/solana-release-aarch64" \
                               "-apple-darwin.tar.bz2 "

    def install(self):
        tarball = self.download_tarball(self.tarball_url)
        self.extract_tarball(tarball)
        print(f"{self.name}")
        self.copy_files_to_path(f"{self.name}-*", "/usr/local/")

    def print_help(self):
        subprocess.run(["solana", "--help"])


class Monero(Blockchain):
    def __init__(self):
        super().__init__("monero")
        if os_type == "Linux":
            self.tarball_url = "https://downloads.getmonero.org/cli/monero-linux-x64-v0.18.2.2.tar.bz2"

    def install(self):
        tarball = self.download_tarball(self.tarball_url)
        self.extract_tarball(tarball)
        self.copy_files_to_path(f"{self.name}-*", "/usr/local/bin/")

    def print_help(self):
        subprocess.run(["monero-wallet-cli", "--help"])


class Litecoin(Blockchain):
    def __init__(self):
        super().__init__("litecoin")
        if os_type == "Linux":
            self.tarball_url = "https://download.litecoin.org/litecoin-0.21.2.2/linux/litecoin-0.21.2.2-x86_64-linux-gnu" \
                           ".tar.gz "

    def install(self):
        tarball = self.download_tarball(self.tarball_url)
        self.extract_tarball(tarball)
        self.copy_files_to_path(f"{self.name}-*", "/usr/local/")

    def print_help(self):
        subprocess.run(["litecoin-cli", "--help"])

