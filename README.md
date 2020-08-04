# Rocket League Mafia Discord Bot

A discord bot to help you facilitate Mafia games on Rocket League

## The Rules

Inspired by [Sunless Khan's Rocket League Mafia](https://www.youtube.com/watch?v=nZjNx7UlqWY&t=628s).

Each player will be assigned a role, `Villager` or `Mafia`. The goal for `Villager`s is to win the Rocket League match while `Mafia` tries to lose the match, while doing their best to be undetected. At the end of the game, everyone votes on who is `Mafia`. `Mafia` is defeated if a plurality of votes are against him/her.

The points:

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
$mafia new <number of Mafia>
```

this will check your voice channel and split the members on the VC into the two teams. 

If you want to specify the players:

```
$mafia with <number of Mafia> @player1 @player2 @player3
```

This can also be used to generate teams, without mafia:

```
$game new
```

```
$game with @player1 @player2 @player3
```

## Install

The bot needs to run on your machine. The package is available in [PyPI](https://pypi.org/project/mafia-rl-discord-bot/) and can be installed via `pip`.

### What I did

This is what I did to set up the bot. (If you're comfortable with python, you can do whatever works for you.)

Set up a [virtual environment](https://docs.python.org/3/library/venv.html). (Note which directory you call this method, the environment will be in that location. I created a folder for the bot specifically.)

```
~/personalWorkspace/mafia_bot $ python3 -m venv env
~/personalWorkspace/mafia_bot $ source env/bin/activate
(env) ~/personalWorkspace/mafia_bot $
```

Installed the package

```
(env) ~/personalWorkspace/mafia_bot $ pip install mafia-rl-discord-bot
(env) ~/personalWorkspace/mafia_bot $ source env/bin/activate
```

Ran the package

```
(env) ~/personalWorkspace/mafia_bot $ mafia_rl_discord_bot 
```

If this is your first time, it will ask for your bot token

```
(env) ~/personalWorkspace/mafia_bot $ mafia_rl_discord_bot 
Enter your bot token: 
```

[Create a bot token](https://discordpy.readthedocs.io/en/latest/discord.html), and paste it here. It will be saved if you start it up in the future. Once entered, you should see:

```
Logged in as
<something>
<something>
------
```

You're good to go!

### Tear Down

To leave the environment

```
(env) ~/personalWorkspace/mafia_bot $ deactivate 
~/personalWorkspace/mafia_bot $ 
```

Once you leave the environment you cannot start the bot. The bot was only installed in the virtual environment.

```
~/personalWorkspace/mafia_bot $ mafia_rl_discord_bot
zsh: command not found: mafia_rl_discord_bot
```

To start it back up, you need to run the activate command wherever you set it up

```
~/personalWorkspace/mafia_bot $ source env/bin/activate
(env) ~/personalWorkspace/mafia_bot $
```

or

```
~ $ source ~/personalWorkspace/mafia_bot/env/bin/activate
(env) ~ $
```