from framework.helper.ckb_auth_cli import *
from framework.helper.ripple_cli import *


class TestRipple:

    @classmethod
    def setup_class(cls):
        cls.DOCKER_RIPPLED_NAME = start_service()

    @classmethod
    def teardown_class(cls):
        stop_service()

    def test_signMessage(self):
        print(f"debug:{self.DOCKER_RIPPLED_NAME}")
        self.account_id, self.master_seed = get_account_id_and_master_seed(self.DOCKER_RIPPLED_NAME)
        self.ckb_message_hash = get_message_hash_ripple()
        tx_blob = get_tx_blob_from_rippled_sign(self.master_seed, self.ckb_message_hash, self.DOCKER_RIPPLED_NAME)
        assert tx_blob is not None

    def test_verifyMessage(self):
        self.account_id, self.master_seed = get_account_id_and_master_seed(self.DOCKER_RIPPLED_NAME)
        self.ckb_message_hash = get_message_hash_ripple()
        result = verify_ripple_signature(self.account_id,
                                         get_tx_blob_from_rippled_sign(self.master_seed, self.ckb_message_hash,
                                                                       self.DOCKER_RIPPLED_NAME),
                                         )
        assert "Signature verification succeeded" in result
