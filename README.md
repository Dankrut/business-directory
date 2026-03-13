# Инструкция по запуску

# 1. Собрать образ приложения
```docker build -t guide_app .```

# 2. Создать сеть
```docker network create myNetwork```

# 3. Создать volume для данных БД
```docker volume create pg-guide-data```

# 4. Запустить PostgreSQL
```
docker run --name guide_db \
    -p 6432:5432 \
    -e POSTGRES_USER=user \
    -e POSTGRES_PASSWORD=user123 \
    -e POSTGRES_DB=guide \
    --network=myNetwork \
    --volume pg-guide-data:/var/lib/postgresql/data \
    -d postgres:16 
```

# 5. Создать тестовую БД
```docker exec -it guide_db psql -U user -d guide -c "CREATE DATABASE test;"```

# 6. Запустить приложение
```
docker run --name guide_back \
    -p 7777:8000 \
    --network=myNetwork \
    -e MODE=LOCAL \
    -e DB_USER=user \
    -e DB_PASS=user123 \
    -e DB_HOST=guide_db \
    -e DB_PORT=5432 \
    -e DB_NAME=guide \
    -e API_KEY=static_key \
    -d guide_app 
```

# 7. Проверить логи (дождаться запуска)
```docker logs -f guide_back```

# Проверка работоспособности:

Документация API:
    ```
    - Swagger UI: http://localhost:7777/docs
    - ReDoc: http://localhost:7777/redoc
    ```

```X-API-Key: static_key```

# Через команду curl в терминале:

Список зданий:
```curl -X GET "http://localhost:7777/buildings" -H "X-API-Key: static_key"```

Дерево деятельности:
```curl -X GET "http://localhost:7777/activities/tree" -H "X-API-Key: static_key"```

Информация об организации:
```curl -X GET "http://localhost:7777/organizations/1" -H "X-API-Key: static_key"```

Поиск по названию:
```curl -X GET "http://localhost:7777/organizations/search/name?name=%D0%90%D0%B2%D1%82%D0%BE%D0%9C%D0%B8%D1%80" -H "X-API-Key: static_key"```

Поиск в радиусе:
```curl -X GET "http://localhost:7777/organizations/nearby?lat=55.7558&lng=37.6176&radius=1000" -H "X-API-Key: static_key"```

# Запуск тестов:

Зайти в контейнер с приложением:
```docker exec -it guide_back bash```

Внутри контейнера запустить тесты:
```MODE=TEST pytest tests/ -v```

Выйти:
```exit```