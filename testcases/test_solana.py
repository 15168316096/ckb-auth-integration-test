from download import Solana
from framework.helper.ckb_auth_cli import *
from framework.helper.solana_cli import *
import pytest
from framework.utils import *

class TestSolana:
    pubkey = solana_keygen()

    @classmethod
    def setup_class(cls):
        blockchain = Solana()
        blockchain.install()
        blockchain.print_help()
        cls.pubkey = solana_keygen()
        cls.message = "e0dcaff0aac47033faf574450bf90b792777b3ce3e284e2d6b3559a5dbb12a09"
        # cls.pubKeyHash = get_pubKeyHashForSolana(cls.pubkey)
        # cls.msgToSign = get_messageForSolana(cls.pubKeyHash)
        cls.msgToSign = base58_str(cls.message)
        cls.message_value = cls.public_keys = cls.signatures = None

    # @classmethod
    # def teardown_class(cls):
    #     clean("solana")

    def test_signMessage(self):
        self.message_value, self.public_key, self.signature = solana_signMessage(
            "/tmp/keypair.json", self.msgToSign, self.pubkey)
        assert self.message_value is not None
        assert self.public_key == self.pubkey
        assert self.signature is not None

    def test_verifyMessage(self):
        self.message_value, self.public_key, self.signature = solana_signMessage(
            "/tmp/keypair.json", self.msgToSign, self.pubkey)
        # for i in range(len(self.public_keys)):
        result = verifyMsgForSolana(self.public_key, self.signature, self.message_value, 
        self.message)
        assert "Signature verification succeeded!" in result
