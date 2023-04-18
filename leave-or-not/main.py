from aiogram import Bot, executor, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound
from aiogram.dispatcher import FSMContext
import asyncio
from loguru import logger

import os
from contextlib import suppress

import database
from config import States, TOKEN, add_user_action, create_notify


CURRENT_SKILL_ID = None

bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

os.makedirs("logs/", exist_ok=True)
logger.remove()
logger.add("logs/info.log", format="{time} {level} {message}", level="INFO", rotation="10 MB", compression="zip", mode="w")



@dp.message_handler(commands='start')
async def run_bot(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Готов')
    
    # Запускаем вспомогательный метод, с которого всё начнется 
    await States.start_question.set()  # Показываем следующий вопрос
    await message.answer('Для начала напишите мне - готов', reply_markup=markup)
    logger.info(f"{message.from_user.username, message.from_user.full_name, message.from_user.id} Начал работу с ботом", )


@dp.message_handler(state=States.start_question)
async def start(message: types.Message):
    """Вспомогательный метод для запуска первого вопроса. Без этого метода, дублируются первые два вопросы и сбивается весь порядок ответов
    Поэтому был написан этот метод, как отправная точка и добавлена переменная CURRENT_QUESTION_ID"""

    global CURRENT_SKILL_ID
    if message.text.lower() != "готов":
        asyncio.create_task(input_invalid(message))
        logger.info("Неправильный ответ на вопрос '%s'", message.text)
        return

    skill = await database.get_skill_from_database()
    if not skill:
        logger.warning("Закончились вопросы")
        await message.answer("Все вопросы закончились! Спасибо", reply_markup=types.ReplyKeyboardRemove())
        quit()
    CURRENT_SKILL_ID = skill.iD # Меняем значение нашей переменной, тем самым указывая корректный айди вопроса, который нужно обработать
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Нет', 'Да')
    _, remains = await database.show_the_rest()
    await message.answer(f"Оставить навык?\n- {skill.title}\nОсталось:{remains}", reply_markup=markup)
    await States.question.set()

# Переключение между вопросами 
@dp.message_handler(state=States.question)
async def show_question(message: types.Message, state: FSMContext):
    """
    Основной метод, который будет обрабатывать ответы пользователя и изменять значения в БД
    """
    global CURRENT_SKILL_ID
    if message.text.lower() not in {"да", "назад", "нет"}:
        asyncio.create_task(input_invalid(message))
        return
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Нет', 'Назад', 'Да')
    if message.text.lower().strip() == 'назад':
        add_user_action(actionName="cancel", message=message)
        previos_skill = await database.get_previos_skill(CURRENT_SKILL_ID)
        if previos_skill:
            await States.question.set()
            _, remains = await database.show_the_rest()
            await message.answer(f"Оставить навык?\n- {previos_skill.title}\nОсталось:{remains}", reply_markup=markup)
            CURRENT_SKILL_ID = previos_skill.iD

        else:
            await message.answer("Ранее вы еще не отвечали на вопросы!")
    else:
        # Меняем значения в БД
        if message.text.lower().strip() == 'да':
            add_user_action(actionName="yes", message=message)
            await database.confirm_skill(id=CURRENT_SKILL_ID)
            logger.info("Прошел проверку навык с id: %d", CURRENT_SKILL_ID)
            # logger.warning("Id: %d - Accept", CURRENT_QUESTION_ID)
        elif message.text.lower().strip() == 'нет':
            add_user_action(actionName="no", message=message)
            logger.info("Забраковали навык с id: %d", CURRENT_SKILL_ID)
            await database.confirm_skill(id=CURRENT_SKILL_ID, confirm=False)

        # Получаем новый вопрос
        skill = await database.get_skill_from_database()
        if not skill:
            logger.warning("Закончились вопросы")
            await message.answer("Все вопросы закончились! Спасибо", reply_markup=types.ReplyKeyboardRemove())
            quit()
        CURRENT_SKILL_ID = skill.iD
        print(CURRENT_SKILL_ID)

        # Показываем вопрос пользователю
        await States.question.set() # Показываем следующий вопрос
        _, remains = await database.show_the_rest()
        await message.answer(f"Оставить навык?\n- {skill.title}\nОсталось:{remains}", reply_markup=markup)


# Функция для удаления сообщений
async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


# Обработка исключений
@dp.message_handler(state=States.question)
async def input_invalid(message: types.Message):
    await States.question.set()
    return await message.reply("Неправильный ответ. Используйте клавиатуру или введите ответ самостоятельно")




if __name__ == "__main__":
    create_notify()
    executor.start_polling(dp, skip_updates=True)