from telethon import TelegramClient, events
from datetime import date, timedelta
import json
import os
from dotenv import load_dotenv
from background import keep_alive

load_dotenv()
data_1 = os.getenv("api_id")
data_2 = os.getenv("api_hash")
data_3 = os.getenv("phone")
client = TelegramClient(data_3, data_1, data_2)
file_names = []


@client.on(events.Album)
async def handler(event):
    text = event.text
    for i in event:
        if "Графік вимкнень" in text:
            tomorrow = date.today() + timedelta(days=1)
            file_name = f'img/image_group_{i.id}_{tomorrow.strftime("%d.%m.%Y")}.jpg'  # Генеруємо ім'я файлу для зберігання
            await i.download_media(file=file_name)
            print(f'Saved image {file_name}')

            file_names.append(file_name)

            file_names.sort()
            with open("photo.json", "w") as outfile:
                json.dump(file_names, outfile, indent=2)
            print('Запис у файл JSON виконаний!')


@client.on(events.NewMessage)
async def handler(event):
    text = event.text
    if event.photo:
        if "Графік вимкнень" in text:
            photo = event.photo
            tomorrow = date.today() + timedelta(days=1)
            file_name = f'img/image_{photo.id}_{tomorrow.strftime("%d-%m-%Y")}.jpg'
            await event.download_media(file=file_name)
            print(f'Saved image {file_name}')

            file_names.append(file_name)

            file_names.sort()
            with open("photo.json", "w") as outfile:
                json.dump(file_names, outfile, indent=2)
            print('Запис у файл JSON виконаний!')

keep_alive()
client.start()
client.run_until_disconnected()
