create-service:
	sudo cp services/forexwebapp.service /etc/systemd/system/forexwebapp.service

run-service:
	sudo systemctl daemon-reload
	sudo systemctl enable forexwebapp.service
	sudo systemctl start forexwebapp.service

check-service:
	sudo systemctl status forexwebapp.service

restart-service:
	sudo systemctl restart forexwebapp.service

stop-service:
	sudo systemctl stop forexwebapp.service
	sudo systemctl disable forexwebapp.service

remove-service:
	sudo rm -rf /etc/systemd/system/forexwebapp.service

clean:
	rm -rf .venv
	find . -type d -name '__pycache__' -exec rm -r {} +