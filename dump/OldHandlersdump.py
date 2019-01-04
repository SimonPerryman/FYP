# echo_handler = MessageHandler(Filters.text, conversations.echo)


# def caps(bot, update, args):
#     print("args:", args)
#     # print("update:", update)
#     text_caps = ' '.join(args).upper()
#     bot.send_message(chat_id=update.message.chat_id, text=text_caps)

# caps_handler = CommandHandler('caps', caps, pass_args=True)


# def customKeyboard(bot, update):
#     custom_keyboard = [['top-left', 'top-right', '7'], ['bottom-left', 'bottom-right', '7'], ['top-left', 'top-right', '7'], ['another-One']]
#     reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
#     bot.send_message(chat_id=update.message.chat_id, 
#                     text="Custom Keyboard Test", 
#                     reply_markup=reply_markup)


# keyboard_handler = CommandHandler('keyboard', customKeyboard)  

