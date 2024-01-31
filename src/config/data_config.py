import os

from dotenv import load_dotenv

load_dotenv()

# BOT_TOKEN
BOT_TOKEN = os.getenv('BOT_TOKEN')

# AI
AI_KEY = os.getenv('AI_KEY')
MODEL = 'gpt-3.5-turbo'

ADMINS = os.getenv('ADMINS')
# Словник для зберігання відповідей користувачів
answers = {}

# Список локацій
locations = [f"Локація {i}" for i in range(1, 6)]

# Список питань 
checklist = [
    "1 Опиши що зiбражено на фото",
    "2 Можно ли зробити краще",
    "3 Надай повну вiдповiдь",
    # "Пункт 4",
    # "Пункт 5",
    # Додайте власні пункти 
]