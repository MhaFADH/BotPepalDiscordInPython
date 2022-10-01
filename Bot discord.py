from asyncio import tasks
import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import tasks, commands

bot = discord.Client()

# test*

def cmb_note():
    identifiants = {'login':'','pass':''}

    login_url= 'https://www.pepal.eu/include/php/ident.php'

    session = requests.Session()

    login = session.post(login_url, data = identifiants)

    url = 'https://www.pepal.eu/?my=notes'

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


msg = "@everyone NOUVELLE NOTE DISPONIBLE SUR PEPAL "

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
        await bot.get_channel(887660675600621591).send(msg)
    else:
        print("non")


        

bot.run('OTkwNTk0ODUyOTAxMjI0NDQ4.GM8H3k.PXiqheM7m5GL_1sXi2LlHGMsSppKDcPrMFyLzw')