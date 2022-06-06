from bs4 import BeautifulSoup
import requests as req
import re
import conf

### --------------------------------------------------- ###

token = conf.token
channel_id = conf.channel_id
url = "https://api.telegram.org/bot"
url += token
method = url + "/sendMessage"

ip_18 = conf.ip_18
ip_21 = conf.ip_21
ip_22 = conf.ip_22
ip_13 = conf.ip_13

ip_10 = conf.ip_10
ip_call = conf.ip_call

ip_kassa = conf.ip_kassa
ip_5 = conf.ip_5
ip_17 = conf.ip_17

fotoval = []
foto = []
col = 0
one_percent = 0.56

"""brother_print"""
cab_18 = [ip_18, '18 каб', 9]
cab_21 = [ip_21, '21 каб', 9]
cab_22 = [ip_22, '22 каб', 9]
cab_13 = [ip_13, '13 каб', 9]

"""brother_mfu"""
cab_10 = [ip_10, '10 каб', 8]
cab_call = [ip_call, 'КЦ', 8]

"""ricoh"""
kassa = [ip_kassa, "Касса"]
cab_5 = [ip_5, "5 каб"]
cab_17 = [ip_17, "17 каб"]
#pavelet = ["10.3.102.4", "Павелецкая проц"]

all_bro = [cab_18, cab_21, cab_22, cab_10, cab_call, cab_13]
all_ricoh = [kassa, cab_5, cab_17]

quest = "recep, 6, 16, 25" + "hp_pavelet, pavelet"

def check_brother(cab):
    try:
        req_ton = req.get("http://"+ cab[0] + "/general/status.html")
        soup_ton = BeautifulSoup(req_ton.text, 'lxml')
        toner_int = soup_ton.find('img', class_="tonerremain")['height']
        toner = round(int(toner_int)/one_percent)

        req_foto = req.get("http://" + cab[0] + "/general/information.html?kind=item")
        soup_foto = BeautifulSoup(req_foto.text, 'lxml')
        fotoval_strings = soup_foto.find_all('dd')
        fotoval_html = str(fotoval_strings[cab[2]])
        fotoval_proc=re.sub("[d|<|>|(|)|/|%]","",fotoval_html)
        fotoval = fotoval_proc.split('.')[0]

        if int(toner) < 20 or int(fotoval) < 20:
            r = req.post(method, data={
                "chat_id": channel_id,
                "text": "В " + str(cab[1]) + ' осталось ' + str(toner) + '% тонера и ' + str(fotoval) + '% фотобарабана'
            })
        else:
            print('В ' + str(cab[1]) + ' все норм')
    except:
        r = req.post(method, data={
            "chat_id": channel_id,
            "text": "Ошибка опроса " + cab[1]
        })

def check_ricoh(cab):
    try:
        resp_ton = req.get('http://' + cab[0] + '/main.asp?Lang=en-us')
        soup = BeautifulSoup(resp_ton.text, 'lxml')
        toner = soup.find('table', class_="toner")['width']
        toner=re.sub("%","",toner)

        if int(toner) < 20:
            r = req.post(method, data={
                "chat_id": channel_id,
                "text": "В " + str(cab[1]) + ' осталось менее ' + str(toner) + '% тонера'
            })
        else:
            print('В ' + str(cab[1]) + ' все норм')
    except:
        r = req.post(method, data={
            "chat_id": channel_id,
            "text": "Ошибка опроса " + cab[1]
        })        

#check_brother(cab_18)
for cab in all_bro:
    check_brother(cab)
for cab in all_ricoh:
    check_ricoh(cab)