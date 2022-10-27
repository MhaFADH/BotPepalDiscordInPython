from asyncio import tasks
import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import tasks, commands

bot = discord.Client()

# test*

def cmb_note():
    identifiants = {'login':'','pass':''}

    login_url= 'ident page'

    session = requests.Session()

    login = session.post(login_url, data = identifiants)

    url = 'grade page'

    result = session.get(url)

    doc = BeautifulSoup(result.text, "html.parser")
    tab_note = doc.find_all(class_ = "note_devoir")
    tds = tab_note[0].find_all("td")

    # print(tds[3].text)

    nb_notes = 0

    for i in tab_note:
        if tds[3].text != " ":
            nb_notes += 1

    return nb_notes


notes_act = cmb_note()


msg = "@everyone NOUVELLE NOTE DISPONIBLE SUR **** "

@bot.event
async def on_ready():
    print("ready to go")
    checkfornewnotes.start()


@tasks.loop(minutes=30)
async def checkfornewnotes():
    global notes_act
    if notes_act != cmb_note():
        print("oui")
        notes_act += 1
        await bot.get_channel().send(msg)
    else:
        print("non")


        

bot.run('bot token')
