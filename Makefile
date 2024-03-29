.PHONY: start stop restart

start:
	docker-compose build
	docker-compose up -d

stop:
	docker-compose down

restart:
	docker-compose down
	docker-compose build
	docker-compose up -d
