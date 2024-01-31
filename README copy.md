# aiogram-bot - telegram-bot (Python, [aiogram](https://aiogram.dev/))

### Запуск в Докере

Создать и запустить контейнер:

```bash
$ export BOT_TOKEN=<BOT_TOKEN>
$ export AI_KEY=<AI_KEY>
$ docker-compose up -d
```

Остановить запущенный контейнер:

```bash
$ docker-compose stop
```

Запустить остановленный контейнер:

```bash
$ docker-compose start
```

Остановить и удалить контейнер и сеть:

```bash
$ docker-compose down
```

Удалить докер-образ:

```bash
$ docker rmi aiogram_bot
```

Очистить логи:

```bash
$ sudo rm -rf logs/*
```

### [Пустой шаблон для деплоя](https://railway.app/template/-S3lVz?referralCode=jUyx2Z)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/-S3lVz?referralCode=jUyx2Z)

#### Переменные

- `BOT_TOKEN` - токен Telegram-бота
- `CHAT_ID` - ID чата, в котором разрешено работать боту.
- `AI_KEY` - OpenAI API токен
- `DOMAIN` - URL-адрес с названием приложения. После развертывания перейдите в настройки проекта (`Settings`) и скопируйте домен из раздела `Domains`. Это должно быть похоже на `worker-production-XXXX.up.railway.app`. Это и будет значение для переменной `DOMAIN`.
