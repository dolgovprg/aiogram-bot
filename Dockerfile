FROM python:3.11.5-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR ~/aiogram-bot

COPY requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt

COPY aiogram_bot ./aiogram_bot

CMD ["python", "-m", "/src/app.py"]

# -------------------------------
# Build an image from a Dockerfile:
# $ docker build -t aiogram_bot .
# -------------------------------
# Create and run a new container from an image:
# $ docker run -d --name aiogram-bot \
#    --env "BOT_TOKEN=<BOT_TOKEN>" \
#    --env "AI_KEY=<AI_KEY>" \
#    --env "ADMINS=<ADMINS>" \
#    aiogram_bot
# -------------------------------
# Stop running container:
# $ docker stop aiogram-bot
# -------------------------------
# Start stopped container:
# $ docker start aiogram-bot
# -------------------------------
# Remove container:
# $ docker rm aiogram-bot
# -------------------------------
# Remove image:
# $ docker rmi aiogram_bot
# -------------------------------
# Execute a command in a running container:
# $ docker exec -it aiogram-bot bash
