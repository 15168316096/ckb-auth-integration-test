from framework.helper.ckb_auth_cli import *
from framework.helper.bitcoin_cli import *


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

    def test_verifyMessageByUnisat(self):
        """
        verify message by unisat wallet
        """
        verify_cases = [
            {
                "address": "bc1ql9ju4rwv20k4ly7yxzev4und09wwexn9wspeta",
                "signature": "HEarX4AQUIqrwcebW6ra7yEDOLSbOCPwcVH5QTmYlmgXWrA6FjLzGCM5ggiujM8Ce7gyon+MeW2LJdpWlpXKHEI=",
                "message": "0011223344556677889900112233445500112233445566778899001122334455"
            },
            {
                "address": "tb1ql9ju4rwv20k4ly7yxzev4und09wwexn9yk62sw",
                "signature": "HAcDpCzFUF9+2WE3cUeNhX0HUCRQ3xf0p61gDZ4rjvYSePxF6zYlE5hfQob+PdClohJLV5JBwuTcjyIgOb4ZK+M=",
                "message": "0011223344556677889900112233445500112233445566778899001122334455"
            },
            {
                "address": "3HsqUZPg8BKi9q242W5fyFGGqzquPDBpWB",
                "signature": "HFhoFGzuZ/iB5EJ3KS/liI3CIdRtylR8Jvjo0LDtZbZrIuIOPkImcntE1TglmxPahYdxVofrKxopoP839Yo/Fng=",
                "message": "0011223344556677889900112233445500112233445566778899001122334455"
            },
            {
                "address": "2N9S3YJKhjdq4McebhdhYbCFY4M45DqGsW5",
                "signature": "HGnj9mK62Kl9l6RwnKuDZdItqDGp2VRJL0Hlv8JfMSwaewkwM1TJgZNCeJrkWEAArVo2pzihLrY/1jsELN1gDBE=",
                "message": "0011223344556677889900112233445500112233445566778899001122334455"
            },
            {
                "address": "n1rY3ZQi9YB5pMtdBvk79eyYEUsdv5K24b",
                "signature": "Gz1enxNMu/IBUTuHj3PQsVCixzen/Im6mRW8tfrfFKn/MTOyPuXyAhSrHYKtmB34yGgqZnixCh6IfimbyT7gD7E=",
                "message": "0011223344556677889900112233445500112233445566778899001122334455"
            },
            {
                "address": "1MLakWKjLWjq3FR1UMmjKjmDNVGvyLk6Tc",
                "signature": "G0c+GB5p6a9Dnrz/U3BzWnnAHAI5Bn2tjqG+Bm35UBQHDRHukng4n90exqSda4cEVcBbIAkEEEFikb0OIIpBPtY=",
                "message": "0011223344556677889900112233445500112233445566778899001122334455"
            }
        ]
        for verify_case in verify_cases:
            result = verify_bitcoin_signature_byUnisat(
                verify_case["address"],
                verify_case["signature"],
                verify_case["message"]
            )
            assert "Signature verification succeeded!" in result
