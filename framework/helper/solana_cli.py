from framework.utils import *

solana_path = f"cd {get_project_root()}/testcases/solana-release/bin"


def solana_keygen():
    """
    xueyanli@xueyanlideMacBook-Pro bin % solana-keygen new --force --no-bip39-passphrase
    Generating a new keypair
    Wrote new keypair to /Users/xueyanli/.config/solana/id.json
    ====================================================================
    pubkey: 69RyGvuAaCnuKjDgWycQdzDNjz9u2z4JudogjzdG493Z
    ====================================================================
    Save this seed phrase to recover your new keypair:
    wolf north mesh crazy man soap voice once rapid athlete iron between
    ====================================================================
    """
    cmd = f"{solana_path} && ./solana-keygen new --force --no-bip39-passphrase  -o /tmp/keypair.json"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    # 提取pubkey的值
    pubkey = None
    lines = result.stdout.splitlines()
    for line in lines:
        if "pubkey:" in line:
            pubkey = line.split(": ")[1]
            break

    return pubkey


def solana_signMessage(keypair, blockhash, pubKey, payer=None):
    """
    1、单个signer场景(--fee-payer {keypair})
    xueyanli@xueyanlideMacBook-Pro bin % solana transfer --from /Users/xueyanli/.config/solana/id.json --blockhash 6ukfHkjdBDsbF44dYVU8cTcQG8uzSdja884uHs1eVrdC 69RyGvuAaCnuKjDgWycQdzDNjz9u2z4JudogjzdG493Z 0 --output json --verbose --dump-transaction-message --sign-only

    which outputs

    {
    "blockhash": "6ukfHkjdBDsbF44dYVU8cTcQG8uzSdja884uHs1eVrdC",
    "message": "AQABAkxzUKeyLsP/6vDpIvRUtGh2/aKIgtTuQjJGKzu3dNbcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABXzgDejI3rdzjG5MTKixkH2S5v9cxjmVjK7mrDL4ySRwEBAgAADAIAAAAAAAAAAAAAAA==",
    "signers": [
    "69RyGvuAaCnuKjDgWycQdzDNjz9u2z4JudogjzdG493Z=5yeAu6Sdbi8ZDVfLLXoYayh2BgpNt7G1yPBAMytFAgWkLbCFaZahuAFAG1eZBVSNADRxfQ58ev3ZMw5Y1zTHFb7m"
    ]
    }
    2、多个signer场景
    xueyanli@192 bin % ./solana transfer --from /tmp/keypair.json --blockhash G8mW5A2r4ab8gnmCB4abus21BN8vyMa3hbLg91AcsMon F63cExLuPMUPVVLMsTBDno3mjxhX9pKc8FVNox1rjmpv 0 --output json --verbose --dump-transaction-message --sign-only

    {
      "blockhash": "G8mW5A2r4ab8gnmCB4abus21BN8vyMa3hbLg91AcsMon",
      "message": "AgABAzFGLntWeTb+SKJJwhopukuREqpcWO5NXpvRUpHBcQ6t0U54LMGUevZ8kg8hR8KCvgCI6ViDaDR1HG71r6+jH2sAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAODcr/CqxHAz+vV0RQv5C3knd7POPihOLWs1WaXbsSoJAQICAQEMAgAAAAAAAAAAAAAA",
      "signers": [
        "4KM3gAmBFT9hVZ5Zditju77KxtxpX3J4J6LvAcHsumzL=5FzgxFGM5w9VJAdvyCsZB6Wk85vzu7ybBBvAJbZyzogQ1Y8dLi5bS81vGBKmSPrDCqwpkove7rCPGSUFauG4ZFXv",
        "F63cExLuPMUPVVLMsTBDno3mjxhX9pKc8FVNox1rjmpv=5qeHoMm8kBCxbqkfcv8HfHCMsSfbvftVHLXxKjfmaPCo5jews56hFioNdnCtqu1b7ek1d7FwMzQ83oE4oh8yyZbt"
      ]
    }

    """
    if payer is not None:
        cmd = f"{solana_path} && ./solana transfer --from {keypair} --fee-payer {keypair} " \
              f"--blockhash {blockhash}{pubKey}" \
              f" 0 --output json --verbose --dump-transaction-message --sign-only "
    else:
        cmd = f"{solana_path} && ./solana-keygen new --force --no-bip39-passphrase"
        subprocess.run(cmd, shell=True, capture_output=True, text=True)
        cmd = f"{solana_path} && ./solana transfer --from {keypair} --blockhash {blockhash}{pubKey}" \
              f" 0 --output json --verbose --dump-transaction-message --sign-only "
    cmd = cmd.replace("\n", " ")

    # 运行cmd命令并获取输出结果
    result = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True, text=True)
    output = result.stdout.strip()

    # 处理输出
    return process_solana_output(output)


