PROJECT_NAME = sftp_mysql_indexer
DOCKER_COMPOSE = docker-compose

# Environment
ENV_FILE = .env

# Docker commands
build:
	pip install paramiko mysql-connector-python
	$(DOCKER_COMPOSE) build

up: build
	$(DOCKER_COMPOSE) --env-file $(ENV_FILE) up -d

down:
	$(DOCKER_COMPOSE) down

logs:
	$(DOCKER_COMPOSE) logs -f

run:
	$(DOCKER_COMPOSE) run --rm app

restart: down up

clean:
	$(DOCKER_COMPOSE) down -v

ps:
	$(DOCKER_COMPOSE) ps

mysql:
	docker exec -it $$(docker ps -qf "name=mysql") mysql -uroot -p$$(grep MYSQL_ROOT_PASSWORD $(ENV_FILE) | cut -d '=' -f2) sftp_index

status:
	$(DOCKER_COMPOSE) ps
