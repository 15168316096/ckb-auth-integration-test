prepare:
	echo "install ckb-auth-cli"
	sh prepare.sh

test:
	python -m pytest

clean:
	rm -rf ckb-auth
	rm -rf report
