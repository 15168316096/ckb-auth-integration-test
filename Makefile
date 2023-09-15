prepare:
	echo "install ckb-auth-cli"
	sh prepare.sh

test:
	cd testcases/ && python -m pytest -vv -s

clean:
	sudo rm -rf ckb-auth
	sudo rm -rf report
