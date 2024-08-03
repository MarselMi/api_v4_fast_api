up:
	docker compose -f docker-compose-test.yaml up -d
refresh:
	docker compose -f docker-compose-test.yaml down && docker network prune --force && docker compose -f docker-compose-test.yaml up -d
down:
	docker compose -f docker-compose-test.yaml down && docker network prune --force