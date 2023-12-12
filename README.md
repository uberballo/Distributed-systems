# Distributed-systems

## How to run
Start the service by running:
`make up`

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
- [ ] When new node joins or disconnects main node must ask every node to find out round trip times to all the other nodes an return it to main node. Based on RRTs between all nodes, main node should calculate minimum spanning tree to find out which nodes should communicate to each others to avoid unnecessary traffic.
- [ ] Get rid of main node, make chat nodes discover each others by broadcasting or multicasting and add leader election


### Missing features

- Minimize overhead when sending messages
- Send all messages including history when forwarding to new nodes
- Reduce client overhead when polling for new messages

## Development

_Makefile assumes you have python3.12 installed. To change this behaviour run `make <target> PYTHON=pythonX.Y`_

### Setup dev environment

`make init-dev-env`

For activating virtual dev environment: `. .venv/bin/activate`

### Linting, formatting, type checking, import sorting

`make check` - for checking everything

Available targets: `check-format`, `check-imports`,`check-lint`, `check-types`, `format`, `sort-imports`

### Docker compose with reload

`make dev-up`
