# Rocket League Mafia Discord Bot

A discord bot to help you facilitate Mafia games on Rocket League

## The Rules

Each player will be assigned a role, `Villager` or `Mafia`. The goal for `Villager`s is to win the Rocket League match while `Mafia` tries to lose the match, while doing their best to be undetected. At the end of the game, everyone votes on who is `Mafia`. `Mafia` is defeated if a plurality of votes are against him/her.

The default points are:

| Villager | Points |
|---|---|
| Wins the game | 1 |
| Correctly guesses mafia | 1 |
| Kill the mafia | 2 |

| Mafia | Points |
|---|---|
| Loses the game | 2 |
| Not killed | 1 |
| Has no votes against | 2 |
| Wins the game | x0 |

## How To

All commands can be viewed with `$help`.

In order to start a new game:

```
$new <number of Mafia> <player1> .... <player n>
```

## Install

In order to run the bot, execute the python file, `myBot.py`. In order to have it running in your server, you need to have a discord bot, with its token in `./secrets/botToken`.