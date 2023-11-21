prepare:
	echo "install ckb-auth-cli"
	sh prepare.sh

testAll:
	cd testcases/ && python -m pytest -vv -s

testSolana:
	cd testcases/ && pytest test_sol* -vv -s

testBitcoin:
	cd testcases/ && pytest test_bit* -vv -s

testEth:
	cd testcases/ && pytest test_eth* -vv -s

testEos:
	cd testcases/ && pytest test_eos* -vv -s

testTron:
	cd testcases && pytest test_tron* -vv -s

testRipple:
	cd testcases && pytest test_ripple* -vv -s

testDogeCoin:
	cd testcases && pytest test_doge* -vv -s				

clean:
	sudo rm -rf ckb-auth
	sudo rm -rf report
