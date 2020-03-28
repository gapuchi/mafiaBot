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
    install_requires=['discord.py'],
    packages=find_packages(),
)
