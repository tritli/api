[![stability][0]][1] [![Python 3.6][2]][3] [![PyOTA 2.1.0][4]][5] [![build docker][6]][7] 

![amazing trit.li banner](docs/images/logo.png?style=centerme)

# 1. Introduction
Trit.li is a distributed URL shortener service using the IOTA tangle.
It addresses the following main weaknesses of a classical, centralized URL shortener:
* Censorship and possible deactivation of links
* Chaining of links, resulting in longer response times
* Traceability of the user

The name trit.li is derived from two facts:
* The name of a very common centralized URL shortener service 
* Trit.li is based on IOTA, which uses the trinary not the binary system (trit vs. bit)


# 2. API - The backend
The trit.li API generates a random short URL and stores it with the 
respective long URL and optional meta data on the tangle. 
Through the API, the long URL can be retrieved from the generated short URL.

More specific, the trit.li API has the following basic functions:
1. Storing the long URL on the tangle and retrieving a short URL
2. Retrieving the long URL and metadata information from the tangle by using the short URL
3. Redirect short URL to long URL
4. Validation of the combination of short and long URL
5. Exploration of the last requested short URLs using the default tag 

The API uses flask/flask-restplus, which comes with swagger support. 
You can use the [swagger online editor][swagger] to generate an API client in your favorite programming language.


# 3. How does it work?
## 3.1 Short URL from Long URL
The API retrieves the http request with the long URL to be shortened.
A random string is generated (length and the characters can be defined in the config).
By default the random string consists of A-Z a-z 0-9 and - to a length of 7 characters.
The random string is converted to an IOTA compatible address.
After the check if that address exists, a transaction is send to the generated address.

The transaction contains the following information:
* long URL
* short URL
* a defined tag
* customizable meta data
* time stamp
* a hash for validation purposes

![storing the URL on the tangle][sfl]

## 3.2 Long URL from Short URL
It is basically the same with less steps. The API retrieves the http request with the short URL (the random string).
The random string is converted to an IOTA compatible address.
All transactions to that address are retrieved and validated with the default or custom salt. 
If a transaction turns out to be valid the long URL will be returned from the tangle.

![receiving the URL from the tangle][lfs]


# 4. Validation
For validation purposes, by default an sha256 hash is generated over the entire signature message (JSON object) including a salt.
If not specified, a default salt is used by trit.li (can be defined in the config file).
Is the default salt is used, the validation can only be executed through the official trit.li API. 
However, if a custom salt was used, when requesting a short URL, this specific salt will be required for the validation.


# 5. Run the API
## In Python 3
For production purposes it is recommended to use an appropriate wsgi web server.
The current state of the project is not production ready anyways.
To start the API using python, follow the following steps.

1. change to the `./src` directory
    > `cd ./src`
2. Install requirements (best is to use a python virtual environment)
    > `pip3 install -r requirements.txt`
3. Configuration of the API
    > see src/config/config.py
4. Run with the following command
    > `python3 wsgi.py`

## In Docker
As mentioned before the current state of the project is not production ready.
The docker image uses nginx and uwsgi as web server and supervisor as process manager. 
The config files can be found under the `./docker` directory.

1. Build a local docker container 
    > `docker build -t tritliapi .`
2. Run the container (you can assign more cores using --cpuset-cpus="0-n")
    > `docker run -it -p 80:80 tritliapi`


# Your Support
1. Give [feedback] or [participate]
2. Feel free to donate iota to the following IOTA address
    > JYHJOCIFXWGWCAWYAHHPOPCELIGDTGSCLVRAQRZJY9BUTIGVLXACEBOLMPRRMNLZDMIBLPETDWJVZASEXJJUPTVJMC
3. Use the API to donate (API running under localhost/docker and deep links need to be activated in your trinity wallet). 
   * click on [donate]
   * this is no automated payment, it still needs to be confirmed in the wallet

[0]: https://img.shields.io/badge/stability-experimental-orange.svg?style=flat-square
[1]: https://nodejs.org/api/documentation.html#documentation_stability_index
[2]: https://img.shields.io/badge/python-3.6-blue.svg?style=flat-square
[3]: https://www.python.org/downloads/release/python-360
[4]: https://img.shields.io/badge/PyOTA-2.1.0-blue.svg?style=flat-square
[5]: https://pyota.readthedocs.io/en/latest/
[6]: https://img.shields.io/badge/build-docker-green.svg?style=flat-square
[7]: https://www.docker.com/

[logo]: docs/images/logo.png "Trit.li Logo"
[swagger]: https://editor.swagger.io/ "Swagger Online Editor"
[sfl]: docs/images/api_sfl.png "Retrieving the short URL to a long URL - Storing the URL on the tangle"
[lfs]: docs/images/api_lfs.png "Retrieving the long URL to a short URL - Retrieving the URL from the tangle"
[feedback]: mailto:feedback@trit.li
[participate]: mailto:admin@trit.li
[donate]: http://localhost/donate
