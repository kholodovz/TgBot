from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

from config import dp, bot, ADMIN_ID
from states import Form
from keyboards import get_package_markup, get_main_menu_markup, packages

# Обработчики команд и состояний
@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer("Здравствуйте! Выберите пакет разработки для вашего проекта.", reply_markup=get_main_menu_markup())

@dp.message_handler(lambda message: message.text == 'Выбрать пакет')
async def select_package(message: types.Message):
    await Form.package_selection.set()
    await message.answer("Выберите пакет разработки:", reply_markup=get_package_markup())

@dp.message_handler(lambda message: message.text == 'Отменить заявку', state='*')
async def cancel_selection(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Процесс подачи заявки отменен.", reply_markup=ReplyKeyboardRemove())

@dp.callback_query_handler(lambda c: c.data.isdigit(), state=Form.package_selection)
async def handle_package_selection(callback_query: types.CallbackQuery, state: FSMContext):
    selected_index = int(callback_query.data) - 1
    selected_package = list(packages.keys())[selected_index]
    package_details = packages[selected_package]
    package_price = package_details["price"]
    package_description = package_details["description"]
    async with state.proxy() as data:
        data['package_price'] = package_price
        data['selected_package'] = selected_package
        data['package_description'] = package_description
    await callback_query.answer()
    await callback_query.message.answer(
        f"Вы выбрали пакет: {selected_package}
"
        f"Описание: {package_description}
"
        f"Стоимость пакета: ${package_price}.",
        reply_markup=ReplyKeyboardRemove()
    )
    await Form.next()
    await callback_query.message.answer("Пожалуйста, введите дополнительные затраты (если есть):")

@dp.message_handler(state=Form.additional_cost)
async def handle_additional_cost(message: types.Message, state: FSMContext):
    try:
        additional_costs = float(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите правильное число для дополнительных затрат.")
        return

    async with state.proxy() as data:
        total_cost = data['package_price'] + additional_costs
        data['total_cost'] = total_cost
        await message.answer(
            f"Выбранный пакет: {data['selected_package']}
"
            f"Описание пакета: {data['package_description']}
"
            f"Стоимость пакета: ${data['package_price']}
"
            f"Дополнительные затраты: ${additional_costs}

"
            f"Общая стоимость: ${total_cost}.

"
            "Если вас устраивает цена, подтвердите, ответив на кнопки ниже.",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton('Да', callback_data='confirm_yes'),
                InlineKeyboardButton('Нет', callback_data='confirm_no')
            )
        )
    await Form.confirmation.set()

@dp.callback_query_handler(lambda c: c.data.startswith('confirm_'), state=Form.confirmation)
async def process_callback_confirm(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    if callback_query.data == 'confirm_yes':
        data = await state.get_data()
        user_info = (
            f"Новая заявка:
"
            f"Пакет: {data['selected_package']}
"
            f"Описание пакета: {data['package_description']}
"
            f"Стоимость пакета: ${data['package_price']}
"
            f"Дополнительные затраты: ${data['additional_cost']}
"
            f"Общая стоимость: ${data['total_cost']}"
        )
        await callback_query.bot.send_message(chat_id=ADMIN_ID, text=user_info)
        await callback_query.message.answer("Ваша заявка принята! Мы свяжемся с вами в ближайшее время.")
    else:
        await callback_query.message.answer("Заявка отменена.")
    await state.finish()
