# backend
This will be the trit.li backend API using swagger.

# Docker
* Build local docker container 
  * `docker build -t tritliapi .`
* Run to test 
  * `docker run -it -p 80:80 tritliapi`
* For uploading to azure cloud 
  1. `docker tag tritliapi tritliapi.azurecr.io/tritliapi`
  2. `docker push tritliapi.azurecr.io/tritliapi`
