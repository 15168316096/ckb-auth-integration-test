from download import Solana
from framework.helper.ckb_auth_cli import *
from framework.helper.solana_cli import *


class TestSolana:
    pubkey = solana_keygen()

    @classmethod
    def setup_class(cls):
        blockchain = Solana()
        blockchain.install()
        blockchain.print_help()
        cls.pubkey = solana_keygen()
        cls.pubKeyHash = get_pubKeyHashForSolana(cls.pubkey)
        cls.msgToSign = get_messageForSolana(cls.pubKeyHash)
        cls.message_value = cls.public_keys = cls.signatures = None

    @classmethod
    def teardown_class(cls):
        clean("solana")

    def test_signMessage(self):
        self.message_value, self.public_keys, self.signatures = solana_signMessage(
            "/tmp/keypair.json", self.msgToSign, self.pubkey)
        assert self.message_value is not None
        assert self.public_keys[1] == self.pubkey
        assert self.signatures is not None

    def test_verifyMessage(self):
        self.message_value, self.public_keys, self.signatures = solana_signMessage(
            "/tmp/keypair.json", self.msgToSign, self.pubkey)
        for i in range(len(self.public_keys)):
            result = verifyMsgForSolana(self.public_keys[i], self.signatures[i], self.message_value)
            assert "Signature verification succeeded!" in result
