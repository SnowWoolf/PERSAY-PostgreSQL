### Строка 34:
```
from app.db.session import init_db
```
меняем на
```
from app.db.session import init_db, init_engine
```

### Строка 175:
```
settings.load_yaml_config()
```
добавляем строку:
```
settings.load_yaml_config()
init_engine()
```
