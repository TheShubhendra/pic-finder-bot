
########  IMPORTING MODULES   ######
from random import randint
from requests import get
import logging
import os
from telegram.ext import Updater ,CommandHandler , MessageHandler, Filters
from decouple import config
from pixabay import Image
#### CONSTANTS ####
TOKEN = config("TOKEN")
KEY =  config("KEY")
KEY2 = config("KEY2")
APP = "pic-finder-bot"
print(KEY)
print(TOKEN)
PORT = int(config('PORT', 5000))
PB_IMAGE = Image(KEY2)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
       context.bot.send_message(chat_id=update.message.chat_id, text="Hlw! "+update.message.from_user.first_name+ " This bot is developed by Shubhendra  Kushwaha , I can show you many random images of relevant keyword , to see the images simply send me show <keyword> or if you want images from gallery of NASA , send nasa <keyword> . This bot is open source anyone can contribute on GITHUB https://github.com/TheShubhendra/pic-finder-bot. If you found any bug or error , please create a issue on GITHUB")

def getUnsplash(keyword):
      url = "https://api.unsplash.com/search/photos/?client_id="+KEY+"&query="+keyword
      print(url)
      res = get(url).json()
      pics = res["results"]
      urls =[]
      for i in range(len(pics)):
        urls.append(pics[i]["urls"]["regular"])
      return urls
def getPixabay(keyword):
  res = PB_IMAGE.search(keyword)
  if len(res["hits"])>0:
    return [ hits["largeImageURL"] for hits in res["hits"] ]
  else:
    return []
def getNasa(keyword):
      url =  "https://images-api.nasa.gov/search?q="+keyword
      print(url)
      req = get(url)
      try:
        res = req.json()
      except:
        return []
      pics = res["collection"]["items"]
      urls = []
      print("len of pics : ",len(pics))
      for i in range(len(pics)):
        try:
          urls.append(pics[0]["links"][0]["href"])
        except:
          continue
      return urls
      
def geturl(source,keyword):
       print(keyword)
       urlList =[]
       if source == "nasa" :
         urlList+=getNasa(keyword)
       else:
         urlList+=getUnsplash(keyword)
         urlList+=getPixabay(keyword)
       print(urlList)
       if len(urlList)>0:
         return urlList[randint(0,len(urlList))];
       else:
         None
def pic(update,context):
         text = update.message.text.lower()
         if "show " in text:
            print(text)
            keyword = text.replace("show ",'')
            picUrl = geturl("unsplash",keyword)
            print(picUrl)
            print()
            if picUrl is not None:
              update.message.reply_photo(picUrl)
            else:
              update.message.reply_text("Sorry Image related {} not found :( ".format(keyword))
         elif "nasa " in text:
            keyword = text.replace("nasa ","")
            picUrl = geturl("nasa",keyword)
            print(picUrl)
            print()
            if picUrl is not None:
              update.message.reply_photo(picUrl)
            else:
              update.message.reply_text("Sorry Image related {} not found :( ".format(keyword))


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







