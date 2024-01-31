import logging
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards.checklist import checklist_keyboard
from keyboards.location import locations_keyboard
from loader import dp
from config.data_config import locations, checklist, answers, AI_KEY, MODEL
from states.checklist import CheckList
import openai

openai.api_key = AI_KEY

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    
    await message.answer(
        "Привіт! Почнемо працювати.", parse_mode=types.ParseMode.MARKDOWN)

    keyboard = locations_keyboard(locations)

    await CheckList.location.set()
    message = await dp.bot.send_message(
        message.chat.id,
        "Оберіть локацію:", 
        parse_mode=types.ParseMode.MARKDOWN, 
        reply_markup=keyboard)
        

@dp.callback_query_handler(state=CheckList.location)
async def set_location(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Функція, вибору локаціі
    """
    
    try:
        await callback_query.answer()
        await state.update_data(location=callback_query.data)
        await CheckList.next()

        chat_id = callback_query.from_user.id

        await dp.bot.send_message(
            chat_id, 
            f"Заповніть чек-лист:")
        
        await CheckList.answers.set()
        
        await ask_question(chat_id, state, answers)

    except Exception as e:
        logging.exception(e)
        return None, 0


@dp.callback_query_handler(state=CheckList.answers)
async def set_checklist(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Функція, яка задає питання і очікує відповіді користувача
    """

    try:
        chat_id = callback_query.from_user.id

        data = await state.get_data()
        answers = data['answers']
        
        question = callback_query.message.html_text.split('\n', 1)[0]

        if question in answers and answers[question] != None: 
             await dp.bot.send_message(
                chat_id, 
                f"{question}, на цей пункт вже отримана вiдповiдь.")
             return

        if callback_query.data == "Commment":
            await ask_comment(chat_id, question, state, answers, callback_query)
            return

        if callback_query.data == "ok":
            answers[question] = "Все чисто"

        if len(answers) == len(checklist):
            await CheckList.next()
            await ask_setImage(chat_id)
            return


        await ask_question(chat_id, state, answers)

    except Exception as e:
        logging.exception(e)
        return None, 0


async def ask_question(chat_id, state, answers):
    """
    Ask question
    """
    try:
        question = checklist[0] if len(answers) == 0 else [item for item in checklist if item not in answers][0]

        answers[question] = None

        await state.update_data(answers=answers)
        keyboard = checklist_keyboard()
        await dp.bot.send_message(
            chat_id, 
            f"{question}\n\nВиберіть варіант відповіді:",
            reply_markup=keyboard
        )
    except Exception as e:
        logging.exception(e)
        return None, 0


async def ask_comment(chat_id, question, state, answers, callback_query):
    """
    Process ask comment
    """    
    await state.update_data(answers=answers)
    await dp.bot.send_message(chat_id, "Введіть свiй коментар:")
    await dp.bot.answer_callback_query(callback_query.id)

@dp.message_handler(state=CheckList.answers, content_types=types.ContentType.TEXT) 
async def set_comment(message: types.Message, state: FSMContext):
    """
    Set comment, and ask next question
    """
    try:
        chat_id = message.from_user.id

        async with state.proxy() as data:
            data = await state.get_data()

        answers = data['answers']
        question_index = len(answers) - 1

        question = checklist[question_index]
        answers[question] = message.text
        await state.update_data(answers=answers)

        if len(answers) == len(checklist):
            await CheckList.next()
            await ask_setImage(chat_id)
            return

        await ask_question(chat_id, state, answers)

    except Exception as e:
        logging.exception(e)
        return None, 0


async def ask_setImage(chat_id):
    """
    Функція, питання вибору image
    """
    try:

        await CheckList.image.set()

        await dp.bot.send_message(
            chat_id, 
            f"Виберiть фото:")
        
    except Exception as e:
        logging.exception(e)
        return None, 0


@dp.message_handler(state=CheckList.image, content_types=types.ContentType.PHOTO) 
async def set_image(message: types.Message, state: FSMContext):
    """
    Функція, вибору image
    """
    
    try:
        destination_file=f"{message.photo[-1].file_id}.jpg"
        await message.photo[-1].download(destination_file=destination_file) 

        await state.update_data(image=destination_file)
        async with state.proxy() as data:
            data = await state.get_data()

        location = data["location"]
        answers = data['answers']
        image = data['image']
        
        question = "\n".join([f"{key}: {value}" for key, value in answers.items()])

        result = get_ai_answer(question, image)

        await dp.bot.send_message(
            message.from_user.id,
            result
        )
    except Exception as e:
        logging.exception(e)
        return None, 0


def get_ai_answer(question, image_url):

    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question},
            {"role": "assistant", "content": "image: " + image_url},
        ],
        n=1,
        max_tokens=100,
        stop=None,
        temperature=0.7
    )

    return response['choices'][0]['message']['content']


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())
    


