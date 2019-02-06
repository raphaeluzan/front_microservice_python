# front_microservice_python


## Cloner le projet

```
git clone https://github.com/raphaeluzan/front_microservice_python
```

## Dockerisation

Construction de l'image Docker à partir du Dockerfile :
```
docker build -t my_docker_flask:latest .

```

Lancement de notre image (i.e. de l'application) dans un conteneur :
```
docker run -d -p 5000:5000 my_docker_flask:latest
```
Pour information notre docker se lance sur l'IP 192.168.99.100.



