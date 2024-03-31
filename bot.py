import telebot
from telebot import types
import sqlite3
import uuid
import random




APITOKEN = "6723604252:AAEuxHBsoJwiPgEqBtIDluLIBBhEAyYFRF4"
bot = telebot.TeleBot(APITOKEN)
admin = 1108915205
def is_owner(user_id):
    return user_id == admin
must_join = ['@InfinityHackersKE', '@InfinityBotsHub', '@Ihkmods']
user_channels = []
@bot.message_handler(commands=['start', 'help'])
def handle_welcome(message):

    user_channels.clear()  # Clear the user's channel list upon starting
    send_channels_to_join(message)
def send_channels_to_join(message):
    kb = types.InlineKeyboardMarkup()
    for channel in must_join:
        kb.row(types.InlineKeyboardButton(channel, callback_data=channel))

    bot.send_message(message.chat.id, "Please join the following channels:", reply_markup=kb)

    @bot.callback_query_handler(func=lambda call: True)
    def handle_channel_join(call):
        channel = call.data
        if channel in must_join:
            if channel not in user_channels:
                user_channels.append(channel)
                bot.send_message(call.message.chat.id, f"You have joined {channel} successfully!")
                if len(user_channels) < 3:
                    send_channels_to_join(call.message)
                else:
                    bot.send_message(call.message.chat.id,
                                     "You have joined all required channels. You can now use the bot.\n\nRegister in the bot to participate in the giveaway. Send /register to start registration")
            else:
                bot.send_message(call.message.chat.id, f"You have already joined {channel}.")
        else:
            bot.send_message(call.message.chat.id, "Invalid channel selection.")
@bot.message_handler(commands=['register'])
def register_new_user(message):
    bot.send_message(message.chat.id, f"Hello {message.from_user.first_name}, To proceed,Type your Age in numbers. eg: 18")
    bot.register_next_step_handler(message, add_to_db)
def add_to_db(message):
    name = message.from_user.first_name
    age = message.text
    username = message.from_user.username
    user_id = message.from_user.id

    
    data = sqlite3.connect('users.db')
    mycursor = data.cursor()
    mycursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = mycursor.fetchone()
    
    if user is not None:
        bot.reply_to(message, "You are already registered! Enjoy your time.")
    else:
        referral_link = str(uuid.uuid4())
        mycursor.execute("INSERT INTO users (user_id, username, first_name, age, referral_link) VALUES (?, ?, ?, ?, ?)",
                   (user_id, username, name, age,referral_link))
        data.commit()
        bot.reply_to(message, """
Registration successful! Your unique user ID has been assigned.
You are now Participating the giveaway.
Invite your friends to our channels to increase your chances of becoming the winner.
""")

@bot.message_handler(commands=['startgiveaway'])
def start_giveaway(message):
    bot.send_message(message.chat.id, "Enter the Name of the give away.")
    bot.register_next_step_handler(message, addgiveaway)
def addgiveaway(message):
    giveaway_img = "https://i.ibb.co/Sdtf87N/file-128.jpg"
    giveawayname = message.text
    started_by = message.chat.id
    data = sqlite3.connect('users.db')
    mycursor = data.cursor()
    mycursor.execute("SELECT active FROM giveaway")
    active_giveaway = mycursor.fetchone()

    if active_giveaway and active_giveaway[0]:
        bot.reply_to(message, "There is already an active giveaway. Please wait for the current giveaway to end before starting a new one.")
    else:
        mycursor.execute("INSERT INTO giveaway (giveaway_name, started_by, active) VALUES (?, ?, ?)", (giveawayname, started_by, 1))
        data.commit()
        mycursor.execute('SELECT * FROM users')
        users = mycursor.fetchall()

        for user in users:
            user_id = user[0]
            firstname = user[2]
            giveaway_message =f"""
GIVEAWAY STARTED
Hello {firstname},This is to notify you that a giveaway has started.
No need to worry because you are already participating.
To increase your chances of winning, Share your invite link to your friends and ask them to start the bot and join the channels requested.
The giveaway draw will be done automatically and user will recieve his/her gift.
We wish you Good Luck....
"""
            bot.send_photo(user_id, photo=giveaway_img, caption=giveaway_message)
@bot.message_handler(commands=['endgiveaway'])
def end_giveaway(message):
    data = sqlite3.connect('users.db')
    mycursor = data.cursor()
    mycursor.execute("UPDATE giveaway SET active = 0 WHERE active = 1")
    data.commit()
    bot.reply_to(message, "Giveaway has ended. The winner will be announced shortly.")
    mycursor.execute('SELECT * FROM users ORDER BY RANDOM() LIMIT 1')
    winnerid = mycursor.fetchall()
    
    winner = random.choice(winnerid)
    

    if winner:
        winnerd = winner[0]
        firstname = winner[2]
        
        winner_img = "https://i.ibb.co/FDd5hLV/file-130.jpg"
        admin_winner_img = "https://i.ibb.co/b25FL1P/file-129.jpg"

        bot.send_photo(winnerd, photo=winner_img, caption=f"""
Hello there {firstname} , You have been selected as the random winner of the giveaway held by Infinity Hackers Kenya.
To recieve your gift, Chat with the admin @EscaliBud
""")
        bot.send_photo(message.chat.id, photo=admin_winner_img, caption=f"{firstname} has been selected.\n\n a winner has been selected as a random winner from the database.")
    else:
        bot.reply_to(message, "No user found in the database.")
@bot.message_handler(commands=['referral'])
def handle_referral(message):
    user_id = message.chat.id
    data = sqlite3.connect('users.db')
    mycursor = data.cursor()
    # Retrieve the user's referral link from the database
    mycursor.execute("SELECT referral_link FROM users WHERE user_id=?", (user_id,))
    referral_link = mycursor.fetchone()
    
    if referral_link is not None:
        bot.reply_to(message, f"Your referral link is: http://t.me/InfinityGiftsBot?start={referral_link[0]}. Share this link to refer others.")
    else:
        bot.reply_to(message, "You need to register and get your referral link first.")

bot.infinity_polling()