from selenium import webdriver
from time import sleep
from discord_webhook import DiscordWebhook, DiscordEmbed
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display

def advance():
    usr = driver.find_element(By.XPATH, '//*[contains(@id, "Catalog-react-component")]')
    cont = usr.find_element(By.XPATH, './div/div/div[{}]/div/div/div/div[2]/a'.format(1))
    #print("text : "+ cont.get_attribute("href"))
    new_data = collect_info(cont.get_attribute("href"))
    return(new_data)


def scrape_research_page(search_url):
    data = advance()
    return(data)

def collect_info(page_url):
    driver.get(page_url)
    try:
        desc = driver.find_element(By.XPATH, '//div[@itemprop="description"]').text
    except:
        desc = ""
    price = driver.find_element(By.XPATH, '//span[@itemprop="price"]').text#.split(" €")[0]
    try:
        image = driver.find_element(By.XPATH, '//img[@itemprop="image"]').get_attribute("data-src")
    except:
        image = "https://cdn2.sosav.fr/store/69876-large_default/camera-arriere-ipad-pro.jpg"
    try:
        size = driver.find_element(By.XPATH, "//*[contains(text(), 'Taille')]")
        size1 = size.find_element(By.XPATH, './..').text.split("TAILLE ")[1]
    except:
        size1 = "/"
    try:
        p = driver.find_element(By.XPATH, "//*[contains(text(), 'Emplacement')]")
        place = p.find_element(By.XPATH, './..').text.split("EMPLACEMENT ")[1]
    except:
        place = "/"
    try:
        s = driver.find_element(By.XPATH, "//div[contains(text(), 'État')]")
        state = s.find_element(By.XPATH, './..').text.split("ÉTAT ")[1]
    except:
        state = "/"
    return {"title" : driver.title, "desc" : desc, "size" : size1, "state" : state, "place" : place, "price" : price, "image" : image, "url" : page_url}

def research_and_scrape(query, price, end_page=2):
    start_page = 1
    if start_page == 1:
        # start first page
        page = 1
        search_url = 'https://www.vinted.fr/vetements?search_text=' + query.replace(' ', '%20') + "&price_to=" + str(price) + "&order=newest_first"
        driver.get(search_url)
        data = scrape_research_page(search_url)
    return (data)  # Everything went good

global driver
display = Display(visible=0,size=(1024,768))
display.start()
options = webdriver.FirefoxOptions()
options.add_argument("headless")
driver = webdriver.Firefox(options=options)

class Bot():
    def __init__(self):
        self.last = False

        #CONFIG :
        self.logs = True  #True pour activer les logs discord du bot et False pour désactiver
        self.nblogs = 10  #Logs toutes les combien de fois. (10 ici)

        #DISCORD
        self.wh = 'https://discord.com/api/webhooks/923727649904418847/0Gx8UFdoz2s51cofXPZjwLClw1J4jQLCkP6iMEUtemvEuX5RrdmjH2QMWLbQTev1Z_Bs'
        self.whlogs = 'https://discord.com/api/webhooks/923728138444365824/_yMcWI_qrBU8RM7KCrxuOlklu8PmbVp9TgP6V6acTOFz24FkUsVAEbMJ5KlEy8OyUcN7'

        #TELEGRAM
        self.token = '1474222921:AAELAQiydgFOn05cJvxVc44qVeK9WMsaS2k'
        self.id = '1041095687'

        #NE PAS MODIFIER.
        self.stores = {'pull ralph lauren' : [25], 'gilet ralph lauren' : [40],
                       'pull lacoste' : [30], 'pull champion' : [20], 'veste the north face' : [60]}

    def check(self):
        for i in self.stores:
            self.scraped_data = research_and_scrape(i, self.stores[i][0], end_page=1)
            #print(self.scraped_data)
            if len(self.stores[i]) > 1 and self.scraped_data["url"] not in self.stores[i]:
                print('\033[94m['+i.upper()+'] ',end='')
                print(f"\033[92m\033[1mNouvelle annonce ({self.scraped_data['title']} | {self.scraped_data['price']})")
                # DISCORD
                webhook = DiscordWebhook(url=self.wh)
                embed = DiscordEmbed(title=self.scraped_data["title"],
                                     url=self.scraped_data["url"],
                                     description=self.scraped_data["desc"], color=0x09b1ba)
                embed.set_image(url=self.scraped_data["image"])
                embed.add_embed_field(name='Prix : ', value=self.scraped_data["price"])
                embed.add_embed_field(name='Taille : ', value=self.scraped_data["size"])
                embed.add_embed_field(name='Lieu : ', value=self.scraped_data["place"])
                embed.add_embed_field(name='Etat : ', value=self.scraped_data["state"])
                embed.set_footer(text=f"Tourre#2884 | BETA | TAGS : {str([i for i in self.stores])[1:][:-1]}", icon_url='https://cdn.freelogovectors.net/wp-content/uploads/2021/06/vinted-logo-freelogovectors.net_.png')
                webhook.add_embed(embed)
                response = webhook.execute()

                # TELEGRAM
                self.mes = 'Vinted : '
                URL = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.id}&text={self.mes}"
                #dark = requests.get(URL)
            self.stores[i].append(self.scraped_data["url"])
open = True

bot = Bot()

webhook = DiscordWebhook(url=bot.whlogs)
embed = DiscordEmbed(title="BOT Started", description="Tags : "+', '.join(bot.stores), color=0x00b4bb)
embed.set_thumbnail(url="https://www.presse-citron.net/app/uploads/2020/06/vinted-logo.jpg")
embed.add_embed_field(name="Tourre#0001", value="v1.0", inline=False)

webhook.add_embed(embed)
response = webhook.execute()
v = 0
while open:
    print('[SYSTEM] CHECKING')
    v += 1
    if v%bot.nblogs == 0 and bot.logs:
        # DISCORD
        webhook = DiscordWebhook(url=bot.whlogs)
        embed = DiscordEmbed(title="LOGS",description="STILL RUNING : " + str(v)+' time.', color=0x00b4bb)
        embed.add_embed_field(name="Tourre#2884", value="v0.1", inline=False)
        embed.set_thumbnail(url="https://image.flaticon.com/icons/png/512/60/60473.png")
        webhook.add_embed(embed)
        response = webhook.execute()

    try:
        bot.check()
    except:
        pass
    sleep(10)
