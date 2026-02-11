1. Меняем /home/persay/app/db/session.py

2. Ставим драйвер psycopg2
```
apt update
apt install -y python3-dev build-essential libpq-dev python3-wheel
/home/persay/venv/bin/pip install --upgrade pip
/home/persay/venv/bin/pip install wheel setuptools
/home/persay/venv/bin/pip install psycopg2-binary
```

3. Поднимаем PostgreSQL
```
sudo apt install postgresql
sudo -u postgres psql
```
```sql
CREATE DATABASE persaydb;
CREATE USER user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE persaydb TO user;
```
где persaydb - имя базы; user, password -имя и пароль пользователя PostgreSQL

В веб-интерфейсе PERSAY прописываем путь к БД:
```db.url
postgresql+psycopg2://user:password@localhost:5432/persaydb
```
