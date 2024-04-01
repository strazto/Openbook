# Openbook

Openbook is a website currently under development which will feature as a blog and note taking website.
In addition to this it will feature a database for Movies, Games and Books.

It uses Python-Flask's tutorial [Flaskr](https://flask.palletsprojects.com/en/3.0.x/tutorial/) as a starting point.

## Create a Python Virtual Environment

```
python3 -m venv .venv
```

## Activate the Python Virtual Environment

```
$ . .venv/bin/activate
```
## Install Flask

```
$ pip install Flask
```
## Initialise the Database 

```
$ flask --app openbook init-db
```
## Run the App

```
$ flask --app openbook run --debug
```
