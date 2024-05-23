import asyncio
import logging
import os
from typing import Dict

import aiohttp
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile

import utils.keyboards as kb
from utils import watermarker

BOT_TOKEN = os.getenv("BOT_TOKEN")

if BOT_TOKEN is None:
    logging.error("Bot token not found in environment variables")
    raise SystemExit("Bot token not found. Exiting...")


API = "http://127.0.0.1:5000"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_params: Dict[int, Dict[str, any]] = {}


class UserState(StatesGroup):
    waiting_for_text = State()


@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer("\n\nThis bot helps you add watermarks to your images."
                         "\n\nTo get started, please send me an image you'd like to watermark."
                         "\n\nOnce you've sent an image, I'll guide you through the process of adding a watermark."
                         "\n\n_Pro tip: Send an image along with a caption, "
                         "and I'll generate a watermarked version for you using default parameters."
                         "\n\nAnd you can also send your image as a document, "
                         "but I know how to work only with PNG, JPG and JPEG at the moment._",
                         parse_mode="Markdown")


@dp.message(CommandStart())
async def handle_start(message: Message):
    await message.answer(
        "🖼️ Welcome to the Watermark Bot! 🖼️"
        "\n\nThis bot helps you add watermarks to your images."
        "\n\nTo get started, please send me an image you'd like to watermark."
        "\n\nOnce you've sent an image, I'll guide you through the process of adding a watermark."
        "\n\n_Pro tip: Send an image along with a caption, "
        "and I'll generate a watermarked version for you using default parameters."
        "\n\nAnd you can also send your image as a document, "
        "but I know how to work only with PNG, JPG and JPEG at the moment._",
        parse_mode="Markdown")
    try:
        response = await post_data(f'{API}/users', data={'user_id': message.from_user.id})
        if response.status in (200, 201):
            logging.info("Posted User to API Successfully")
        else:
            logging.error(f"Something went wrong when tried to post user to API. Response: {response.text}")
    except Exception as e:
        logging.error(f"Something went wrong when tried to post user to API. Error: {e}")


@dp.message(F.photo)
async def get_photo(message: Message):
    try:
        if not os.path.exists(f"{message.from_user.id}"):
            os.makedirs(f"{message.from_user.id}")
        await message.bot.download(file=message.photo[-1].file_id,
                                   destination=f"{message.from_user.id}/{message.from_user.id}.jpg")
        if message.caption:
            user_id = message.from_user.id
            user_params[user_id] = {
                'text': message.caption,
                'position': 1,
                'color': (255, 255, 255),
                'opacity': 140,
                'size': 3
            }
            await send_watermark(user_id, message)
        else:
            await message.reply("Image received.\nChoose which watermark you want.",
                                reply_markup=kb.choose_watermark)
    except Exception as e:
        logging.error(f"Something went wrong while saving image. Error: {e}")
        await message.reply("Something went wrong. Please try again later.")


@dp.message(F.document)
async def get_doc(message: Message):
    try:
        if message.document.file_name.split('.')[-1] not in ["jpg", "jpeg", "png"]:
            await message.reply(
                "I don't know how to work with this type of document. "
                "Currently only JPG, JPEG and PNG are supported.\n\nPlease try again.")
        else:
            if not os.path.exists(f"{message.from_user.id}"):
                os.makedirs(f"{message.from_user.id}")
            await message.bot.download(file=message.document.file_id,
                                       destination=f"{message.from_user.id}/{message.from_user.id}.jpg")
            if message.caption:
                user_id = message.from_user.id
                user_params[user_id] = {
                    'text': message.caption,
                    'position': 1,
                    'color': (255, 255, 255),
                    'opacity': 140,
                    'size': 3
                }
                await send_watermark(user_id, message)
            else:
                await message.reply("Image received.\nChoose which watermark you want.",
                                    reply_markup=kb.choose_watermark)
    except Exception as e:
        logging.error(f"Something went wrong while saving file. Error: {e}")
        await message.reply("Something went wrong. Please try again later.")


@dp.callback_query(F.data == "custom_watermark")
async def choose_transparency(callback: types.CallbackQuery):
    await bot.edit_message_text(text="Choose watermark transparency", chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id)
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                        reply_markup=kb.choose_transparency)


@dp.callback_query(F.data.startswith("transparency_"))
async def choose_position(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_params[user_id] = {
        'text': 'Sample Watermark',
        'position': 1,
        'color': (255, 255, 255),
        'opacity': 140,
        'size': 3
    }
    transparency_map = {0: 255, 10: 230, 20: 205, 30: 180, 40: 155, 50: 128, 60: 100, 70: 75, 80: 50, 90: 25}
    user_params[user_id]['opacity'] = transparency_map.get(int(callback.data.split("_")[1]), 50)
    await bot.edit_message_text(text="Choose watermark position", chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id)
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                        reply_markup=kb.choose_position)


@dp.callback_query(F.data.startswith("position_"))
async def choose_position(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    position_map = {"position_center": 1, "position_up_left": 2, "position_up_right": 3, "position_down_left": 4,
                    "position_down_right": 5, "position_whole_image": 6}
    user_params[user_id]['position'] = position_map.get(callback.data, 1)
    await bot.edit_message_text(text="Choose watermark size", chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id)
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                        reply_markup=kb.choose_size)


@dp.callback_query(F.data.startswith("size_"))
async def choose_position(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    size_map = {"size_small": 1, "size_medium": 2, "size_large": 3, "size_xlarge": 4}
    user_params[user_id]['size'] = size_map.get(callback.data, 3)
    await bot.edit_message_text(text="Choose watermark color", chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id)
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                        reply_markup=kb.choose_color)


@dp.callback_query(F.data.startswith("color_"))
async def choose_position(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    color_map = {"color_white": (255, 255, 255), "color_black": (0, 0, 0)}
    user_params[user_id]['color'] = color_map.get(callback.data, (255, 255, 255))
    await bot.send_message(callback.message.chat.id, "Please send text for watermark.")
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await state.set_state(UserState.waiting_for_text)


@dp.callback_query(F.data == "default_watermark")
async def default_watermark(callback: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    user_id = callback.from_user.id
    user_params[user_id] = {
        'text': 'Sample Watermark',
        'position': 1,
        'color': (255, 255, 255),
        'opacity': 140,
        'size': 3
    }
    await bot.send_message(callback.message.chat.id, "Please send text for watermark.")
    await state.set_state(UserState.waiting_for_text)


@dp.message(UserState.waiting_for_text)
async def receive_watermark_text(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_params[user_id]["text"] = message.text
    await state.set_state(None)
    await send_watermark(user_id, message)


@dp.message()
async def text_without_image(message: types.Message, state: FSMContext):
    if await state.get_state() is None:
        await message.reply("Sorry, but I don't understand what you want. Please send image."
                            "\n_Currently I support photos and documents (PNG, JPG and JPEG)_", parse_mode="Markdown")
    else:
        await receive_watermark_text(message, state)


async def send_watermark(user_id: int, message: types.Message):
    watermarker.add_text_watermark(folder=str(user_id), image_name=f"{user_id}.jpg",
                                   text=user_params[user_id]["text"],
                                   position=int(user_params[user_id]["position"]),
                                   color=user_params[user_id]["color"],
                                   opacity=int(user_params[user_id]["opacity"]),
                                   size=int(user_params[user_id]["size"]))
    watermarked_image = FSInputFile(f"{user_id}/watermarked.png")
    await message.answer_photo(watermarked_image)

    try:
        response = await post_data(f'{API}/watermarks', data={'user_id': message.from_user.id})
        if response.status in (200, 201):
            logging.info("Posted Watermark to API Successfully")
        else:
            logging.error(f"Something went wrong when tried to post watermark to API. Response: {response.text}")
    except Exception as e:
        logging.error(f"Something went wrong when tried to post watermark to API. Error: {e}")

    await watermarker.clear_folder(f"{user_id}")
    await message.answer("Here is your watermarked image!\n\nJust send another image if you need more!")


async def post_data(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            return response


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    await asyncio.gather(dp.start_polling(bot))


if __name__ == "__main__":
    asyncio.run(main())
