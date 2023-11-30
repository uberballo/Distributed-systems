# Distributed-systems

## How to run
Start the service by running:
```
    docker compose up
```

## "Kanban"

TODO:
- [ ] Send messages to a chat node
- [ ] Get messages from a chat node
- [x] Get neighbors from the main node
- [x] Implement proper initialization to a chat node
    - Easy to do with fastapi `@app.on_event("startup")`
    - More difficult is reinitialization after node you are connected to disconnects while serving client
- [x] Ping main node when a new chat nodes joins
- [x] Add health checker to main node
- [ ] Create a client that communicates with a chat node

## Dev environment

### Setup

```
python3.12 -m venv --clear .venv
source .venv/bin/activate
pip install --editable main_node[dev] --editable chat_node[dev] --editable client[dev]
```

### Linting, formatting, type checking, import sorting

After activating the environment and installing applications and dependencies: `make check`
