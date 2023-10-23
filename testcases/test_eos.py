from framework.helper.ckb_auth_cli import *
from framework.helper.eos_cli import *

class TestEOS:
    def test_eos(self):
        pubKey, privKey = acccount_new()
        sign_tx = sign_transaction(privKey)
        verify_result_cleos = validate_signatures(sign_tx)
        assert pubKey in verify_result_cleos[1]
        ckb_auth_verify_result = verify_eos_signature(pubKey, sign_tx)
        assert "Success" in ckb_auth_verify_result