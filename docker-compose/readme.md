## Manual mode

### Create a network

```bash
docker network create docker-compose-network
```

### Run a MySQL container

```bash
docker run \
  --network docker-compose-network \
  --name mysql \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=db \
  -v mysql_data:/var/lib/mysql \
  -p 3306:3306 \
  mysql:8.0
```

### Setup the database

#### Build the setup-db container

```bash
docker build -t setup-db ./setup-db
```

#### Run the setup-db container

```bash
docker run \
  --network docker-compose-network \
  --name setup-db \
  -e MYSQL_HOST=mysql \
  -e MYSQL_USER=root \
  -e MYSQL_PASSWORD=root \
  -e MYSQL_DATABASE=db \
  setup-db
```

After the container is running, you can check if the database is ready.

### Setup our FastAPI app

#### Build the web-api container

```bash
docker build -t web-api ./web-api
```

#### Run the web-api container

```bash
docker run \
  --network docker-compose-network \
  --name web-api \
  -e MYSQL_HOST=mysql \
  -e MYSQL_USER=root \
  -e MYSQL_PASSWORD=root \
  -e MYSQL_DATABASE=db \
  -p 8080:8080 \
  web-api
```

### Cleanup

```bash
docker rm -f setup-db
docker rm -f mysql
docker rm -f web-api
docker volume rm mysql_data
docker network rm docker-compose-network
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
