from appdirs import AppDirs
import os


def check_token():
    app_name = "mafiarldiscordbot"
    app_author = "gapuchi"
    dirs = AppDirs(app_name, app_author)
    config_path = dirs.user_config_dir
    secrets_path = os.path.join(config_path, 'secrets')
    if not os.path.exists(secrets_path):
        os.makedirs(secrets_path)
        token_path = os.path.join(secrets_path, 'botToken')
        bot_token = input('Enter your bot token: ')
        f = open(token_path, "w")
        f.write(bot_token)
        f.close()
