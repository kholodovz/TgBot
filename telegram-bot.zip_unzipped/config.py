from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Конфигурация
TOKEN = "7069065610:AAFvnG9_vASfONaavZxuMUSaQGVYiTSwNVA"
ADMIN_ID = 1384356846

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
