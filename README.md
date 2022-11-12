![GitHub](https://img.shields.io/github/license/hunar4321/life_code)

# Discord-Emulator
A discord bot that can be used to play any game boy game using the discord chat. The way the bot works is that the emulator runs on a seperate thread. When the bot sees somebody wants to press a button, it changes one of the bools in a dictionary to True. The game loop checks the dictionary for when one of the bools is True. When it detects a button is pressed, it sends input to the emulator and changes the button back to False. Rinse and repeat

It will save periodically, depenidng on what you set it to. The default is a save each 10 minutes. IT WILL KEEP SAVING THE ENTIRE TIME THE PROGRAM IS ON. The save files weigh basically nothing, though. You should delete older ones periodically

How to run it
-----------------

![Peek 2022-11-06 17-50](https://user-images.githubusercontent.com/96934612/200225062-4a32658e-388e-4e9a-a67f-b6c3e2d10cea.gif)

Put the path to your ROM in the relevant variable. Run observer.py to start the bot. It will ask you your token and the ID of the channel you want the bot to monitor for commands. After that it opens a window of the ROM running. Use {prefix}help to see a further description of the bot and what it does. Use {prefix}press [a, b, start, select, up, down, left, right] to press a button in the emulator. Somebody needs to screenshare the game window in the discord server for members to see anything

A more detailed description later. Contact me if you need help
Also tell me if you are planning on hosting an event with this bot, I wanna see it.

Do what you want with the code, but credit would be much appreciated. Contact info in the profile

It is not strcitly necessary, but I highly recommend naming the bot "The Observer" and giving it this pfp:
![EQ1p524U4AAAppn](https://user-images.githubusercontent.com/96934612/200225323-491c88e6-169c-4dc3-a62c-6c24bcf378c8.jpg)
