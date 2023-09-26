# ckb-auth-integration-test

## Goals

The goal of this project is to support ckb-auth compatibility with various blockchain networks. The tests ensure that ckb-auth functions as expected across different chains.
Inculde solana, Eth, Bitcoin, Ripple...


## Jobs

### Test

This job runs on `ubuntu-latest`.

Testing Steps:

```yaml
    - name: Install ckb-auth-cli
      run: make prepare

    - name: Run tests
      run: make test
