# Introduction
The idea behind trit.li is a distributed URL shortener service based on the IOTA tangle.
It addresses the following main weaknesses of a classical, centralized URL shortener:
* Censorship and possible deactivation of links
* Chaining of links, resulting in longer response times
* Traceability of the user
The name trit.li is based on the name of a very common centralized URL shortener service.
As IOTA is not based on the binary, but trinary system, so it is called trit.li.

# API - The backend
The trit.li API generates a short URL and stores it with the 
respective long URL and optional meta data on the tangle. 
By calling the short URL, trit.li will retrieve the long URL 
from the tangle and then redirect you to the original web site.

The trit.li API has the following basic functions:
1. Storing the long URL on the tangle and retrieving a short URL
2. Retrieving the long URL and metadata information from the tangle
3. Redirect short URL to long URL
4. Validation of the combination of short and long URL

# Storing and Retrieving the data
The information for a short URL is stored as a JSON object in a transaction.
To find this transaction, the short URL is decoded in the receiving address.
![storing the URL on the tangle][sfl]

# Validation
For validation purposes, by default a hash is generated over the entire 
JSON object including a salt, which is only known by trit.li. 
Therefore (by default) the validation can only be executed through 
the official trit.li website/API. However it is possible to define the salt,
when requesting a short URL. For a later validation, this specific salt will
be required.

# Docker
1. Build local docker container 
    > `docker build -t tritliapi .`
2. Run to test 
    > `docker run -it -p 80:80 tritliapi`
    

* For uploading to azure cloud 
  1. `docker tag tritliapi tritliapi.azurecr.io/tritliapi`
  2. `docker push tritliapi.azurecr.io/tritliapi`

[sfl]: docs/images/20190723_api_sfl.png "Storing the URL on the tangle"
