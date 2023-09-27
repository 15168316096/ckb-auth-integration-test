from framework.helper.ckb_auth_cli import *
from framework.helper.ethereum_cli import *

class TestEth:
    def test_installGeth(self):
        install_ethereum()
        
    def test_sign_and_verify_msg_by_ethkey(self):
        eth_address, eth_privkey_file_path, eth_password_file_path  = account_new()
        sign_message = sign_message_eth(eth_password_file_path, eth_privkey_file_path)
        print(f"sign msg:{sign_message}")
        verify_msg_result = verify_message_by_ethkey(eth_address, sign_message)
        print(f"verify result:{verify_msg_result}")
        assert "Signature verification successful!" in verify_msg_result

    def test_sign_and_verify_msg_by_ckb_auth_cli(self):
        eth_address, eth_privkey_file_path, eth_password_file_path  = account_new()
        sign_message = sign_message_eth(eth_password_file_path, eth_privkey_file_path)
        print(f"sign msg:{sign_message}")
        verify_msg_result = verify_message_eth_by_ckbauth(eth_address, sign_message)
        print(f"verify result:{verify_msg_result}")
        assert "Ethereum Signature verification succeeded!" in verify_msg_result


    