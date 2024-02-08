1. Build container

```shell
docker build -t pdf2dom:latest .
```

2. Run container

```shell
docker run -it -v %cd%:/app pdf2dom:tag /bin/bash
```

3. run scripts

```shell
java -jar pdf2dom.jar input.pdf output.html
```