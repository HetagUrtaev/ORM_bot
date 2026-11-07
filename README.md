# 1. Создаем общую Docker-сеть
docker network create myNetwork

# 2. Запуск базы данных PostgresSQL 18

# Вариант для Linux / macOS (Bash / Zsh):
docker run --name ORM-db \
    -p 6432:5432 \
    -e POSTGRES_USER=abcde \
    -e POSTGRES_PASSWORD=abcde \
    -e POSTGRES_DB='ORM' \
    --network=myNetwork \
    --volume pg_data:/var/lib/postgresql \
    -d postgres:18

# Вариант для Windows (PowerShell):
docker run --name ORM-db `
    -p 6432:5432 `
    -e POSTGRES_USER=abcde `
    -e POSTGRES_PASSWORD=abcde `
    -e POSTGRES_DB='ORM' `
    --network=myNetwork `
    --volume pg_data:/var/lib/postgresql `
    -d postgres:18


# Запуск приложения через docker-compose
docker compose up --build

# Команда для остановки и удаления контейнера
docker compose down