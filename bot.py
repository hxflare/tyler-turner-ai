from typing import Final
from telegram import *
from telegram.ext import *
from data_manager import Config
from ai_controller import ai
import logging
import os
import time
tyler=ai()
config=Config()
logging.basicConfig(filename=config.json['log-filename'],format='%(asctime)s %(message)s',filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)
last_question_time=time.time()
async def start(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_message.chat_id,action="typing")
    await update.message.reply_text("I think charlie kirks reflectivity is only matched by king von. Charlie is just THAT shiny. I want him to slither all over me, leaving trails of his shiny goopy skin excertions. I am just that aroused by his slug-like form. His shell is more intricate than anything in this world. If i was there, i would jump to save him. My beloved little slimey boy kirk! Oh that would be delightful if he crawled all over my mouth, blocking my airway so i had to breath in the air that came through him. I wamt him to debate me while he is on me, stuck to me with his shiny goopy snail foot, his shell bobbing from side to side.")
async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text=update.message.text
    if update.message.chat.type !="private":
        addressed=False
        for i in config.bot_names:
            if i.lower() in text.lower():
                text=text.lower().replace(i.lower(),"Tyler Turner")
                addressed=True
                break
        if not addressed:
            return
    await context.bot.send_chat_action(chat_id=update.effective_message.chat_id,action="typing")
    global last_question_time
    print(time.time()-last_question_time)
    if time.time()-last_question_time>30:
        
        print(update.message.text)
        os.makedirs(config.cache_dir,exist_ok=True)
        try:
            nh=context.user_data["history"]
        except:
            context.user_data["history"]=[]
        if not context.user_data["history"]:
            context.user_data["history"]=[]
        response=await tyler.respond(text,update.effective_user.username,None,context.user_data["history"])
        context.user_data["history"].append({"photo": None,"text": response[0]})
        await update.message.reply_text(response[0])
        last_question_time=time.time()
        with open(f"{config.cache_dir}/history.txt", "a") as f:
            f.write(f"\nuser @{update.effective_user.username} at {time.time()}:\n{text}\nResponse:\n{response[0]}")
    else: 
        await update.message.reply_text(f"Rate limited. Wait {round(30-time.time()+last_question_time)}s")
async def handle_images(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_message.chat_id,action="typing")
    global last_question_time
    print(last_question_time)
    if time.time()-last_question_time>60:
        photo=update.message.photo[-1]
        text=update.message.text
        os.makedirs(config.cache_dir,exist_ok=True)
        id=photo.file_id
        file: File=await context.bot.get_file(id)
        path=f"{config.cache_dir}/{id}"
        await file.download_to_drive(path)
        try:
            nh=context.user_data["history"]
        except:
            context.user_data["history"]=[]
        response=await tyler.respond(text,update.effective_user.username,path,context.user_data["history"])
        context.user_data["history"].append({"photo": response[1],"text": response[0]})
        await update.message.reply_text(response[0])
        last_question_time=time.time()
        with open(f"{config.cache_dir}/history.txt", "a") as f:
            f.write(f"\nuser @{update.effective_user.username} at {time.time()}:\n{text}\nResponse:\n{response[0]}")
    else: 
        await update.message.reply_text(f"Rate limited. Wait {round(60-time.time()+last_question_time)}s")

async def clear(update: Update,context:ContextTypes.DEFAULT_TYPE):
    context.user_data["history"]=[]
    await update.message.reply_text("Cleared your history.")
print("starting bot")
persistence=PicklePersistence(filepath=config.persistence_filename)
print("pers")
app=Application.builder().token(config.bot_token).persistence(persistence).build()
print("build")
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,handle_messages))
app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("clear",clear))
print("mess")
app.add_handler(MessageHandler(filters.PHOTO,handle_images))
print("img")
app.run_polling()
print("bot started")
