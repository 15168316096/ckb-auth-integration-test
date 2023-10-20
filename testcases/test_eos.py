from framework.helper.ckb_auth_cli import *
from framework.helper.eos_cli import *

class TestEOS:
    def test_demo(self):
        pubKey, privKey = acccount_new()
        print(f"pubKey:{pubKey}, privKey:{privKey}")
        sign_tx = sign_transaction(privKey)
        print(f"sign_transaction:{sign_tx}")
        verify_result_cleos = validate_signatures(sign_tx)
        print(f"verify result:{verify_result_cleos}")
        assert pubKey in verify_result_cleos
        result = verify_eos_signature(pubKey, sign_tx)
        assert result == "Success"