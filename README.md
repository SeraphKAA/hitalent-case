# hitalent-case
Тестовое задание от компании "hitalent"

## Установка

### Первый этап

Клонирование репозитория и .env файла
```
git clone git@github.com:SeraphKAA/hitalent-case.git
cd hitalent-case
cp .env.example .env
```

По желанию можете дополнительно настроить .env файл.

### Второй этап (запуск)

Запустить можно либо через команду makefile либо следующим образом
```
docker compose up --build
```

## Использование

Сайт доступен по протоколу HTTP. 
Swagger сервера доступен по порту 8000 на эндпоинте /api/docs.
Redoc сервера доступен по порту 8000 на эндпоинте /api/redoc.

## Дополнительно

Команды Makefile:
- Cтарт проекта
```
make start
```

- Билд проекта
```
make build
```

- Удаление контроллеров и зависимостей
```
make down
```


Можно было конечно сделать проверки на sql инъекции и подобного (самый простой "'; DROP DATABASE ...; --"), но решил не делать
Если нужно сделать, то на уровне dto классов бы сделал или на уровне контроллеров

## Результат

Все существующие эндпоинты:
![ImageAlt](https://github.com/SeraphKAA/hitalent-case/blob/main/photoes/image_endpoints.png)

Тесты:
![ImageAlt](https://github.com/SeraphKAA/hitalent-case/blob/main/photoes/image_tests.png)
Кроме обычных тестов также сделал негативные, чтобы проверить на заголовок <=200 и сообщение  <= 5000


Изображение когда делал миграции:
![ImageAlt](https://github.com/SeraphKAA/hitalent-case/blob/main/photoes/image_from_migrations.png)
