Commands used to run this example
```bash
docker build -t status-server:1.0.0 .
docker run -d -p 8080:8080 --name status status-server
curl localhost:8080
docker ps
docker exec status whoami
docker rm -f status
```
