from telegram.ext import Updater , CommandHandler , MessageHandler, Filters

import logging
import settings

from handlers import film, film_base, talk_to_me


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

#В файле settings будет API_KEY и PROXY
def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("film", film))
    dp.add_handler(CommandHandler("1", film_base, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    mybot.start_polling()
    mybot.idle()



if __name__=='__main__':
    main()
    