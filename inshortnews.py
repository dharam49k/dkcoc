import requests
import telebot # pyTelegramBotAPI library
import pyfiglet
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import time, os, sys, json
from termcolor import colored
import logging
import os
from telegram.ext import Updater, CommandHandler


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


print("\n")
banner = pyfiglet.figlet_format('DIALY-NEWS')
print(banner)
print("Welcome to Daily News posting bot for telegram! \n")



	
url = 'https://www.inshorts.com/en/read'
uClient = uReq(url)
page_html= uClient.read()
uClient.close()


Token = "1916990445:AAECyo4jMCeJPbjPQsKOOljGMjX5OWGv6nk"
chatid = "-1001213504018"
delay = 1000


page_soup = soup(page_html,"html.parser")

body_contain = page_soup.findAll("div",{"class":"card-stack"})
containers = body_contain[0].findAll("div",{"class":"news-card z-depth-1"})


filename = "news.txt"

#f = open(filename,"w", encoding='UTF-8')
#headers = "Headline, News_Content\n"
#f.write(headers)

filename = "news.txt"

news_details = []

def news_repeator(context):
    
    for container in containers :

        headline = container.a.span.text
        news_container =  container.findAll("div",{"itemprop":"articleBody"})
        news_content = news_container[0].text.strip()
        img_contain = container.findAll("span",{"itemprop":"image"})
        img_con = img_contain[0].meta['content']
        news_link = container.findAll("div",{"class":"read-more"})

        if len(news_link)==1 :
           news_links = news_link[0].a['href']
        else :
           news_links= "Link is not available"

        news_list = {
            'Headline': headline,
            'News_Content': news_content.replace("\"",""),
            'Image': img_con,
            'News_Link' : news_links
        }

        news_details.append(news_list)

        #print(news_list)

        with open(filename,"w", encoding='UTF-8') as wf:
            json.dump(news_details, wf)

        #f.write(List1 + List2.replace(",","") + "\n")

    wf.close()    
 
    print("\n----------News Coming--------------")

    
    with open(filename, 'r') as r:
        news = json.load(r)

        for i in news :

            context.bot.send_message(chatid, "\n\n" + i["News_Content"] +"\n\n" + i["News_Link"] )
            time.sleep(10)
           
    r.close()



updater = Updater(token=Token, use_context=True)
job_queue = updater.job_queue
dp = updater.dispatcher


job_queue.run_repeating(news_repeator, delay)

updater.start_polling()
updater.idle()

print("\n NEWS POSTED :) !!")		



		