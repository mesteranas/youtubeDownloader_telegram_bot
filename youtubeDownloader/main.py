import requests
import message,app
import os
import telegram
from telegram import InlineKeyboardMarkup,InlineKeyboardButton
from telegram.ext import CommandHandler,MessageHandler,filters,ApplicationBuilder,CallbackQueryHandler
import pafy
import re
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)
with open("token.bot","r",encoding="utf-8") as file:
    bot=ApplicationBuilder().token(file.read()).build()
async def download(update,contextt):
    file=update.message.text
    video=pafy.new(file)
    info=update.effective_user
    MessageId=await message.Sendmessage(info.id,"downloading")
    path=os.path.join("cach",str(info.id))
    if not os.path.exists(path):
        os.makedirs(path)
    name=sanitize_filename(video.title) + ".mp4"
    try:
        with requests.get(video.getbest().url,stream=True) as r:
            if r.status_code!=200:
                await error(info.id,MessageId,path)
                return
            with open(os.path.join(path, name),"wb") as reseived:
                for pk in r.iter_content(1024):
                    reseived.write(pk)
        await message.Editmessage(info.id,"uploading to telegram",MessageId)
        await contextt.bot.send_document(chat_id=info.id,document=open(os.path.join(path,name),"rb"),caption="uploaded by {} ".format(str(info.id)))
        os.remove(os.path.join(path,name))
        await contextt.bot.delete_message(chat_id=info.id,message_id=MessageId)
    except Exception as e:
        print(e)

        await error(info.id,MessageId,path)
async def error(id,MessageId,path):
    await message.Editmessage(id,"error while downloading ",MessageId)
    try:
        for file in os.listdir(path):
            os.remove(os.path.join(path,file))
    except:
        pass

async def start(update,contextt):
    info=update.effective_user
    keyboard=InlineKeyboardMarkup([[InlineKeyboardButton("donate",url="https://www.paypal.me/AMohammed231")],[InlineKeyboardButton("help",callback_data="help")]])
    await message.Sendmessage(chat_id=info.id,text="welcome " + str(info.first_name) + " to this bot. please send video URL",reply_markup=keyboard)
async def helb(update,contextt):
    links="""<a href="https://t.me/mesteranasm">telegram</a>

<a href="https://t.me/tprogrammers">telegram channel</a>

<a href="https://x.com/mesteranasm">x</a>

<a href="https://Github.com/mesteranas">Github</a>

email:
anasformohammed@gmail.com

<a href="https://Github.com/mesteranas/youtubeDownloader_telegram_bot">visite project on Github</a>
"""
    info=update.effective_user
    await message.Sendmessage(info.id,"""name: {}\nversion: {}\ndescription: {}\n developer: {}\n contect us {}""".format(app.name,str(app.version),app.description,app.developer,links))
async def callBake(update,contextt):
    q=update.callback_query
    q.answer()
    if q.data=="help":
        await helb(update,contextt)

print("running")
bot.add_handler(CommandHandler("start",start))
bot.add_handler(CommandHandler("help",helb))
bot.add_handler(MessageHandler(filters.TEXT,download))
bot.add_handler(CallbackQueryHandler(callBake))
bot.run_polling()