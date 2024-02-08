# parse pdf

1. build container

```shell
docker build -t pdf-to-html .
```

2. mount volume 

```shell
docker run -it --rm -v "%cd%:/app" -w /app pdf-to-html
```

3. run script

```shell
python script.py input.pdf output.html
```