prepare:
	echo "install ckb-auth-cli"
	sh prepare.sh

test:
	pytest -k testcases -s

clean:
	rm -rf ckb-auth
	rm -rf report
