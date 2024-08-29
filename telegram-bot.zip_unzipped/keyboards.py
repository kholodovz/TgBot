from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

# Пакеты разработки
packages = {
    "Базовый (1-2 функции)": {"price": 5000, "description": "Основные функции, такие как приветствие и команды."},
    "Стандартный (3-5 функций)": {"price": 10000, "description": "Базовые функции плюс интеграция с API и уведомления."},
    "Расширенный (6-8 функций)": {"price": 15000, "description": "Все функции стандартного пакета плюс работа с базой данных и аналитика."},
    "Премиум (9-12 функций)": {"price": 20000, "description": "Расширенный пакет плюс многоязычная поддержка и интеграция с соцсетями."},
    "Максимум (13+ функций)": {"price": 30000, "description": "Все функции предыдущих пакетов плюс машинное обучение и AI."},
}

# Генерация клавиатуры с пакетами
def get_package_markup():
    markup = InlineKeyboardMarkup()
    for idx, (package, details) in enumerate(packages.items(), start=1):
        markup.add(InlineKeyboardButton(f"{idx}. {package} (${details['price']})", callback_data=str(idx)))
    markup.add(InlineKeyboardButton('Завершить выбор', callback_data='finish'))
    return markup

# Генерация основного меню
def get_main_menu_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(InlineKeyboardButton('Выбрать пакет'))
    markup.add(InlineKeyboardButton('Отменить заявку'))
    return markup
