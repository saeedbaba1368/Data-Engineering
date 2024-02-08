1. Build container

```shell
docker build -t pdf2dom:latest .
```

2. Run container

```shell
docker run -it -v %cd%:/app pdf2dom:latest /bin/bash
```

3. run scripts

```shell
cd /app
java -jar pdf2dom.jar input.pdf output.html
```