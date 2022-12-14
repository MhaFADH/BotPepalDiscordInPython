import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import tasks,commands

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)


class PepalToolbox:

    def __init__(self,username,password):
        self.username = username
        self.password = password

    def pepal_connect(self):
        idents = {'login' :self.username ,'pass' :self.password}
        login_url = 'url to login page'
        get_session = requests.Session()
        logToPepal = get_session.post(login_url, data = idents)

        return get_session

    def how_many_grades(self):
        grades_url = 'url to grades page'
        session = self.pepal_connect()
        page = session.get(grades_url)
        parsedPage = BeautifulSoup(page.text, "html.parser")
        grades_class = parsedPage.find_all(class_="note_devoir")
        page_td = grades_class[0].find_all("td")

        grades_counter = 0

        for classes in grades_class:
            if page_td[3].text != " ":
                grades_counter += 1

        return grades_counter

#######################SETTINGS######################
tools = PepalToolbox('Username','Password')
msg = "@everyone NOUVELLE NOTE DISPONIBLE SUR PEPAL "
old_counter = tools.how_many_grades()
#####################################################

@bot.event
async def on_ready():
    global tools
    print("Bot is ready !")
    check_for_new_grades.start()

@tasks.loop(minutes=5)
async def check_for_new_grades():
    global old_counter
    global tools
    global msg

    new_counter = tools.how_many_grades()
    if old_counter != new_counter:
        print("Nouvelle note !")
        old_counter = new_counter
        await bot.get_channel('Channel token').send(msg)
    else:
        print("Aucune nouvelle note !")



bot.run('Bot token')
