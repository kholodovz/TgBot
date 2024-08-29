from aiogram.dispatcher.filters.state import State, StatesGroup

# Определение состояний
class Form(StatesGroup):
    package_selection = State()
    additional_cost = State()
    confirmation = State()
