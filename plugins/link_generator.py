#(©)Codexbotz

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS
from helper_func import encode, get_message_id

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(text = "🔰 اولین پیام را از کانال دیتابیس ارسال نمائید (با نقل قول) و یا لینک همان پست در دیتابیس را بفرستید.", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply("❌ خطا\n🔸️ پست فوروارد شده یا لینک ارسال شده از کانال دیتابیس من نیست.", quote = True)
            continue

    while True:
        try:
            second_message = await client.ask(text = "🔰 آخرین پیام را از کانال دیتابیس ارسال نمائید (با نقل قول) و یا لینک همان پست در دیتابیس را بفرستید.", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply("❌ خطا\n🔸️ پست فوروارد شده یا لینک ارسال شده از کانال دیتابیس من نیست.", quote = True)
            continue


    string = f"{f_msg_id * int(str(abs(client.db_channel.id))[3:])}-{s_msg_id * int(str(abs(client.db_channel.id))[3:])}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 اشتراک‌گذاری لینک", url=f'https://telegram.me/share/url?url={link}')]])
    await second_message.reply_text(f"<b>🔗 لینک دانلود این فایل‌ها:</b>\n\n{link}", quote=True, reply_markup=reply_markup)


@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    while True:
        try:
            channel_message = await client.ask(text = "🔰 پستی را از کانال دیتابیس ارسال نمائید (با نقل قول) و یا لینک همان پست در دیتابیس را بفرستید.", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        else:
            await channel_message.reply("❌ خطا\n🔸️ پست فوروارد شده یا لینک ارسال شده از کانال دیتابیس من نیست.", quote = True)
            continue

    base64_string = await encode(f"{msg_id * int(str(abs(client.db_channel.id))[3:])}")
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 اشتراک‌گذاری لینک", url=f'https://telegram.me/share/url?url={link}')]])
    await channel_message.reply_text(f"<b>🔗 لینک دانلود این فایل</b>\n\n{link}", quote=True, reply_markup=reply_markup)
