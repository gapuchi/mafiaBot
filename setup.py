#! /usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name='mafia-rl-discord-bot',
    description='A discord bot to help you facilitate Mafia games on Rocket League',
    long_description=readme,
    long_description_content_type="text/markdown",
    url='https://github.com/gapuchi/mafiaBot',
    author='Arjun Adhia',
    author_email='arjun.adhia@gmail.com',

    version='0.0.1',

    install_requires=['discord.py', 'appdirs'],
    python_requires='>=3.7',
    packages=['mafia_rl_discord_bot'],
    package_data={'mafia_rl_discord_bot': ['config/*.json']},

    entry_points={'console_scripts': ['mafia_rl_discord_bot=mafia_rl_discord_bot.discord_bot:run_bot']}
)
