from download import Dogecoin
from framework.helper.ckb_auth_cli import *
from framework.helper.dogecoin_cli import *
import pytest

class TestDogecoin:
    @classmethod
    def setup_class(cls):
        cls.cli = installDogecoinCore()

    @classmethod
    def teardown_class(cls):
        stopDogecoind()
      
    def test_signMessageAndVerify(self):
        address = get_dogecoin_address(self.cli)
        print(f"address: {address}")
        signMessage, message = generateSignature(self.cli, address)
        print(f"signMessage:{signMessage}")
        assert signMessage is not None
        result = verify_dogecoin_signature(address, signMessage, message)
        assert "Signature verification succeeded!" in result  

    