#!/usr/bin/python3
import os, subprocess, logging, requests, random, math, sys
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import InlineQueryHandler

sys.stdout = open('bot.log', "w")
sys.stderr = open("botErr.log", "w")

scriptDir = os.path.dirname('__file__')
tokenFile = open(scriptDir + 'token', 'r')
token = tokenFile.read()

updater = Updater(token=token, use_context=True)

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

#cwd = os.getcwd() + '/'
#ffmpeg = "/home/aephk/ffmpeg/ffmpeg"
#ffprobe = "/home/aephk/ffmpeg/ffmpeg"
#youtubedl = "/home/aephk/.local/bin/yt-dlp"
#deleteTemp = 'rm temp.*'
cwd = os.getcwd() + '\\'
ffmpeg = "C:\\youtubedl\\ffmpeg\bin\ffmpeg.exe"
ffprobe = "C:\\youtubedl\\ffmpeg\bin\ffprobe.exe"
youtubedl = "C:\\youtubedl\\yt-dlp.exe"
deleteTemp = 'del temp.*'

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="me bot")

def v(update, context):
    os.system(deleteTemp)
    chat_id=update.effective_chat.id
    message_id=update.message.message_id
    name = "Sent by: " + update.message.from_user.first_name
    url = context.args[0]
    print(url)
    context.bot.deleteMessage(chat_id, message_id)
    downloadRequest = youtubedl + " -S 'res:720,+br' --ffmpeg-location " + ffmpeg + " --merge-output-format mp4 -o " + cwd + "temp.mp4 " + url

    os.system(downloadRequest)
    
    try:
        os.rename(cwd + "temp.mp4", cwd + "temp.temp")

        #Get video length and calculate max video bitrate in order to come in under 50MB
        sourceLength = ffprobe + " -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 " + cwd + "temp.temp"
        finalMaxBitrate = math.floor((25000/sourceLength)*8)
        videoBitrate = finalMaxBitrate-0.128

        command = ffmpeg + " -i " + cwd + 'temp.temp -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -b:v ' + videoBitrate + "M  -b:a 128k -maxrate " + finalMaxBitrate + "M -bufsize 1M" + cwd + 'temp.mp4'

        os.system(command)
    except:
        os.rename(cwd + "temp.temp", cwd + "temp.mp4")


    file = open(cwd + 'temp.mp4', 'rb')
    files = {
        'video' : file
        }
    requests.post("https://api.telegram.org/bot" + token + "/sendVideo?chat_id={}".format(update.effective_chat.id) + "&caption=" + name, files=files)
    file.close()

    os.system(deleteTemp)
    #os.remove(cwd + "temp.*")

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
    requests.post("https://api.telegram.org/bot" + token + "/sendPhoto?chat_id={}".format(update.effective_chat.id), files=files, data=caption)
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

start_handler = CommandHandler('v', v)
dispatcher.add_handler(start_handler)

start_handler = CommandHandler('dab', dab)
dispatcher.add_handler(start_handler)

#start_handler = CommandHandler('test', test)
#dispatcher.add_handler(start_handler)

updater.start_polling()
