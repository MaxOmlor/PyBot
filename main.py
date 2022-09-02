import Constants
import Responses
import telegram.ext as te


print('Bot is running...')

updater = te.Updater(Constants.API_KEY, use_context=True)
dp = updater.dispatcher

dp.add_handler(te.CommandHandler('help', Responses.handle_help))
dp.add_handler(te.CommandHandler('namespace', Responses.handle_namespace))

dp.add_handler(te.MessageHandler(te.Filters.text, Responses.handle_msg))
dp.add_error_handler(Responses.error)

update_queue = updater.start_polling(timeout=10)
#updater.idle()

while True:
    text = input()

    # Gracefully stop the event handler
    if text == 'stop':
        update_queue.put('bot stopped.')
        updater.stop()
        break

print('Bot closed')
