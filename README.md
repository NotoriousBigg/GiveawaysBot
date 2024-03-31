# GiveawaysBot
A Python telegram Bot to host giveaways for certain channels. Uses PyTelegramBotAPI

## BOT FUTURES
> Users are stored in local database
> Notifies every users in the database(only registered users) when a giveaway is started.
> Only Admin can start and end a giveaway.
> Bot selects random user when a giveaway ends and sends him/her a message that he/she is the winner.
> Admin gets the winners Details
 

## BOT COMMANDS
```
/start - to start the bot
/register - for registration to the bots database
/startgiveaway - for starting a giveaway
/endgiveaway - this will stop the giveaway and select and random user as the winner
/referral - to get your unique referral link(not fully functional)
```

To host on Your Local Machine:
```
python3 bot.py
```
For Nonstop running , Its recommended you use A vps.
to deploy on your vps:

#Clone this repository
```
git clone https://github.com/Muiruri42/GiveawaysBot
```
#Change directory to GiveawaysBot
```
cd GiveawaysBot
```
#Now we should make the bot run all times 24/7 even if the vps is closed.
we will use tmux to make sure that the bot do not stop.
```
tmux
```
#Now run the bot's script
```
python3 bot.py
```
#Now lets close the tmux terminal
```
ctrl + b
```
then click 
```
d
```
The bot should now be running 24/7 on your vps

##FOR ANY HELP:
(TELEGRAM)[https://t.me/EscaliBud] <br>
(WHATSAPP)[https://wa.me/254798242085] <br>

Visit my Website at https://infinityhackers.tech
Keep checking repo for Updates.
