import asyncio
import random
from data_loader import load_data
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from time import sleep

""" data loading; configurations; main_functions initialization """
data = asyncio.run(load_data())
if not data:
    print("Остановка бота")
    exit()

TOKEN = "8026787503:AAELtcIvwOwGnasgT-NQP03Y-60GmldUPe8"

dp = Dispatcher()
""""""

""" classes and functions """
class UserStates(StatesGroup):
    waiting_for_answer = State()
    waiting_for_question = State()

async def get_random_question():
    return random.choice(data)
""""""

""" keyboards """
main_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="Помощь"), types.KeyboardButton(text="Рулетка вопросов")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

stop_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[[types.KeyboardButton(text="Отмена")]],
    resize_keyboard=True,
    one_time_keyboard=True
)
""""""

""" start command """
@dp.message(Command("start"))
async def cmd_start_with_keyboard(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Выберите действие:",
        reply_markup=main_keyboard
    )
""""""

""" help requests module """
@dp.message(F.text == "Помощь")
async def handle_help_button(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Напишите свой вопрос в поддержку:", reply_markup=stop_keyboard)
    await state.set_state(UserStates.waiting_for_question)
    await state.update_data(question_processing=False)


@dp.message(UserStates.waiting_for_question)
async def get_question(message: types.Message, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    if user_data.get('question_processing'):
        return
    await state.update_data(question_processing=True)

    if message.text == "Отмена":
        await state.clear()
        await message.answer("Вы отменили свой вопрос", reply_markup=main_keyboard)
    else:
        admin_id = 1883711626
        await bot.send_message(chat_id=admin_id, text=f"Вам вопрос от {message.from_user.username}:\n{message.text}")
        await message.answer("Ваш вопрос отправлен админу", reply_markup=main_keyboard)
        await state.clear()
""""""

""" roulette of questions module """
@dp.message(F.text == "Рулетка вопросов")
async def handle_random_questions_button(message: types.Message, state: FSMContext):
    question = await get_random_question()
    await message.answer(question['task_text'], reply_markup=stop_keyboard)
    await state.set_state(UserStates.waiting_for_answer)
    await state.update_data(question=question)
    await state.update_data(question_processing=False)


@dp.message(UserStates.waiting_for_answer)
async def check_answer(message: types.Message, state:FSMContext):
    user_data = await state.get_data()
    if user_data.get('question_processing'):
        return
    await state.update_data(question_processing=True)

    if message.text == "Отмена":
        await state.clear()
        await message.answer("Вы завершили серию вопросов", reply_markup=main_keyboard)
    else:
        state_data = await state.get_data()
        question = state_data['question']
        user_answer = set([i for i in message.text.strip().lower()])
        correct_answer = set([i for i in question['answer']])

        if user_answer == correct_answer: await message.answer("Верно!", reply_markup=stop_keyboard)
        else: await message.answer(f"Правильный ответ: {question['answer']}", reply_markup=stop_keyboard)

        await handle_random_questions_button(message, state)
""""""


""" run the bot """
async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
""""""