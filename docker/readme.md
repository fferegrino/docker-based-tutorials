## Demo 1

```bash
docker run hello-world
```

It may look like a simple thing, but it's actually a very powerful tool. Let me try to explain what is going on.

### Creating our own hello-world image

```bash
cd hello-world
docker build -t hola-mundo .
docker run hola-mundo
```

What happened here?

#### What is a Dockerfile?

A Dockerfile is a text file that contains a set of instructions for Docker to build an image.

#### What is an image?

An image is a read-only template with instructions for creating a Docker container.

#### What is a container?

A container is a runnable instance of an image.

## Demo 2

### Creating our own hola-pokemon image

```bash
cd hola-pokemon
docker build -t hola-pokemon .
docker run hola-pokemon
```

#### What is the Docker context?

The Docker context is the directory that contains the Dockerfile and the files that are needed to build the image.

### Changing the context

```bash
cd ..
docker build -t hola-pokemon .
```

This will fail because the Dockerfile, and all the files that are needed to build the image, are in the hola-pokemon directory.

To fix this, we can change the context to the hola-pokemon directory.

```bash
docker build -t pokemon ./hola-pokemon
docker run pokemon
```

### Caching layers

To speed up the build process, Docker caches the layers of the image, that is why you see the `CACHED` message. If you change the Dockerfile or the files that are needed to build the image, Docker will not use the cached layer and will build the image from scratch.

You can force Docker to use the cached layer by using the `--no-cache` flag.

## Demo 3: Creating a ToDo app

```bash
cd todo-app
docker build -t todo-app .
docker run todo-app
```

### Running the app

```bash
docker run todo-app
```

Now, you can go to `http://localhost:8000/todos` to see the todos, but...

There is no response! why?

#### Networking

Docker containers are isolated from the host machine and other containers by default. This isolation is achieved through a virtual network interface.

To access the app, we need to map the container's port to the host machine's port.

```bash
docker run -p 8000:8000 todo-app
```

Now, you can go to `http://localhost:8000/todos` to see the todos. Though there are no todos yet.

### Creating a ToDo

```bash
curl -X POST http://localhost:8000/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries"}'
```

Now if we go to `http://localhost:8000/todos`, we will see the todo.

Now, we can cancel the container run and run it again.

If we go to `http://localhost:8000/todos` again, after restarting the container, we will see that the todo is gone!

This is because the data is stored in the container's filesystem, and when the container is stopped, the data is lost.

To fix this, we need to use a persistent storage.

### Using a persistent storage

We can use a volume to persist the data.

```bash
docker run \
  -p 8000:8000 \
  -v ./todo-data:/data \
  todo-app
```

Now, if we stop and restart the container, the todos will still be there, and the data will be persisted in the `todo-data` directory.

## Demo 4: Creating a ToDo app with a database

```bash
cd todo-app-db
docker build -t todo-app-db .
```

### Creating the network

```bash
docker network create todo-network
```

`docker network create`: Creates an isolated network for our containers to communicate among them.

### Creating the database

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

Command explanation:

   - `--name todo-db`: Names the container
   - `--network todo-network`: Connects it to our network
   - `-v todo-db-data:/var/lib/mysql`: Mounts the `todo-db-data` volume to the container's `/var/lib/mysql` directory
   - `-e MYSQL_ROOT_PASSWORD=example`: Sets the root password
   - `-e MYSQL_DATABASE=todos`: Creates the initial database
   - `-p 3306:3306`: Maps the container's port 3306 to the host machine's port 3306
   - `mysql:8.0`: The image to use

```bash
docker run \
  --network todo-network \
  -p 8000:8000 \
  todo-app-db
```

```bash
docker stop todo-api todo-db
docker rm todo-api todo-db
docker volume rm todo-db-data
docker network rm todo-network
```
