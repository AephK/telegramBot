Simple Telegram bot writtin in Python using [Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot)

---

## Features:
### /dab : send a squidward dabbing image and inform the chat that you have just dabbed.<br><br>
### /video [url] : passes a video URL to the bot, which will then download and convert to a Telegram compliant .mp4 and send to the chat followed by a message stating which user sent the video.<br><br>
### /roll : Without arguments this will roll 1d20 and announce to the chat that you have done this and what the result was.
* Arguments for /roll should be entered in the form of "/roll xdy" where x is the number of dice to roll, and y is the type of dice. For example "/roll 2d10" will announce to the chat that you are rolling 2 d10 dice and the total result of that roll.

### /start and /test : test commands to ensure bot is running or placeholders for troubleshooting.