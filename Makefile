.PHONY: down image up

down:
	docker compose down

image:
	docker build --tag osiris-78:latest .

up:
	docker compose up --detach
