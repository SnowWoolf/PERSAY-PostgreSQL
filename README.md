### 1. Меняем файлы из репозитория:
/home/persay/app/db/session.py

/home/persay/app/main.py


### 2. Ставим драйвер psycopg2:
```
apt update
apt install -y python3-dev build-essential libpq-dev python3-wheel
/home/persay/venv/bin/pip install --upgrade pip
/home/persay/venv/bin/pip install wheel setuptools
/home/persay/venv/bin/pip install psycopg2-binary
```


### 3. Поднимаем PostgreSQL:
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


### 4. Перезапускаем сервис
```
systemctl restart persay
```


### 5. В веб-интерфейсе PERSAY прописываем путь к БД:
```db.url
postgresql+psycopg2://user:password@localhost:5432/persaydb
```
и перезапускаем сервис (можно кнопкой в веб-интерфейсе)


### 6. Настраиваем внешний доступ к БД:
   
Разрешаем PostgreSQL слушать сеть
```
sudo nano /etc/postgresql/*/main/postgresql.conf
```
меняем:
```
listen_addresses = 'localhost'
```
   на
```
   listen_addresses = '*'
```
где * можно заменить на конкретный ip адрес, которому разрешен доступ к БД


Затем разрешаем доступ пользователю по сети
```
sudo nano /etc/postgresql/*/main/pg_hba.conf
```
в самый конец добавляем строку:
```
host all all 0.0.0.0/0 md5
```
или более безопасно:
```
host    persaydb    user    192.168.1.0/24    md5
```

Перезапускаем PostgreSQL
```
sudo systemctl restart postgresql
```

И подключаемся с другого ПК через pgAdmin.

### Узнать размер БД через pgAdmin:

В консоли PSQL Tool Workspace подключиться к БД и выполнить команду
```
SELECT pg_size_pretty(pg_database_size(current_database()));
``` 
