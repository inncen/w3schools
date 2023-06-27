# w3schools

## Running tests locally

1. Install [python](https://www.python.org/downloads/release/python-390/) if necessary
2. Create and activate [virtualenv](https://docs.python.org/3/library/venv.html)
3. Install dependencies:
```shell
pip install -r requirements.txt
```
4. Run tests:
```shell
python -m pytest --gui
```


## Running tests in docker

1. Install [docker](https://docs.docker.com/engine/install/ubuntu/) if necessary
2. Build image:
```shell
docker build -t seleniumbase .
```
3. Run docker container:
```
docker run seleniumbase
```