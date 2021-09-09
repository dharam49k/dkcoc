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
from colorama import init


init()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

print("\n")
my_url = input("Enter Your Url which one to scarp :")

print("\n")

print("Url is : " + my_url)

uClient = uReq(my_url)
page_html= uClient.read()
uClient.close()

page_soup = soup(page_html,"html.parser")

Token = "1929419642:AAHjp8xbxPCe4pyUr_bCO3rHFNHSVruoyJ0"
chatid = "-1001515138028"
delay = 30

filename= "octa_profile.txt"

re = "\u001b[31;1m"
gr = "\u001b[32m"
ye = "\u001b[33;1m"  

print(gr+"Welcome\n")

def news_repeator(context):

    re = "\u001b[31;1m"
    gr = "\u001b[32m"
    ye = "\u001b[33;1m"

    uClient = uReq(my_url)
    page_html= uClient.read()
    uClient.close()

    page_soup = soup(page_html,"html.parser")
    
    body_contain = page_soup.body.findAll("script")[8].string

    data = body_contain.strip()[16368:-183].replace("'" , '"')

    profile_data = json.loads(data)

    #print(profile_data)

    with open(filename,"w", encoding='UTF-8') as wf:
        json.dump(profile_data, wf)
    wf.close()

    with open(filename, 'r') as r:
        profile = json.load(r)   

    # context.bot.send_message(chatid, "Profile Detail :-->\n" + " Name :" + profile['profileProps']['master']['nickname'] + "\n" +

    #                             "Equity :" + profile['profileProps']['equity'] + "\n" +

    #                             "Float Profit :" + profile['accountDetailsProps']['floatingProfitCurrency'] + "\n" +

    #                             "Total Balance :" + profile['accountDetailsProps']['balance'] + "\n" +

    #                             "Open Trade No :" + str(profile['historyProps']['openTradesCount'] ))
    print("\n")
    print("Profile Detail :\n" + ye+"Name :" + re+profile['profileProps']['master']['nickname'] + "\n" +

                                ye+"Equity :" + re+profile['profileProps']['equity'] + "\n" +

                                ye+"Float Profit :" + re+profile['accountDetailsProps']['floatingProfitCurrency'] + "\n" +

                                ye+"Total Balance :" + re+profile['accountDetailsProps']['balance'] + "\n" +

                                ye+"Open Trade No :" + re+str(profile['historyProps']['openTradesCount'] )) 

    print(gr+"\n")
updater = Updater(token=Token, use_context=True)
job_queue = updater.job_queue
dp = updater.dispatcher


job_queue.run_repeating(news_repeator, delay)

updater.start_polling()
updater.idle()


		