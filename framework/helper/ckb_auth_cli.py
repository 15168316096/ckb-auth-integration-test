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
