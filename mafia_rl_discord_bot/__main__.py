#!/usr/bin/python

from mafia_rl_discord_bot.check_token import check_token
from mafia_rl_discord_bot.discord_bot import run_bot


def main():
    check_token()
    run_bot()


if __name__ == "__main__":
    main()
