.PHONY: fcls clean build up 

.PHONY: clean
clean:
	docker system prune -f

.PHONY: down
down:
	docker-compose down

.PHONY: up
up:
	docker-compose up -d

.PHONY: build
build:
	docker-compose build --no-cache

.PHONY: restart
restart: down
	docker-compose up -d --build --force-recreate

.PHONY: fcls
fcls:
	sudo rm -rf pizza/localstack-data/*

