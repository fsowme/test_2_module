# test_2_module

## Запуск приложения

### 1. Настройка окружения
```shell
cp .env_example .env
```

### 2. Настройка топиков
```shell
chmod +x ./init.sh && ./init.sh
```

### 3. Запуск кластера Kafka и приложения
```shell
docker compose up
```

## Запуск тестов
### 1. Поднятие консьюмера
```shell
python clients/consumer.py
```

### 2. Запуск тестов
```shell
python clients/test.py --ban --censorship

# --ban отправит сообщение в топик 'bans', а агент добавит в таблицу 'bans' информацию о бане (ключ - имя получателя
# ('User1'), значение - список имен (['BadUser']), заблокированных отправителей). Затем выполняется отправка двух
# сообщений пользователю 'User1', одно от 'User2', второе от BadUser. Consumer должен получить только одно сообщение
# от пользователя 'User2', а в логе faust (docker logs app) должно появиться сообщение 'Sender BadUser banned by User1'

# --censorship отправит сообщение в топик 'obscene-words', а агент добавит в таблицу 'obscene_words' запись о
# цензурируемом слове ('bad') (ключ - само слово, значение - true). Затем выполняется отправка сообщения с этим словом.
# Consumer должен получить сообщение с таким текстом 'Hello world! <CENSORED>. Tssss...'
```

### 3. Ручные тесты
```shell
python clients/producer.py

# добавление бана
python clients/producer.py ban --blocker "User" --banned "Spammer"

#  отправка сообщения
python clients/producer.py message --sender "User10" --recipient "User5" "Hello World!"

# Добавление цензурируемого слова
python clients/producer.py obscene_words "bad_word"
```
