#!/usr/bin/python3
import os, logging, random, math, sys, platform
from telegram import Update
from telegram.ext import CommandHandler, Application, ContextTypes

sys.stdout = open('bot.log', "w")
sys.stderr = open("botErr.log", "w")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

scriptDir = os.path.dirname('__file__')
tokenFile = open(scriptDir + 'token', 'r')
token = tokenFile.read()

if platform.system() == 'Linux':
    cwd = os.getcwd() + '/'
    ffmpeg = "/usr/bin/ffmpeg"
    ffprobe = "/usr/bin/ffprobe"
    youtubedl = "/home/aephk/.local/bin/yt-dlp"
    deleteTemp = 'rm temp.*'

elif platform.system():
    cwd = os.getcwd() + '\\'
    ffmpeg = "C:\\youtubedl\\ffmpeg.exe"
    ffprobe = "C:\\youtubedl\\ffprobe.exe"
    youtubedl = "C:\\youtubedl\\yt-dlp.exe"
    deleteTemp = 'del temp.*'

else:
    print("Unable to determin OS version")
    exit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        "Me bot!"
    )

async def v(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    os.system(deleteTemp)
    chat_id1=update.effective_chat.id
    message_id=update.message.message_id
    url = context.args[0]
    capt = '<a href="' + url + '">Sent by: ' + update.message.from_user.first_name + '</a>'
    print(url)
    update.message.reply_video
    await (
    context.bot.deleteMessage(chat_id1, message_id)
    )
    downloadRequest = youtubedl + " -S res:720,+br --ffmpeg-location " + ffmpeg + " --merge-output-format mp4 -o " + cwd + "temp.mp4 " + url

    os.system(downloadRequest)
    
    try:
        os.rename(cwd + "temp.mp4", cwd + "temp.temp")

        #Get video length and calculate max video bitrate in order to come in under 50MB
        sourceLength = ffprobe + " -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 " + cwd + "temp.temp"
        finalMaxBitrate = math.floor((25/sourceLength)*8)
        videoBitrate = finalMaxBitrate-0.128

        command = ffmpeg + " -i " + cwd + 'temp.temp -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -b:v ' + videoBitrate + "M  -b:a 128k -maxrate " + finalMaxBitrate + "M -bufsize 1M" + cwd + 'temp.mp4'

        os.system(command)
    except:
        os.rename(cwd + "temp.temp", cwd + "temp.mp4")


    file = open(cwd + 'temp.mp4', 'rb')
    files = {
        'video' : file
        }
    await (
        context.bot.send_video(chat_id=chat_id1, video=file, parse_mode='html', caption=capt, disable_notification=True)
    )
    file.close()

    os.system(deleteTemp)

async def dab(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id1=update.effective_chat.id
    message_id=update.message.message_id

    await (
    context.bot.deleteMessage(chat_id1, message_id)
    )

    capt = update.message.from_user.first_name.upper() + " JUST DABBED!!! XD"

    file = open(cwd + 'dab.jpg', 'rb')
    await (
        context.bot.send_photo(chat_id=chat_id1, photo=file, caption=capt, disable_notification=True)
    )
    file.close()

async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id1=update.effective_chat.id
    message_id=update.message.message_id

    await (
    context.bot.deleteMessage(chat_id1, message_id)
    )

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
    
    await(
        context.bot.send_message(chat_id=update.effective_chat.id, disable_notification=True, text=message)
    )
    

def main() -> None:


    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler('roll', roll))
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('v', v))
    application.add_handler(CommandHandler('dab', dab))

    application.run_polling()

if __name__ == "__main__":
    main()