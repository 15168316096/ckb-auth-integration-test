from framework.helper.ckb_auth_cli import *
from framework.helper.ripple_cli import *
from framework.helper.solana_cli import *


class TestSolana:

    @classmethod
    def setup_class(cls):
        start_service()
        cls.account_id, cls.master_seed = get_account_id_and_master_seed()
        cls.ckb_message_hash = get_message_hash_ripple()

    @classmethod
    def teardown_class(cls):
        stop_service()

    def test_signMessage(self):
        tx_blob = get_tx_blob_from_rippled_sign(self.master_seed, self.ckb_message_hash)
        assert tx_blob is not None

    def test_verifyMessage(self):
        result = verify_ripple_signature(self.account_id,
                                get_tx_blob_from_rippled_sign(self.master_seed, self.ckb_message_hash),
                                )
        assert "Signature verification succeeded" in result

