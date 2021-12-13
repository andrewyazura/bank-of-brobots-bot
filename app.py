from brobank_bot import create_app

app = create_app()

if __name__ == "__main__":
    import os.path
    from telegram.ext import Updater

    updater = Updater(dispatcher=app.dispatcher, workers=None)

    if not os.path.isfile(".bot-started"):
        open(".bot-started", "w").close()
        updater.start_polling()

    app.run(debug=True)

    os.remove(".bot-started")
