ifndef workers
override workers = 3
endif

run-scheduler:
	make down && docker compose up redis scheduler

del-redis:
	rm redis_data/dump.rdb || true

prune:
	docker compose down --volumes --rmi="all" && make del-redis

down:
	rm celerybeat-schedule || true && docker compose down

build:
	docker compose build

build-cl:
	make clean && make build

run:
	make down && docker compose up

clean-run:
	(make del-redis || 1) && docker compose down --volumes && make run

build-and-run:
	make build && make run

run-scale:
	make down && docker compose up --scale worker='$(workers)'

build-and-run-scale:
	make down && make build && make run-scale
