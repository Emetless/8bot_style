from time import sleep

import requests
import logging

from PIL import Image
from telegram.ext import Updater, RegexHandler, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, update

# Enable logging
import PictureProcessor

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

PHOTO, RESOLUTION, COLOR = range(3)



def start(bot, update):
    update.message.reply_text(
        'Привет,  я 8 битный бот'
        'Отправь /cancel для того чтобы меня остановить.\n\n'
        'Отправь мне фотографию и я её  изменюю'
        'для лучшего качества отправь картиннку файлом')
    return PHOTO


def photo(bot, update):
    reply_keyboard = [['Не сжатое', 'Среднее сжатие', 'Сильное сжатие']]

    user = update.message.from_user
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    photo_file.download('temp.jpg')
    logger.info("Photo of %s: ", user.first_name)
    update.message.reply_text('Окей, теперь выбери разрешение будущего изображения',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return RESOLUTION


def document(bot, update):
    reply_keyboard = [['Не сжатое', 'Среднее сжатие', 'Сильное сжатие']]

    user = update.message.from_user
    photo_file = bot.get_file(update.message.document.file_id)
    photo_file.download('temp.jpg')
    logger.info("Photo of %s: ", user.first_name)
    update.message.reply_text('Окей, теперь выбери разрешение будущего изображения',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return RESOLUTION


def resolution(bot, update):
    reply_keyboard = [['черно-белое', 'Геймбой', 'Apple 2', 'отенки серого']]

    user = update.message.from_user
    global resol
    resol = update.message.text
    logger.info("Resolution set %s: %s", update.message.text, resol)
    update.message.reply_text('А теперь выбери цветовую гамму',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return COLOR


def showResult(bot, update):
    user = update.message.from_user
    image = Image.open('temp.jpg')
    print(resol)
    re = 1
    if resol == 'Не сжатое':
        re = 1
    elif resol == 'Среднее сжатие':
        re = 8
    elif resol == 'Сильное сжатие':
        re = 16
    print(re)
    worker = PictureProcessor.PictureProcessor(image, re, update.message.text)
    worker.Pixilizer()
    image.save("ans.jpeg", "JPEG")
    worker.Colorer()
    del worker
    image.save("fin.jpeg", "JPEG")
    del image
    bot.send_photo(chat_id=update.message.chat_id, photo=open('ans.jpeg', 'rb'))
    bot.send_photo(chat_id=update.message.chat_id, photo=open('fin.jpeg', 'rb'))
    bot.send_document(chat_id=update.message.chat_id, document=open('ans.jpeg', 'rb'))
    bot.send_document(chat_id=update.message.chat_id, document=open('fin.jpeg', 'rb'))
    logger.info("Return process photo %s: ", update.message.text)
    update.message.reply_text('Лови свои фотографии'
                              'Если хочешь  отправить еще нажми /start',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""

    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # REQUEST_KWARGS = {
    #     'proxy_url': 'http://62.210.149.33:10534/'    прокся которая не нужна
    #
    # }

    updater = Updater("TOKEN" )
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={

            PHOTO: [MessageHandler(Filters.photo, photo),
                    MessageHandler(Filters.document, document)],

            RESOLUTION: [RegexHandler('^(Не сжатое|Среднее сжатие|Сильное сжатие)$', resolution)],

            COLOR: [RegexHandler('^(черно-белое|Геймбой|Apple 2|отенки серого)$', showResult)]

        },

        fallbacks=[CommandHandler('cancel', cancel)]

    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.

    updater.idle()


if __name__ == '__main__':
    main()
