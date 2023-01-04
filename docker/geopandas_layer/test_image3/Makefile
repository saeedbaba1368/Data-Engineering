docker-build:
	sudo docker build -t name:LambdaLayer .

docker-copy:
	$(eval id=$(shell docker create name:LambdaLayer)) 
	sudo docker cp $(id):/opt/app/lib .
	sudo docker rm -v $(id)

docker-zip:
	zip -r lambda_layer.zip lib