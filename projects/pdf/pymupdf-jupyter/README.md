1. build
```shell
docker build -t pdf-to-html .
```

2. run
```shell
docker run -it --rm -p 8080:8080 -v "%cd%:/app" pdf-to-html
```

3. Open a new terminal or command prompt window on your host machine and start a Chrome browser:

```shell
chrome http://localhost:8080/lab
```

4. In the first terminal or command prompt window where the Docker container is running, enter the container:

```shell
docker exec -it <container_id> /bin/bash
```

5. Inside the container, start JupyterLab:

```shell
jupyter lab --ip=0.0.0.0 --port=8080 --no-browser --allow-root
```