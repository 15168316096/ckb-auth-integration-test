prepare:
	echo "install ckb-auth-cli"
	sh prepare.sh

test:
	cd testcases/ && python3 -m pytest -vv -s

clean:
	rm -rf ckb-auth
	rm -rf report
