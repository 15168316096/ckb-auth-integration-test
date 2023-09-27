from download import Bitcoin
from framework.helper.ckb_auth_cli import *
from framework.helper.bitcoin_cli import *
import pytest

# @pytest.mark.skip("debug")
class TestBitcoin:
    @classmethod
    def setup_class(cls):
        cls.cli = installBitcoinCore()

    @classmethod
    def teardown_class(cls):
        stopBitcoind()   
      
    def test_signMessageAndVerify(self):
        address, walletName = createWalletAndAddress(self.cli, generate_random_string(5))
        print(f"address: {address}, walletName: {walletName}")
        signMessage, message = generateSignature(self.cli, address, walletName)
        print(f"signMessage:{signMessage}")
        assert signMessage is not None
        result = verify_bitcoin_signature(address, signMessage, message)
        assert "Signature verification succeeded!" in result  

    