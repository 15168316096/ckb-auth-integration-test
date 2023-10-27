from framework.helper.ckb_auth_cli import *
from framework.helper.tronweb.tron_cli import *

class TestTron:

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def test_tron(self):
        signature, address = getSignatureOfTron()
        ckb_auth_verify_result = verify_tron_signature(address, signature)
        assert "Success" in ckb_auth_verify_result