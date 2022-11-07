from discord.ext import commands
from threading import Thread
from pyboy import PyBoy
from pyboy import WindowEvent
from os.path import exists
import discord
import time
import datetime
import shutil

#Probably not the best solution

'''
The way the bot works is that the emulator runs on a seperate thread.
When the bot sees somebody wants to press a button, it changes one of the 
bools in the dictionary to True. The game loop checks the dictionary for when
one of the bools is True. When it detects a button is pressed, it sends input to the 
emulator and changes the button back to False. Rinse and repeat

It will save periodically, depenidng on what you set it to. IT WILL KEEP SAVING
WHILE THE PROGRAM IS ON. The save files weigh basically nothing, though
'''

#The string can be replaced with a path to any ROM you want
ROM = 'ROMs/Pokemon Red.gb'
#Self-explanatofdfry. In minutes
time_between_saves = 10

buttons = {
    'up': False,
    'down': False,
    'left': False,
    'right': False,
    'a': False, 
    'b': False,
    'start': False,
    'select': False,
    'restart': False
    }

bot_token = input("What is the bot's token ?\n")

channel_id = input("What is the ID of the channel you want the bot to monitor ?\n")

prefix = input("What prefix do you want to use ?\n")

if input("Are you reloading ? (y/n)") == 'y':
    buttons['restart'] = True

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command('help')

#The main loop. It creates a pyboy object and checks the dictionary in a loop
def game_loop():
    #Used to autosave on time
    timer = time.time()

    pyboy = PyBoy(ROM)
    while not pyboy.tick():
        try:
            if buttons['restart'] == True:
                pyboy.send_input(WindowEvent.STATE_LOAD)
                del buttons['restart']
        except:
            pass

        #THIS WILL KEEP SAVING FOREVER
        #The saves weigh bascially nothing, though
        if time.time() - timer >= (time_between_saves*60):
            save_dir = ROM + '.state'
            if exists(save_dir):
                split_dir = save_dir.split('/')
                target_dir = f"Saves/{datetime.datetime.now()} " + split_dir[-1]
                shutil.copy(save_dir, target_dir)

                pyboy.send_input(WindowEvent.STATE_SAVE)
            else:
                pyboy.send_input(WindowEvent.STATE_SAVE)
            
            print("Saved")
            timer = time.time()

        for key in buttons:
            if buttons[key] == True:
                click(pyboy, key_translator(key))
                buttons[key] = False

#If inputs are being missed, add a third tick in the function
#Might happen because of heavy use
def click(emul, buttons):
    press, release = buttons

    emul.send_input(press)
    emul.tick()
    #Having only one tick between press and release causes missed inputs occasionally
    emul.tick()
    emul.send_input(release)

#Pretend this isn't here
def key_translator(key):
    match key:
        case 'up':
            return (WindowEvent.PRESS_ARROW_UP, WindowEvent.RELEASE_ARROW_UP)
        case 'down':
            return (WindowEvent.PRESS_ARROW_DOWN, WindowEvent.RELEASE_ARROW_DOWN)
        case 'left':
            return (WindowEvent.PRESS_ARROW_LEFT, WindowEvent.RELEASE_ARROW_LEFT)
        case 'right':
            return (WindowEvent.PRESS_ARROW_RIGHT, WindowEvent.RELEASE_ARROW_RIGHT)
        case 'a':
            return (WindowEvent.PRESS_BUTTON_A, WindowEvent.RELEASE_BUTTON_A)
        case 'b':
            return (WindowEvent.PRESS_BUTTON_B, WindowEvent.RELEASE_BUTTON_B)
        case 'start':
            return (WindowEvent.PRESS_BUTTON_START, WindowEvent.RELEASE_BUTTON_START)
        case 'select':
            return (WindowEvent.PRESS_BUTTON_SELECT, WindowEvent.RELEASE_BUTTON_SELECT)

@bot.event
async def on_ready():
    print("ready")

#The help command
@bot.command()
async def help(ctx):
    msg = ctx.message

    await msg.channel.send(f""" ```
I am a bot for emulating Game boy with the ability to control it from chat.
I observe chat and relay commands back to the host in order to control the emulator

{prefix}help to see this
{prefix}press [a, b, start, select, up, down, left, right] to press a button in the emulator

Credit:
https://github.com/DvorakDwarf
@DwarflessDvorak on Twitter
HistidineDwarf#8927 on Discord 
Preferred method of communication is over Discord``` """)

#The command used in chat to press a button                
@bot.command(name='press')
async def press(ctx, command):
    if ctx.channel.id != int(channel_id):
        return
    else:
        for key in buttons:
            if command == key:
                print(key)
                buttons[key] = True

gameThread = Thread(target=game_loop)
gameThread.start()

bot.run(bot_token)