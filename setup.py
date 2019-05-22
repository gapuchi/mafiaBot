#! /usr/bin/env python

from setuptools import setup

with open("README.md", encoding="utf-8") as f:
	readme = f.read()

setup(
	name='mafiabot',
	description='A discord bot to help you facilitate Mafia games on Rocket League',
	long_description=readme,
	long_description_content_type="text/markdown",
	url='https://github.com/gapuchi/mafiaBot',
	author='Arjun Adhia',

	version='0.1.0',
	install_requires=['discord'],
	scripts=['myBot.py']
)
