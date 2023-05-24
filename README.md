# beauty-city-web


## Local environment setup:

1. Setup virtual environment

```shell
python -m venv venv
```

then activate it:

```shell
. ./venv/bin/activate
```

```cmd
venv\Scripts\activate.bat
```


2. Install requirements


```shell
pip install -r requirements.txt
```

3. Create .env file in project root directory and fill it with your settings

```shell
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=
DATABASE_URL=sqlite:///db.sqlite3
```

4. Run migrations

```shell
python manage.py migrate
```

5. Create superuser

```shell

python manage.py createsuperuser
```

6. (optional) Load fixtures

```shell
python manage.py loaddata sample
```

7. Run server

```shell
python manage.py runserver
```

8. Open in browser

localhost:8000


9. Open admin panel

localhost:8000/admin


## Deploy

