
########  IMPORTING MODULES   ######
import random
from requests import get
import logging
import os
import re
from telegram.ext import Updater ,CommandHandler , MessageHandler, Filters
from decouple import config
from pixabay import Image
import sys
import json
#### CONSTANTS ####
TOKEN = config("TOKEN")
KEY =  config("KEY")
KEY2 = config("KEY2")
APP = "pic-finder-bot"
print(KEY)
print(TOKEN)
PORT = int(config('PORT', 5000))
PB_IMAGE = Image(KEY2)
DATA = dict()
SPECIAL_QUERIES = {}
ADMIN_CHAT_ID = int(config("ADMIN_CHAT_ID"))
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def set_var(update,context):
  global SPECIAL_QUERIES
  if not update.message.chat_id == ADMIN_CHAT_ID:
    return
  else:
    text=update.message.text[9:]
    try:
      print(text)
      SPECIAL_QUERIES = json.loads(text)
      print(SPECIAL_QUERIES)
      update.message.reply_text(json.dumps(SPECIAL_QUERIES))
    except:
      update.message.reply_text("Something bad happened :(")



def source(update,context):
  text = update.message.text
  if "@" in text:
    text = text[:text.find("@")]
  chat_id = update.message.chat_id
  if chat_id not in DATA:
    DATA[chat_id] = []
  if text == "/reset_source":
    DATA[chat_id] = []
  else:
    source = text.split("_")[2]
    if source not in DATA[chat_id]:
      DATA[chat_id].append(source)
  source_elem = ""
  if len(DATA[chat_id])>0:
    for elem in DATA[chat_id]:
      source_elem = source_elem+" "+elem
  else:
    source_elem = "random sources"
  update.message.reply_text("Now you will receive images from {}.".format(source_elem))
  context.bot.send_message(ADMIN_CHAT_ID,str(DATA))
def start(update, context):
       context.bot.send_message(chat_id=update.message.chat_id, text="Hlw! "+update.message.from_user.first_name+ " This bot is developed by Shubhendra  Kushwaha , I can show you many random images of relevant keyword , to see the images simply send me show <keyword> or if you want images from gallery of NASA , send nasa <keyword> . This bot is open source anyone can contribute on GITHUB https://github.com/TheShubhendra/pic-finder-bot. If you found any bug or error , please create a issue on GITHUB")

def getUnsplash(keyword):
      url = "https://api.unsplash.com/search/photos/?client_id="+KEY+"&query="+keyword
      print(url)
      try:
        res = get(url).json()
        pics = res["results"]
      
        urls =[]
        for i in range(len(pics)):
          urls.append(pics[i]["urls"]["regular"])
      except:
        return []
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
      
def geturl(chat_id,keyword):
       print(keyword)
       print(SPECIAL_QUERIES)
       if keyword in SPECIAL_QUERIES:
         keyword = SPECIAL_QUERIES[keyword]
       source_list =[]
       func_dict = {"unsplash":getUnsplash,"pixabay":getPixabay,"nasa":getNasa}
       if chat_id in DATA.keys() and len(DATA[chat_id])>0:
          source_list = DATA[chat_id]
       else:
          source_list = ["unsplash","pixabay","nasa"]
       print(source_list)
       source = source_list[random.randint(0,len(source_list)-1)]
       urlList = func_dict[source](keyword)
       if len(urlList)==0:
         source = source_list[random.randint(0,len(source_list)-1)]
         urlList = func_dict[source](keyword)
         
       if len(urlList)>0:
         return urlList[random.randint(0,len(urlList)-1)];
       else:
         None
def pic(update,context):
            text = update.message.text.lower()
            print(text)
            keyword = text.replace("show ",'')
            picUrl = geturl(update.message.chat_id,keyword)
            print(picUrl)
            print()
            if picUrl is not None:
              update.message.reply_photo(picUrl)
            else:
              update.message.reply_text("Sorry {} not found :( ".format(keyword))
         

def main():
    updater = Updater(token=TOKEN,use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    pic_handler = MessageHandler(Filters.regex(re.compile(r'^show',re.IGNORECASE)),pic)
    source_handler = CommandHandler(["set_source_unsplash","set_source_pixabay","set_source_nasa","reset_source"],source)
    
    variable_handler= CommandHandler("set_var",set_var)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(pic_handler)
    dispatcher.add_handler(source_handler)
    dispatcher.add_handler(variable_handler)
    if len(sys.argv)>1 and sys.argv[1]=="-l":
        updater.start_polling()
    else:
        updater.start_webhook(listen="0.0.0.0",port=int(PORT),url_path=TOKEN)
        updater.bot.setWebhook("https://"+APP +".herokuapp.com/" + TOKEN)
        updater.idle()

if __name__ == '__main__':
    main()







