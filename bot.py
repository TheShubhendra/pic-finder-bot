
########  IMPORTING MODULES   ######
from random import randrange
import re
from requests import get
import logging
import os
from telegram.ext import Updater ,CommandHandler , MessageHandler, Filters
from decouple import config
#### CONSTANTS ####
TOKEN = config("TOKEN")
KEY =  config("KEY")
APP = "pic-finder-bot"
print(KEY)
print(TOKEN)
PORT = int(os.environ.get('PORT', 5000))



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
       context.bot.send_message(chat_id=update.message.chat_id, text="Hlw! "+update.message.from_user.first_name+ " This bot is developed by Shubhendra  Kushwaha , I can show you many random images of relevant keyword , to see the images simply send me sho <keyword> or if you want images from gallery of NASA , send nasa <keyword> . This bot is open source anyone can contribute on GITHUB https://github.com/TheShubhendra/pic-finder-bot. If you found any bug or error , please create a issue on GITHUB")

def geturl(source,r,keyword):
       print(keyword)
       if source == "unsplash" :
         url = "https://api.unsplash.com/search/photos/?client_id="+KEY+"&query="+keyword
         print(url)
         req = get(url)
         res = req.json()
         ls = res["results"]
         if len(ls)>0:
            return ls[randrange(len(ls))]["urls"][r]
       elif source == "nasa" :
         url =  "https://images-api.nasa.gov/search?q="+keyword
         print(url)
         req = get(url)
         res = req.json()
         ls = res["collection"]["items"]
         if len(ls)>0 :
            return ls[randrange(len(ls))]["links"][0]["href"]


def pic(update,context):
       if 1 or update.message.chat.type == "group":
         text = update.message.text.lower()
         comm = r"show "
         match1 = re.search(comm,text)
         match2 = re.search(r"nasa ",text)
         res = ["regular","raw","full","small","thumb"]
         if match1:
            text = text().split()
            if len(text) == 3 and text[2] in res:
              picUrl = getUrl("unsplash",text[2],text[1])
            else:
              picUrl = geturl("unsplash","regular",text[1])
            print(picUrl)
            print()
            context.bot.send_photo(update.effective_chat.id,picUrl)
         elif match2:
            q = text[match2.end():]
            picUrl = geturl("nasa",text)
            print(picUrl)
            print()
            context.bot.send_photo(update.effective_chat.id,picUrl)


def main():
    updater = Updater(token=TOKEN,use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    pic_handler = MessageHandler(Filters.text & (~ Filters.command) , pic)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(pic_handler)


    updater.start_webhook(listen="0.0.0.0",port=int(PORT),url_path=TOKEN)


    updater.bot.setWebhook("https://"+APP +".herokuapp.com/" + TOKEN)
   #updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()







