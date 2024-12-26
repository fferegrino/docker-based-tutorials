## Manual mode

### Create a network


```bash
docker network create todo-network
```

`docker network create`: Creates an isolated network for our containers to communicate among them.

### Run a MySQL container

```bash
docker run \
  --name todo-db \
  --network todo-network \
  -v todo-db-data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=example \
  -e MYSQL_DATABASE=todos \
  -p 3306:3306 \
  mysql:8.0
```

### Setup the database

#### Build the setup-db container

```bash
docker build \
  -f ./setup-db/Dockerfile \
  -t setup-db \
  .
```

#### Run the setup-db container

```bash
docker run \
  --network todo-network \
  --name setup-db \
  setup-db
```

After the container is running, you can check if the database is ready.

### Setup our FastAPI app

#### Build the web-api container

```bash
docker build \
  -f ./web-api/Dockerfile \
  -t web-api \
  .
```

#### Run the web-api container

```bash
docker run \
  --network todo-network \
  --name web-api \
  -p 8000:8000 \
  web-api
```

### Creating a ToDo

```bash
curl -X POST http://localhost:8000/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries"}'
```

### Cleanup

```bash
docker rm -f web-api todo-db setup-db
docker volume rm todo-db-data
docker network rm todo-network
```

### Troubleshooting

Conflict. The container name "/[SERVICE_NAME]" is already in use by container "XXXXXX". You have to remove (or rename) that container to be able to reuse that name.

```bash
docker rm -f [SERVICE_NAME]
```

## Docker Compose mode

```bash
docker compose up
```

### Cleanup

```bash
docker compose down -v
```
