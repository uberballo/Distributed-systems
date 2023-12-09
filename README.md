# Distributed-systems

## How to run
Start the service by running:
```
    docker compose up
```

## "Kanban"

TODO:
- [x] Send messages to a chat node
- [x] Get messages from a chat node
- [x] Get neighbors from the main node
- [x] Implement proper initialization to a chat node
    - Easy to do with fastapi `@app.on_event("startup")`
    - More difficult is reinitialization after node you are connected to disconnects while serving client
- [x] Ping main node when a new chat nodes joins
- [x] Add health checker to main node
- [ ] Create a client that communicates with a chat node

## Development

_Makefile assumes you have python3.12 installed. To change this behaviour run `make <target> PYTHON=pythonX.Y`_

### Setup dev environment

`make init-dev-env`

For activating virtual dev environment: `. .venv/bin/activate`

### Linting, formatting, type checking, import sorting

`make check` - for checking everything

Available targets: `check-format`, `check-imports`,`check-lint`, `check-types`, `format`, `sort-imports`

### Docker compose with reload

`docker compose -f docker-compose-dev.yml up --build`
