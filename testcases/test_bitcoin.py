from download import Bitcoin
from framework.helper.ckb_auth_cli import *
from framework.helper.bitcoin_cli import *

@pytest.mark.skip("debug")
class TestBitcoin:
    def test_signMessageAndVerify(self):
        cli = installBitcoinCore()
        address, walletName = createWalletAndAddress(cli, generate_random_string(5))
        print(f"address: {address}, walletName: {walletName}")
        signMessage, message = generateSignature(cli, address, walletName)
        print(f"signMessage:{signMessage}")
        assert signMessage is not None
        result = verify_bitcoin_signature(address, signMessage, message)
        assert "Signature verification succeeded!" in result   


    