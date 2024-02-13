from aiogram import Bot, Dispatcher, executor, types
import keyboards as kb
from dotenv import load_dotenv
import os
import DB

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)



@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(f'{message.from_user.first_name}, приветствую Вас! Я бот-трекер ваших отжиманий.',
                         reply_markup=kb.main)
    user = DB.User(tg_id=message.from_user.id)
    DB.session.add(user)
    DB.session.commit()
    await message.reply('Вы успешно зарегистрированы')
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Вы авторизовались как администратор!', reply_markup=kb.main_admin)


# @dp.message_handler(text='Рег')
# async def addpushup(message: types.Message):
#     user = DB.User(tg_id=message.from_user.id)
#     DB.session.add(user)
#     DB.session.commit()
#     await message.reply('Вы успешно зарегистрированы')

@dp.message_handler(text='Добавить')
async def addpushup(message: types.Message):
    user = DB.session.query(DB.User).filter_by(tg_id=message.from_user.id).first()
    if user:
        await message.reply('Введите количество отжиманий:')
    else:
        await message.reply('Вы не зарегистрированы!')

    @dp.message_handler(lambda message: message.text.isdigit())
    async def realadd(message: types.Message):
        pushup = DB.Pushup(number=int(message.text), user=user.id)
        DB.session.add(pushup)
        DB.session.commit()
        await message.reply('Отжимания добавлены!')



# @dp.message_handler(text='Просмотреть')
# async def viewpushup(message: types.Message):
#     await message.answer('Введите количество:')
#     @dp.message_handler('text')
#     async def realadd(message: types.Message):
#         session = DB.Session()
#         user = session.query(DB.User).filter_by(tg_id=message.from_user.id).first()
#
#         if user:
#             pushup = DB.Pushup(number = int(message.text), user_id=user.id)
#             session.add(pushup)
#             session.commit()
#
#             await message.reply('Отжимания добавлены!')
#         else:
#             await message.reply('Вы не зарегистрированы!')


@dp.message_handler(text='Просмотреть')
async def viewpushup(message: types.Message):
    user = DB.session.query(DB.User).filter_by(tg_id=message.from_user.id).first()
    if user:
        pushups = DB.session.query(DB.Pushup).filter_by(user=user.id).all()
        if pushups:
            reply_message = 'Ваши отжимания:\n'
            for pushup in pushups:
                reply_message += f'{pushup.number} - {pushup.created_at}\n'
            await message.reply(reply_message)
        else:
            await message.reply('У вас еще нет зарегистрированных отжиманий.')

@dp.message_handler(text='Админ-панель')
async def adminpan(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Вы вошли в админ-панель.', reply_markup=kb.admin_panel)
    else:
        await message.reply('Я тебя не понимаю.')


# @dp.message_handler()
# async def answer(message: types.Message):
#     await message.reply('Я тебя не понимаю.')


if __name__ == '__main__':
    executor.start_polling(dp)
