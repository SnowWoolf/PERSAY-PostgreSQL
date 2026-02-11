1. Меняем /home/persay/app/db/session.py

2. Ставим драйвер psycopg2
'''
apt update
apt install -y python3-dev build-essential libpq-dev python3-wheel
/home/persay/venv/bin/pip install --upgrade pip
/home/persay/venv/bin/pip install wheel setuptools
/home/persay/venv/bin/pip install psycopg2-binary
'''
