import asyncio
import logging
import sqlite3

import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import executor
from PIL import Image
from io import BytesIO
from aiogram.dispatcher.filters import Command

import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np
import pandas as pd

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS status (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        type TEXT
    )
""")

prev_data = {
    '---': '-'
}

url = '1.csv'
data11 = pd.read_csv(url, on_bad_lines='skip', delimiter=',')

url = '2.csv'
data2 = pd.read_csv(url, on_bad_lines='skip', delimiter=',')

url = '3.csv'
data3 = pd.read_csv(url, on_bad_lines='skip', delimiter=',')

url = '4.csv'
data4 = pd.read_csv(url, on_bad_lines='skip', delimiter=',')

url = '5.csv'
data5 = pd.read_csv(url, on_bad_lines='skip', delimiter=',')

url = '6.csv'
data6 = pd.read_csv(url, on_bad_lines='skip', delimiter=',')

url = '7.csv'
data7 = pd.read_csv(url, on_bad_lines='skip', delimiter=',')

url = '8.csv'
data8 = pd.read_csv(url, on_bad_lines='skip', delimiter=',')

url = '9.csv'
data9 = pd.read_csv(url, on_bad_lines='skip', delimiter=',')

url = '10.csv'
data10 = pd.read_csv(url, on_bad_lines='skip', delimiter=',')

# for i in range(4, 11):
#   url = 'proba' + str(i) + '.csv'
#   data3 = pd.read_csv(url, on_bad_lines='skip', delimiter=',')


bot = Bot(token="6562601848:AAGmXoo2fGcBa1mlgzYBIDbESkezB_lvj-4")
dp = Dispatcher(bot)  # Уберите параметр bot из Dispatcher, если он не поддерживается в вашей версии aiogram
logging.basicConfig(level=logging.INFO)


def create_fio_to_id_dict():
    fio_to_id = {
        "Киселева Софья Ивановна": 0,
        "Орлова Ярослава Петровна": 1,
        "Зимина Василиса Фёдоровна": 2,
        "Колесников Константин Владиславович": 3,
        "Князева Виктория Макаровна": 4,
        "Старостина Анастасия Олеговна": 5,
        "Орлова Александра Артемьевна": 6,
        "Артамонов Максим Матвеевич": 7,
        "Булгакова Екатерина Романовна": 8,
        "Семенова Виктория Макаровна": 9,
    }
    return fio_to_id



def change_status(user_id, set):
    conn = sqlite3.connect("database.db", check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM status WHERE user_id = ?", (user_id,))
    existing_record = cursor.fetchone()

    if existing_record:
        cursor.execute("UPDATE status SET type = ? WHERE user_id = ?", (set, user_id,))
    else:
        cursor.execute("INSERT INTO status (user_id, type) VALUES (?, ?)", (user_id, set))

    conn.commit()

def check_status(user_id):
    conn = sqlite3.connect("database.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT type FROM status WHERE user_id = ?", (user_id,))
    status = cursor.fetchall()
    print(status[0])
    return status[0]
    conn.commit()



async def delete_user_messages(user_id, chat_id, message_id):
    await asyncio.sleep(1)
    await bot.delete_message(chat_id, message_id)

@dp.message_handler(Command('start'))
async def start(message: types.Message):
    user_id = message.from_user.id
    change_status(user_id, "none")
    username = message.from_user.username
    chat_id = message.chat.id
    message_id = message.message_id
    if user_id:
        await delete_user_messages(user_id, chat_id, message_id)
    markup = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton("Индивидуальная статистика📊", callback_data='type1')
    btn2 = InlineKeyboardButton("Статистика класса📈", callback_data='type2')
    btn5 = InlineKeyboardButton("Связь с разработчиками 📶", callback_data='type5', url="https://t.me/Danil13x")
    markup.add(btn1, btn2, btn5)
    if username:
        await message.answer(f"Здравствуйте, {username}! Выберите интересующий вас вариант демеонстрации статистики по пробникам ЕГЭ:", reply_markup=markup)
    else:
        await message.answer(
            f"Здравствуйте! Выберите интересующий вас вариант демеонстрации статистики по пробникам ЕГЭ:",
            reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data in ['type1', 'type2'])
async def process_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    change_status(user_id, "none")
    if callback_query.data == "type1":
        markup = InlineKeyboardMarkup(row_width=1)
        btn1 = InlineKeyboardButton("По конкретному пробнику1️⃣", callback_data='type_individual_one')
        btn2 = InlineKeyboardButton("За все время🕗", callback_data='type_individual_all')
        back = InlineKeyboardButton("⬅Назад", callback_data='back')
        markup.add(btn1, btn2, back)

        await callback_query.message.edit_text("Выберите тип демонстрации статистики конкретного человека:", reply_markup=markup)
    else:
        markup = InlineKeyboardMarkup(row_width=1)
        btn1 = InlineKeyboardButton("По конкретному пробнику1️⃣", callback_data='type_class_one')
        btn2 = InlineKeyboardButton("За все время🕗", callback_data='type_class_all')
        back = InlineKeyboardButton("⬅Назад", callback_data='back')
        markup.add(btn1, btn2, back)

        await callback_query.message.edit_text("Выберите тип демонстрации статистики класса:", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data in ['type_class_one', 'type_class_all'])
async def process_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if callback_query.data == 'type_class_one':
        change_status(user_id, "type_class_one")
        markup = InlineKeyboardMarkup(row_width=1)
        back = InlineKeyboardButton("⬅В начало", callback_data='back')
        markup.add(back)
        await callback_query.message.edit_text("Введите номер пробника, по которому вы хотите получить статистику всего класса:", reply_markup=markup)
    else:
        try:
            num = callback_query.message.text
            datas = [data11, data2, data3, data4, data5, data6, data7, data8, data9, data10]
            maxball = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 2, 2, 3, 4, 4]
            imaxball = 0
            prob_count = 10
            for bl in maxball:
                imaxball += bl

            tasks = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13', 't14', 't15', 't16',
                     't17', 't18']
            for data1 in datas:
                data1['sum'] = data1['t1'] + data1['t2'] + data1['t3'] + data1['t4'] + data1['t5'] + data1['t6'] + data1[
                    't7'] + data1['t8'] + data1['t9'] + data1['t10'] + data1['t11'] + data1['t12'] + data1['t13'] + data1[
                                   't14'] + data1['t15'] + data1['t16'] + data1['t17'] + data1['t18']
            data = data1  # номер пробника
            id = 0  # id ученика

            np.random.seed(191)
            scores = []
            for data in datas:
                scores.append(data['sum'].mean())
            plt.xticks(np.arange(0, prob_count), labels=np.arange(1, prob_count + 1))
            plt.xlabel('Номер пробника')
            plt.ylabel('Средний балл по классу')
            plt.plot(scores)
            plt.grid()

            buf = BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            change_status(user_id, "none")
            markup = InlineKeyboardMarkup(row_width=1)
            back = InlineKeyboardButton("⬅В начало", callback_data='back')
            markup.add(back)
            await bot.send_photo(user_id, photo=buf, caption=f"Выше приведенны данные класса, за все время", reply_markup=markup)
            await callback_query.message.delete()
            plt.close()
            await asyncio.sleep(1)
        except:
            change_status(user_id, "none")
            markup = InlineKeyboardMarkup(row_width=1)
            back = InlineKeyboardButton("⬅В начало", callback_data='back')
            markup.add(back)
            await callback_query.message.edit_text("Указаны некоректные данные =(",
                                 reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data in ['type_individual_one', 'type_individual_all'])
async def process_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if callback_query.data == 'type_individual_one':

        change_status(user_id, "type_individual_one")
        markup = InlineKeyboardMarkup(row_width=1)
        back = InlineKeyboardButton("⬅В начало", callback_data='back')
        markup.add(back)
        await callback_query.message.edit_text("Введите ФИО ученика, по которому хотете получить статистик, разделяя пробелом.\nПример: Киселева Софья Ивановна", reply_markup=markup)
    elif callback_query.data == 'type_individual_all':
        change_status(user_id, "type_individual_all")
        markup = InlineKeyboardMarkup(row_width=1)
        back = InlineKeyboardButton("⬅В начало", callback_data='back')
        markup.add(back)
        await callback_query.message.edit_text("Введите ФИО ученика, по которому хотете получить статистику, разделяя пробелом.\nПример: Киселева Софья Ивановна", reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'back')
async def process_callback(callback_query: types.CallbackQuery):
    try:
        user_id = callback_query.from_user.id
        change_status(user_id, "none")
        markup = InlineKeyboardMarkup(row_width=1)
        btn1 = InlineKeyboardButton("Индивидуальная статистика📊", callback_data='type1')
        btn2 = InlineKeyboardButton("Статистика класса📈", callback_data='type2')
        btn5 = InlineKeyboardButton("Связь с разработчиками 📶", callback_data='type5', url="https://t.me/Danil13x")
        markup.add(btn1, btn2, btn5)
        await callback_query.message.edit_text("Выберите интересующий вас вариант демеонстрации статистики по пробникам ЕГЭ:",
                             reply_markup=markup)
    except:
        user_id = callback_query.from_user.id
        change_status(user_id, "none")
        markup = InlineKeyboardMarkup(row_width=1)
        btn1 = InlineKeyboardButton("Индивидуальная статистика📊", callback_data='type1')
        btn2 = InlineKeyboardButton("Статистика класса📈", callback_data='type2')
        btn5 = InlineKeyboardButton("Связь с разработчиками 📶", callback_data='type5', url="https://t.me/Danil13x")
        markup.add(btn1, btn2, btn5)
        await bot.send_message(user_id,
            "Выберите интересующий вас вариант демеонстрации статистики по пробникам ЕГЭ:",
            reply_markup=markup)
        await callback_query.message.delete()


@dp.message_handler()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    message_id = message.message_id

    if str(check_status(user_id)) == "('type_individual_one',)":
        try:
            prev_data[user_id] = message.text
            markup = InlineKeyboardMarkup(row_width=1)
            back = InlineKeyboardButton("⬅В начало", callback_data='back')
            markup.add(back)
            await bot.send_message(user_id, "Ввыедите номер пробника, по которому хотите получить статистику:", reply_markup=markup)
            change_status(user_id, "type_individual_one_num")
        except:
            change_status(user_id, "none")
            markup = InlineKeyboardMarkup(row_width=1)
            back = InlineKeyboardButton("⬅В начало", callback_data='back')
            markup.add(back)
            await bot.send_message(user_id, "Указаны некоректные данные =(",
                                 reply_markup=markup)
    elif str(check_status(user_id)) == "('type_individual_one_num',)":

        try:
            fio_to_id_dict = create_fio_to_id_dict()

            important_id = 0
            if prev_data[user_id] in fio_to_id_dict:
                important_id = fio_to_id_dict[prev_data[user_id]]
                print("ok")


            num = message.text
            datas = {
                '1': data11,
                '2': data2,
                '3': data3,
                '4': data4,
                '5': data5,
                '6': data6,
                '7': data7,
                '8': data8,
                '9': data9,
                '10': data10,
            }
            maxball = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 2, 2, 3, 4, 4]
            imaxball = 0
            prob_count = 10
            for bl in maxball:
                imaxball += bl

            tasks = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13', 't14', 't15', 't16',
                     't17', 't18']
            data1 = datas[str(num)]
            data1['sum'] = data1['t1'] + data1['t2'] + data1['t3'] + data1['t4'] + data1['t5'] + data1['t6'] + data1[
                    't7'] + data1['t8'] + data1['t9'] + data1['t10'] + data1['t11'] + data1['t12'] + data1['t13'] + data1[
                                   't14'] + data1['t15'] + data1['t16'] + data1['t17'] + data1['t18']
            data = data1
            id = important_id
            np.random.seed(191)
            ans = pd.DataFrame()

            ans['balls'] = data.iloc[id][tasks].tolist()
            ans['max'] = maxball
            print(ans)
            ans_str = ans.to_string(index=True)
            await bot.send_message(user_id, f"Ниже приведенны данные ученика: {prev_data[user_id]}, за пробник номер {num}:\n№ {ans_str}")
        except:
            change_status(user_id, "none")
            markup = InlineKeyboardMarkup(row_width=1)
            back = InlineKeyboardButton("⬅В начало", callback_data='back')
            markup.add(back)
            await bot.send_message(user_id, "Указаны некоректные данные =(",
                                 reply_markup=markup)
    elif str(check_status(user_id)) == "('type_individual_all',)":
        try:
            num = message.text

            fio_to_id_dict = create_fio_to_id_dict()

            important_id = 0
            if num in fio_to_id_dict:
                important_id = fio_to_id_dict[num]
                print("ok")

            datas = [data11, data2, data3, data4, data5, data6, data7, data8, data9, data10]
            maxball = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 2, 2, 3, 4, 4]
            imaxball = 0
            prob_count = 10
            for bl in maxball:
                imaxball += bl

            tasks = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13', 't14', 't15', 't16',
                     't17', 't18']
            for data1 in datas:
                data1['sum'] = data1['t1'] + data1['t2'] + data1['t3'] + data1['t4'] + data1['t5'] + data1['t6'] + data1[
                    't7'] + data1['t8'] + data1['t9'] + data1['t10'] + data1['t11'] + data1['t12'] + data1['t13'] + data1[
                                   't14'] + data1['t15'] + data1['t16'] + data1['t17'] + data1['t18']
            data = data1  # номер пробника
            id = important_id  # id ученика


            np.random.seed(191)
            scores = []
            for data in datas:
                scores.append(data.iloc[id]['sum'].tolist())

            plt.xticks(np.arange(0, prob_count), labels=np.arange(1, prob_count + 1))
            plt.xlabel('Номер пробника')
            plt.ylabel('Средний балл ученика')
            plt.plot(scores)
            plt.grid()

            buf = BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)

            await bot.send_photo(user_id, photo=buf, caption=f"Выше приведенны данные {num}, за все пробники")
            plt.close()
            await asyncio.sleep(1)
        except:
            change_status(user_id, "none")
            markup = InlineKeyboardMarkup(row_width=1)
            back = InlineKeyboardButton("⬅В начало", callback_data='back')
            markup.add(back)
            await bot.send_message(user_id, "Указаны некоректные данные =(",
                                 reply_markup=markup)
    elif str(check_status(user_id)) == "('type_class_one',)":
        try:
            num = message.text
            datas = {
                '1': data11,
                '2': data2,
                '3': data3,
                '4': data4,
                '5': data5,
                '6': data6,
                '7': data7,
                '8': data8,
                '9': data9,
                '10': data10,
            }
            maxball = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 2, 2, 3, 4, 4]
            imaxball = 0
            prob_count = 10
            for bl in maxball:
                imaxball += bl

            tasks = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13', 't14', 't15', 't16',
                     't17', 't18']
            data1 = datas[str(num)]
            data1['sum'] = data1['t1'] + data1['t2'] + data1['t3'] + data1['t4'] + data1['t5'] + data1['t6'] + data1[
                't7'] + data1['t8'] + data1['t9'] + data1['t10'] + data1['t11'] + data1['t12'] + data1['t13'] + data1[
                               't14'] + data1['t15'] + data1['t16'] + data1['t17'] + data1['t18']
            data = data1
            id = 0
            np.random.seed(191)

            sum = 0
            ans2 = pd.DataFrame()
            avg = []
            for i in range(18):
                task = 't' + str(i + 1)
                sum = data[task].sum()
                avg.append(10 * sum / (maxball[i]))
            plt.figure(figsize=(9, 6))
            df = pd.DataFrame(avg)
            df = df[::-1]
            ax = df.plot(kind='barh', title='Гистограмма', width=0.9, color='green', legend=False)
            plt.yticks(np.arange(0, 18), labels=np.flip(np.arange(1, 19)))
            plt.ylabel('Номер задания')
            plt.xlabel('Процент правильных ответов')

            buf = BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)

            await bot.send_photo(user_id, photo=buf, caption=f"Выше приведенны данные класса, за пробник номер {num}")
            plt.close()
            await asyncio.sleep(1)
        except:
            change_status(user_id, "none")
            markup = InlineKeyboardMarkup(row_width=1)
            back = InlineKeyboardButton("⬅В начало", callback_data='back')
            markup.add(back)
            await bot.send_message(user_id, "Указаны некоректные данные =(",
                                 reply_markup=markup)

    if user_id:
        await delete_user_messages(user_id, chat_id, message_id)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
