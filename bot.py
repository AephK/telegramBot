#!/usr/bin/python3
import os, subprocess, logging, requests, random, math
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import InlineQueryHandler 

scriptDir = os.path.dirname('__file__')
tokenFile = open(scriptDir + 'token', 'r')
token = tokenFile.read()

updater = Updater(token=token, use_context=True)

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

#cwd = os.getcwd() + '/'
#ffmpeg = "/usr/bin/ffmpeg"
#youtubedl = "/home/aephk/.local/bin/youtube-dl"
cwd = os.getcwd() + '\\'
ffmpeg = "C:\youtubedl\ffmpeg\bin\ffmpeg.exe"
youtubedl = "C:\youtubedl\youtube-dl.exe"
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="me bot")

def video(update, context):
    chat_id=update.effective_chat.id
    message_id=update.message.message_id
    name = "Sent by: " + update.message.from_user.first_name
    url = context.args[0]
    context.bot.deleteMessage(chat_id, message_id)
    downloadRequest = youtubedl + " --ffmpeg-location " + ffmpeg + " --max-filesize 50M --merge-output-format mp4 -o " + cwd + "temp.mp4 " + url
    
    os.system(downloadRequest)
    os.rename(cwd + "temp.mp4", cwd + "temp.temp")
    
    try:
        command = ffmpeg + " -i " + cwd + 'temp.temp -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" ' + cwd + 'temp.mp4'
        os.system(command)
    except:
        os.rename(cwd + "temp.temp", cwd + "temp.mp4")


    file = open(cwd + 'temp.mp4', 'rb')
    files = {
        'video' : file,
        'disable_notification' : 'true'
        }
    requests.post("https://api.telegram.org/bot1567021524:AAFHy6GiHcnND082qadOFaXwPdYBA7cI510/sendVideo?chat_id={}".format(update.effective_chat.id), files=files)
    file.close()
    context.bot.send_message(chat_id=update.effective_chat.id, disable_notification=True, text=name)

    os.remove(cwd + "temp.temp")
    os.remove(cwd + "temp.mp4")

#def test(update, context):
#    message = context.args[0]
#    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def dab(update, context):
    chat_id=update.effective_chat.id
    message_id=update.message.message_id
    context.bot.deleteMessage(chat_id, message_id)

    name = update.message.from_user.first_name.upper() + " JUST DABBED!!! XD"
    caption = {'caption' : name}

    file = open(cwd + 'dab.jpg', 'rb')
    files = {'photo' : file}
    requests.post("https://api.telegram.org/bot1567021524:AAFHy6GiHcnND082qadOFaXwPdYBA7cI510/sendPhoto?chat_id={}".format(update.effective_chat.id), files=files, data=caption)
    file.close()

def roll(update, context):
    chat_id=update.effective_chat.id
    message_id=update.message.message_id
    context.bot.deleteMessage(chat_id, message_id)
    name = update.message.from_user.first_name
    result = 0
    diceCount = 0
    diceType = 0

    if context.args:
        if 'd' in context.args[0]:
            roll = context.args[0]
            diceCount = roll.split('d')[0]
            diceType = roll.split('d')[1]
        
    else:
        diceCount = 1
        diceType = 20

    if str(diceCount).isdigit() and str(diceType).isdigit():
        diceCount = int(math.floor(float(diceCount)))
        diceType = int(math.floor(float(diceType)))

        if diceCount != 0 and diceType != 1 and diceType != 0:

            for i in range(diceCount):
                result += random.randint(1, diceType)

            message = name + " rolled " + str(diceCount) + "d" + str(diceType) + " and got: " + str(result)

        else:
            message = name + " failed the constipation check."

    else:
        message = name + " failed the constipation check."

    context.bot.send_message(chat_id=update.effective_chat.id, disable_notification=True, text=message)





start_handler = CommandHandler('roll', roll)
dispatcher.add_handler(start_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

start_handler = CommandHandler('video', video)
dispatcher.add_handler(start_handler)

start_handler = CommandHandler('dab', dab)
dispatcher.add_handler(start_handler)

#start_handler = CommandHandler('test', test)
#dispatcher.add_handler(start_handler)

updater.start_polling()
