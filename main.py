from emoji import UNICODE_EMOJI
from time import sleep
import ast
from html.parser import HTMLParser
from collections import Counter
import re
import shutil
import mysql.connector

import os
import requests

import telebot
from threading import Thread
import datetime
from rough2 import analyse
from telebot import types
import pytesseract
from PIL import Image
from pdf_crop import downloadPdf, cropPdf, dividePdf
from kit import divideChat, mergePdf, sieve, mergePdf2

auth = 'a193a994-019d-450c-8a95-26aef1690afc'
app_name = 'chand-tara1'
info_data = {}


class MyHTMLParser(HTMLParser):
    def __init__(self, lst):
        super().__init__()
        self.allData = lst
    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for i in attrs:
                if i[0] == 'src':
                    k = i[1].split('/')[-1] + ' (file attached)'
                    self.allData.append(k)

    def handle_data(self, data):
        self.allData.append(data)
        # print("Encountered some data  :", data)
#detect the running app
HEADERS = {
            "Accept": "application/vnd.heroku+json; version=3",
            "Authorization": f'Bearer {auth}'
        }

url = f"https://api.heroku.com/apps/{app_name}/dynos/worker.1"

result = requests.get(url, headers=HEADERS)
print(result)


if str(result) in ['<Response [200]>','<Response [201]>','<Response [202]>','<Response [206]>']:
    running_app = 'chand-tara1'
    sleeping_time ='160000'
    sleeping_app = 'chand-tara2'
else:
    running_app = 'chand-tara2'
    sleeping_app = 'chand-tara1'
    sleeping_time = '010000'


def restart():
    # APP = 'baghin2'
    PROCESS = 'worker.1'
    HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/vnd.heroku+json; version=3",
        "Authorization": f'Bearer {auth}'
    }
    url = "https://api.heroku.com/apps/" + running_app + "/dynos/" + PROCESS

    print(url)
    result = requests.delete(url, headers=HEADERS)
    print(result)
    print(result.content)
    

try:
    url = 'https://www.dropbox.com/s/5f8enws2wipbrjb/pricing.png?dl=1'
    r = requests.get(url, allow_redirects=True)
    open('pricing.png', 'wb').write(r.content)
except:
    pass


def changeDyno():
    # turn on sleeping app
    payload = {'quantity': 1}
    url = "https://api.heroku.com/apps/" + sleeping_app + "/formation/worker"
    result = requests.patch(url, headers=HEADERS, data=payload)

    # turn off running app
    payload = {'quantity': 0}
    url = "https://api.heroku.com/apps/" + running_app + "/formation/worker"
    result = requests.patch(url, headers=HEADERS, data=payload)


def scheduler():
        while True:
            time = datetime.datetime.now().strftime('%d%H%M')
            if time == sleeping_time:
                changeDyno()
                print('done')
            sleep(1)

Thread(target=scheduler, args=()).start()



TOKEN = '5186507750:AAH4_xds21DEcDkui3OR5QZ75JyQZntuqZ4'
TOKEN2 = '5577708184:AAHR7BlxQtbBz5848_ejzJ7-MCz8Vd72-yc'
TOKEN = TOKEN2
# TOKEN2 = '2025314077:AAHaS5N98O5mWiKztJena2j62f7R2p8YLAk'
bot = telebot.TeleBot(TOKEN)
bot2 = telebot.TeleBot(TOKEN2)
msg5k = 15
msg10k = 25
msg20k = 35
msg40k = 50
price_image = 'pricing.png'
#price_image = 'pricing.jpg'

#HOST = 'remotemysql.com'
#USER = 'Iiz39S07Z0'
#PASS = 'DSRHc6wWK2'
#DATABASE = 'Iiz39S07Z0'

HOST = 'bquwvep8bplhl7fmivr8-mysql.services.clever-cloud.com'
USER = 'upjrz6vokfdkcteg'
PASS = 'qZfWJoz0WzMs9EYxlNqb'
DATABASE = 'bquwvep8bplhl7fmivr8'


#MYID = 5022660886 #new
MYID = 2040144251
ANUID = 1882806632
#ANUID = 5022660886 #ravi

print('sent')
bot.send_message(MYID, f'Bot Started\n{running_app}')
#bot.send_document(MYID, data=open(f'kit.py', 'rb').read(), document=None)
print('Started')

mydb = mysql.connector.connect(
    host=HOST,
    database=DATABASE,
    user=USER,
    password=PASS
)
mycursor = mydb.cursor(buffered = True)

def ping():
    if not mydb.is_connected():
        mydb.reconnect(attempts=10, delay=10)


def addVisitor(chat_id, name):
    ping()
    sql = "INSERT INTO data (id, name) VALUES (%s, %s)"
    val = (chat_id, name)
    mycursor.execute(sql, val)
    mydb.commit()


def read_img(img_name):
    img = Image.open(img_name)
    pytesseract.pytesseract.tesseract_cmd = './.apt/usr/bin/tesseract'
    text = pytesseract.image_to_string(img)
    return(text)


def getVisitor():
    ping()
    mycursor.execute("SELECT id from data")
    data = mycursor.fetchall()
    allVisitors = [i[0] for i in data]
    return allVisitors

visitors = getVisitor()

def checkVisitor(msg):
    ping()
    mycursor.execute("SELECT id from data")
    data = mycursor.fetchall()
    allVisitors = [i[0] for i in data]
    # print(allVisitors)
    # print(type(msg))
    if msg.chat.id not in allVisitors:
        name = str('' if msg.from_user.first_name is None else msg.from_user.first_name) + \
               str('' if msg.from_user.last_name is None else ' ' + msg.from_user.last_name)
        try:
            addVisitor(msg.chat.id, name)
        except:
            addVisitor(msg.chat.id, 'unnamed')

def getUserNum():
    ping()
    mycursor.execute("SELECT id from data")
    data = mycursor.fetchall()
    allVisitors = [i[0] for i in data]
    return len(allVisitors)

def getRemainingCredit(id):
    ping()
    mycursor.execute(f"SELECT remaining FROM data WHERE id={id}")
    data = mycursor.fetchall()
    # print(data, data[0][0])
    remainingCredit = int(data[0][0])
    return remainingCredit

def getCredit(id):
    ping()
    mycursor.execute(f"SELECT credit FROM data WHERE id={id}")
    data = mycursor.fetchall()
    # print(data, data[0][0])
    credit = int(data[0][0])
    return credit


def getUsedCredit(id):
    ping()
    mycursor.execute(f"SELECT used FROM data WHERE id={id}")
    data = mycursor.fetchall()
    # print(data, data[0][0])
    used = int(data[0][0])
    return used


def updateRemainingCredit(id, value):
    ping()
    sql = f"UPDATE data SET remaining = {value} WHERE id ={id}"
    mycursor.execute(sql)
    mydb.commit()


def addCredit(id, value):
    ping()
    mycursor.execute(f"SELECT credit FROM data WHERE id={id}")
    data = mycursor.fetchall()
    # print(data, data[0][0])
    credit = int(data[0][0])
    sql = f"UPDATE data SET credit = {value+credit} WHERE id ={id}"
    mycursor.execute(sql)
    mydb.commit()
    a = getRemainingCredit(id)
    sql = f"UPDATE data SET remaining = {value + a} WHERE id ={id}"
    mycursor.execute(sql)
    mydb.commit()


def addUsedCredit(id, value):
    ping()
    mycursor.execute(f"SELECT used FROM data WHERE id={id}")
    data = mycursor.fetchall()
    # print(data, data[0][0])
    credit = int(data[0][0])
    sql = f"UPDATE data SET used = {value + credit} WHERE id ={id}"
    mycursor.execute(sql)
    mydb.commit()


def getName(id):
    ping()
    mycursor.execute(f"SELECT name FROM data WHERE id={id}")
    data = mycursor.fetchall()
    # print(data, data[0][0])
    name = data[0][0]
    return name


def extract_emojis(s):
    if s == None:
        return []
    return [c for c in s if c in UNICODE_EMOJI.keys()]


def make(textFile=None, id=None, admi = None):
    try:

        info_dict = info_data[id]
        print(info_dict)
        textFile = info_dict['fileName']
        theme = info_dict['theme']
        me = info_dict['me']
    except Exception as e:
        print(e)
        bot.send_message(id,
                         'Please export your chat again. If you want to add a background, send an Image before exporting the chat.')
        return 0

    if textFile is None:
        try :
            textFile = open(f'{id}/fileName', 'r').read()
        except:
            bot.send_message(id, 'Please export your chat again. If you want to add a background, send an Image before exporting the chat.')
            return 0
    raww, users, _me, divided_chats, emojiList = sieve(f'{id}/{textFile}')
    
    if len(divided_chats) == 0:

        bot.send_message(id, "Can't process because of unmatched text formatting. We are working for other countries' format and would support your text file format in near future.")

        bot2.send_message(MYID, 'INCORRECT FORMAT')
        return None
    
    if len(raww) < 25 : 
        bot.send_message(id, 'Your chat is too small to process.\n\nPlease export other chat.')
        return None
    
    if 0 < len(raww) <= 1250: amount = 0
    elif 1250 < len(raww) <= 5000: amount = msg5k
    elif 5000 < len(raww) <= 10000: amount = msg10k
    elif 10000 < len(raww) <= 20000: amount = msg20k
    elif 20000 < len(raww) <= 50000: amount = msg40k
    else: amount = 100
    remainingCredit = getRemainingCredit(id)
    if 0 < remainingCredit < amount:
        bot.send_message(id, f'You have Rs. {remainingCredit} as Credit. Rs. {amount} is needed to make pdf of {len(raww)} messages chat.')
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        a = types.InlineKeyboardButton(text='Get Payment Info', callback_data='payinfo')
        keyboard.add(a)
        bot.send_message(id, '👇', reply_markup=keyboard)
        bot.send_message(id, f'For more info, contact @raviarya131')
        return 0

    
    print(users, me)
    dirToCopy = ['icons', 'emojies']
    print(dirToCopy)
    fileToCopy = ['block.png', 'bc.jpg', 'img.png']
    for di in dirToCopy:
        if not os.path.exists(f'{id}/{di}'):
            shutil.copytree(di, f'{id}/{di}')
    for f in fileToCopy:
        shutil.copyfile(f, f'{id}/{f}')
    shutil.copyfile(f'theme/theme{theme}/bg.PNG', f'{id}/bg.png')
    shutil.copyfile(f'theme/theme{theme}/style.css', f'{id}/style.css')
    print('files copied')
    # fileNames = divideChat(textFile)
    message = bot.send_message(id, 'Processing your files.')
    sleep(15)
    if me == None:
        me = admi
    if me == None:
        
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for taika in users:
            a = types.InlineKeyboardButton(text=taika, callback_data=f'user_{taika}')
            keyboard.add(a)
        
        bot.send_message(id, 'Which one is you?', reply_markup=keyboard)
        return 0
       # abcdefghi = users
       # abcdefghi.sort(key=len)
       # me = abcdefghi[1]

    count = 0

    message = bot.send_message(id, 'Progress: ░░░░░░░░░░ 0%')
    if remainingCredit >= amount and amount > 0:
        message2 = bot.send_message(MYID, 'Progress: ░░░░░░░░░░ 0%')
    # sleep(20)
    if remainingCredit >= amount and amount > 0:
        try:
            #analyse(f'{id}/{textFile}')

            bot.send_document(id, data=open(f'z.png', 'rb').read(), document=None,
                               visible_file_name='Chat Analysis (Free).png')
            bot2.send_document(MYID, data=open(f'z.png', 'rb').read(), document=None,
                              visible_file_name='Chat Analysis (Free).png')
            os.remove('z.png')
        except Exception as e:
            print("Couldn't analyse")
            print(e)
    users3 = users
    users3.sort(key=len)
    me2 = me
    if me2 == None: me2 = users[0]
    users3.remove(me2)
    other = users3[0]
    print(other.upper().replace('PNG', 'png').replace('EMOJIES', 'emojies'))
    #print(message.message_id)
    for divided_chat in divided_chats:
        #print(message.message_id)
        count = count + 1
        print(f'{count}/{len(divided_chats)}')
        progress = int(((count/len(divided_chats))*100)//10)
        toSend = 'Progress: ' + '█' * progress + '░' * (10 - progress) + f'  {count}/{len(divided_chats)}'
        #bot.send_message(id, f'{count}/{len(divided_chats)}')

        message = bot.edit_message_text(toSend, id, message.message_id)
        if remainingCredit >= amount and amount > 0 :
            message2 = bot.edit_message_text(toSend, MYID, message2.message_id)
        data = divided_chat
        users2 = users
        for i in range(len(users2)):
            em = extract_emojis(users2[i])
            if len(em) > 0:
                for j in em:
                    ucode = 'U+{:X}'.format(ord(j))
                    if j in users2[i]:
                        users2[i] = users2[i].replace(j, fr'<img class="emoji" src="emojies\\{ucode}.png">')

        em = extract_emojis(me)
        if len(em) > 0:
            for j in em:
                ucode = 'U+{:X}'.format(ord(j))
                if j in me:
                    me = me.replace(j, fr'<img class="emoji" src="emojies\\{ucode}.png">')

        # print(me)

        for i in range(len(data)):
            em = extract_emojis(data[i][3])
            # print(em)
            if len(em) > 0:
                # print(em)
                for j in em:
                    ucode = 'U+{:X}'.format(ord(j))
                    if j in data[i][3]:
                        data[i][3] = data[i][3].replace(j,
                                                        fr'<img class="emoji" src="emojies\\{ucode}.png">')

            em = extract_emojis(data[i][2])
            # print(em)
            if len(em) > 0:
                # print(em)
                for j in em:
                    ucode = 'U+{:X}'.format(ord(j))
                    if j in data[i][2]:
                        data[i][2] = data[i][2].replace(j,
                                                        fr'<img class="emoji" src="emojies\\{ucode}.png">')

        # print(data)

        with open(f'{id}/index2.html', 'w', encoding='utf-8') as html:
            html.write(r'''<!DOCTYPE html>
        <html>
        <head>
        <title>''' + str(count) + '''</title>
        <link rel="stylesheet" href="style.css">

        </head>
        <body>
        <div class="page-footer"></div><div class="page-header"></div>
        <div class = 'front'>
         <img class='bg' src="bg.png">
         <p class ='title'>'''+me2.upper().replace('PNG', 'png').replace('EMOJIES', 'emojies')+'''</p>
         <p class ='and'>and</p>
         <p class ='title2'>'''+other.upper().replace('PNG', 'png').replace('EMOJIES', 'emojies')+'''</p>
         <p class ='subtitle'>WHATSAPP CHATBOOK</p>
      </div>
      
    <table><thead>
      <tr>
        <td>
          <!--place holder for the fixed-position header-->
          <div class="page-header-space"></div>
        </td>
      </tr>
    </thead>

    <tbody><tr><td>
        <div class="container">
            <ul>''')
            date = ''
            name = ''
            for line in data:

                if True:
                    time, msg = line[1], line[3]

                    if msg.startswith('This message was deleted') or msg.startswith('You deleted this message'):
                        msg = f'<span class="deleted"><img class ="emoji2" src="block.png">{msg}</span>'

                    if msg.startswith('<Media omitted>'):
                        msg = f'<span class="deleted"><img class ="emoji2" src="block.png">Media omitted</span>'

                    # if msg.startswith('https://') or msg.startswith('http://') or msg.startswith('www.'):
                    #     msg = f"<a href='{msg}'>{msg}</a>"

                    files = ['pdf', 'doc', 'txt', 'zip', 'ppt', 'mpg', 'ai', 'apk', 'html', 'avi']
                    if '(file attached)' in msg and not (
                        msg.endswith('webp (file attached)') or msg.endswith('jpg (file attached)') or msg.endswith(
                        'mp4 (file attached)') or msg.endswith('png (file attached)') or msg.endswith(
                        'gif (file attached)')):
                        # print('file: ' + msg)
                        # print(msg.endswith('webp (file attached)'))

                        ext = (msg.split('.')[1]).split(' ')[0]
                        inte = msg.split('.')[0] if len(msg.split('.')[0]) < 15 else msg.split('.')[0][:12] + '...'
                        # print(ext, inte)
                        # input()
                        if ext in files:
                            msg = f"""<div class='abc'> <a href ='{msg.split('.')[0] + "." + ext}'><div class="file" >
                                        <img class="fileicon" src="icons\\{ext}.png">

                                    <span class="filetext">{inte + "." + ext}</span></div></a></div>"""
                        else:
                            msg = f"""<div class='abc'> <a href ='{msg.split('.')[0] + "." + ext}'><div class="file" >
                                        <img class="fileicon" src="icons\\file.png">

                                    <span class="filetext">{inte + "." + ext}</span></div></a></div>"""
                    if not date == line[0]:
                        date = line[0]
                        html.write(r"<li class = 'date'>" + date + r"</li>")

                    if not name == line[2]:
                        name = line[2]
                        if name == me:
                            x = "'me'"
                        else:
                            x = "'him " + str(users2.index(name)) + "'"
                        #print(msg)
                        #print([msg])
                        #input()
                        if msg.endswith('jpg (file attached)') or msg.endswith(
                            'png (file attached)') or msg.endswith(
                            'gif (file attached)') or msg.endswith('webp (file attached)'):
                            #print('yeas')
                            # print(msg)
                           # input()

                            #
                            msg = msg.split()[0]
                            html.write(r"""<div class='abc'>
                                <li  class=""" + x + r"><div class= 'name'>" + name + r"""</div> 
                                    <ul>
                                        <li><img src= '""" + msg + r"""' alt=""" + msg + """   onerror="this.style.display='none'" ></li>
                                        <li class='time1'>""" + time + r"""</li>
                                        <li class="back"></li>
                                    </ul>
                                </li></div>""")

                        elif msg.endswith('mp4 (file attached)'):
                            msg = msg.split()[0]
                            html.write(
                                "<div class='abc'>    <li class=" + x + f"""><div class= 'name'>""" + name + f"""</div> 
                                                    <ul>
                                                        <li><video controls>
                                                            <source src="{msg}" type="video/mp4">
                                                            Your browser does not support the video tag.
                                                            </video></li>
                                                        <li class='time1'>""" + time + """</li>
                                                        <li class="back"></li>
                                                    </ul>
                                                </li></div> 
                                                """)

                        else:

                            html.write(r"""<div class='abc'>
                                <li  class=""" + x + r"><div class= 'name'>" + name + r"""</div> 
                                    <ul>
                                        <li class='msg'>""" + msg + r"""</li>
                                        <li class='time2'>""" + time + r"""</li>
                                    </ul>
                                </li></div>""")

                    else:
                        if name == me:
                            x = "'me2'"
                        else:
                            x = "'him2 " + str(users2.index(name)) + "'"
                        if msg.endswith('jpg (file attached)') or msg.endswith(
                            'png (file attached)') or msg.endswith(
                            'gif (file attached)') or msg.endswith('webp (file attached)'):
                            msg = msg.split()[0]
                            html.write("<div class='abc'>    <li class=" + x + """>
                                                    <ul>
                                                        <li><img src= '""" + msg + r"""' alt=""" + msg + """ onerror="this.style.display='none'" ></li>
                                                        <li class='time1'>""" + time + """</li>
                                                        <li class="back"></li>
                                                    </ul>
                                                </li></div> 
                                                """)
                            # html.write(r"<li class=" + x + "><img src='" + msg + "'> </li>   \n")
                            # html.write("<li class='time1'>"+time+"</li>")
                        elif msg.endswith('mp4 (file attached)'):
                            msg = msg.split()[0]
                            html.write(" <div class='abc'>   <li class=" + x + f""">
                                                    <ul>
                                                        <li><video controls>
                                                            <source src="{msg}" type="video/mp4">
                                                            Your browser does not support the video tag.
                                                            </video></li>
                                                        <li class='time1'>""" + time + """</li>
                                                        <li class="back"></li>
                                                    </ul>
                                                </li> </div>
                                                """)

                        else:
                            html.write(" <div class='abc'>   <li class=" + x + """>
                                                    <ul>
                                                        <li class='msg'>""" + msg + """</li> 
                                                        <li class='time2'>""" + time + """</li>
                                                    </ul>
                                                </li> </div>
                                                """)
                            # html.write(r"<li class=" + x + "><div class='msg'>" + msg + "</div> </li>   \n")
                            # html.write("<li class='time2'>"+time+"</li>")

            html.write(r'''</ul></div></td></tr></tbody>
<tfoot>
    <tr><td><div class="page-footer-space"></div></td></tr></tfoot>
    </table></body></html>''')

            #convertPdf(count)
            #jjj(count)
            
        downloadPdf(count, id)
        print('downloaded')
        sliceName = cropPdf(f'{id}/temp2.pdf', count, id)

        if remainingCredit == 0 and len(divided_chats) > 1:
                dj = mergePdf2(sliceName, id)
                bot.send_document(id, data=open(dj, 'rb').read(), visible_file_name='Sample Chat.pdf', document=None)
                bot2.send_document(MYID, data=open(dj, 'rb').read(), visible_file_name='Sample Chat.pdf',
                                  document=None)
                bot.send_message(id, 'This is a sample file. To make pdf of your full chat, you need to pay the below amount. \n\nYou will also get a free Chat Analysis if the chat is older than 4 months.')
                bot.send_message(id, f'No. of Messages : {len(raww)}\nAmount to be paid : Rs. {amount}')
                bot.send_message(MYID, f'{id}\nNo. of Messages : {len(raww)}\nAmount to be paid : Rs. {amount}')
                #bot.send_message(id, 'You w')
                bot.send_photo(id, photo=open(price_image, 'rb'))
                #bot.send_photo(id, photo=open('pricing.png', 'rb'))
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                #a = types.InlineKeyboardButton(text='Get Payment Info', callback_data='payinfo')
                #keyboard.add(a)
                #bot.send_message(id, '👇', reply_markup = keyboard)
                os.remove(sliceName)
                
                
                bot.send_message(id, 'You can pay through \nUPI ID : 9060038852@paytm\nName : Anurag Kumar')

                bot.send_message(id,

                                 'After making payment, send the screenshot of payment to @raviarya131. After confirmation of payment, '
                                 'you will receive your full pdf chat file in this bot.')
                #bot.send_message(idc, 'Confirmation of payment may take some time.')
                bot.send_message(id, f'{int(getUserNum()) + 910} users have already used the bot.')
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                a = types.InlineKeyboardButton(text=f'{msg5k}', callback_data=f'paid_{msg5k}_{id}')
                b = types.InlineKeyboardButton(text=f'{msg10k}', callback_data=f'paid_{msg10k}_{id}')
                c = types.InlineKeyboardButton(text=f'{msg20k}', callback_data=f'paid_{msg20k}_{id}')
                d = types.InlineKeyboardButton(text=f'{msg40k}', callback_data=f'paid_{msg40k}_{id}')
                keyboard.add(a, b, c, d)
                bot.send_message(MYID, f'ID : {id}\nName : {getName(id)}', reply_markup=keyboard)
                bot.send_message(ANUID, f'ID : {id}\nName : {getName(id)}', reply_markup=keyboard)
                
                return 0

    print('Creating Pdf')
    bot.send_message(id, 'Creating Pdf')
    mergePdf(count, id)
    print(f'{count} files merged')
    bot.send_message(id, 'Sending File')
    bot2.send_message(MYID, 'Sending File')
    print('done')
    sleep(2)
    size = os.path.getsize(f'{id}/chat.pdf')/1024/1024
    print(size)
    if size > 45:
        bot.send_message(id, 'Created File is too long to send.')
        bot2.send_message(MYID, 'Created File is too long to send.')
        bot.send_message(id, 'Dividing Pdf')
        names = dividePdf(id)
        tk = 0
        for n in names:
            tk = tk +1
            size = os.path.getsize(n)/1024/1024
            bot2.send_message(MYID, str(size)+' mb')
            bot.send_document(id, data=open(n, 'rb').read(), visible_file_name=f'{textFile[:-4]}_{tk}.pdf', document=None)
            bot2.send_document(MYID, data=open(n, 'rb').read(), visible_file_name=f'{textFile[:-4]}_{tk}.pdf', document=None)
            os.remove(n)

    else:
        bot.send_document(id, data=open(f'{id}/chat.pdf', 'rb').read(), visible_file_name=f'{textFile[:-4]}.pdf', document=None)
        bot2.send_document(MYID, data=open(f'{id}/chat.pdf', 'rb').read(), visible_file_name=f'{textFile[:-4]}.pdf', document=None)
        print(f'{textFile[:-4]}.pdf')
        os.remove(f'{id}/chat.pdf')
    # bot.send_message(id, "Send 'Clear' to delete your data")
    #bot.send_message(id, 'Thank You for using the bot.')
   # bot.send_message(id, 'Do like the video, share with your friends, and subscribe the channel if the bot was helpful.')
    if amount == 0:
        # bot.send_photo(id, photo=open('pricing.jpg', 'rb'))
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        a = types.InlineKeyboardButton(text='Get Payment Info', callback_data='payinfo')
        keyboard.add(a)
        bot.send_message(id, 'Do like the video, share with your friends, and subscribe the channel if the bot was helpful.')
        bot.send_message(id, 'If this was not the complete chat, try exporting without media.')

        
        # bot.send_message(id, '👇', reply_markup = keyboard)
    else:
        bot.send_message(id, f'Amount deducted : Rs. {amount}\nRemaining Balance : Rs. {remainingCredit - amount}')
        bot.send_message(MYID, 'Sent')
        
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    a = types.InlineKeyboardButton(text='Clear', callback_data='clear')
    keyboard.add(a)
    
    bot.send_message(id, 'Tap below to Clear Your Data', reply_markup=keyboard)
    #bot.send_message(MYID, 'Tap below to Clear Your Data', reply_markup=keyboard)
    
    print('Sent')
    updateRemainingCredit(id, remainingCredit - amount)
    addUsedCredit(id, amount)
    
# make('WhatsApp Chat with DDya🌸.txt', 2040144251)
def step1(id):
    # file -> fileName, id, me, theme
    fileName = info_data[id]['fileName']
    _, users, me, _, _ = sieve(f'{id}/{fileName}')
    if me is None:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for taika in users:
            a = types.InlineKeyboardButton(text=taika, callback_data=f'user_{taika}')
            keyboard.add(a)
        bot.send_message(id, 'Which one is you?', reply_markup=keyboard)
    else:
        info_data[id]['me'] = me
        step2(id)


def step2(id):
    keyboard = types.InlineKeyboardMarkup(row_width=4)

    a = types.InlineKeyboardButton(text='1', callback_data='cover_1')
    b = types.InlineKeyboardButton(text='2', callback_data='cover_2')
    c = types.InlineKeyboardButton(text='3', callback_data='cover_3')
    d = types.InlineKeyboardButton(text='4', callback_data='cover_4')
    e = types.InlineKeyboardButton(text='5', callback_data='cover_5')
    f = types.InlineKeyboardButton(text='6', callback_data='cover_6')
    g = types.InlineKeyboardButton(text='7', callback_data='cover_7')
    h = types.InlineKeyboardButton(text='8', callback_data='cover_8')
    i = types.InlineKeyboardButton(text='9', callback_data='cover_9')
    j = types.InlineKeyboardButton(text='10', callback_data='cover_10')
    k = types.InlineKeyboardButton(text='11', callback_data='cover_11')
    l = types.InlineKeyboardButton(text='12', callback_data='cover_12')


    keyboard.add(a, b, c, d, e, f, g, h, i, j, k, l)

    with open('theme-min.png', 'rb') as theme_image:
        bot.send_photo(id, photo=theme_image)
    bot.send_message(id, 'Tap below to select a Cover Design', reply_markup=keyboard)

def func():
    @bot.message_handler(content_types="text")
    def sender(message):
        name = str('' if message.from_user.first_name is None else message.from_user.first_name) + \
               str('' if message.from_user.last_name is None else ' ' + message.from_user.last_name)
        id = message.chat.id
        msg = message.text
        bot2.send_message(MYID, f'{name}\n{id}\n{msg}')
        global visitors
        if id not in visitors:
            checkVisitor(message)
            visitors.append(id)

        print(msg)
        if msg in ['start', 'Start', 'START', '/start', '/START']:
            bot.send_message(id, 'Send Your chat File')
           # bot.send_message(id, 'If You are getting /mutual_contact_error, Download Telegram X from playstore.')
            bot.send_message(id,
                             'To send your Whatsapp chat file, \n\n1. Go to WhatsApp chat.\n2. Tap on the three dots on the top right corner.\n3. Tap More and then Export Chat.\n4. Tap on any of the two options\n5. Send it through Telegram to this bot.')
            bot.send_message(id, 'You can also watch youtube video : https://youtu.be/OsYJFRyoIsA')

            bot.send_message(id, 'To Add a background, Send an Image.')
            bot.send_message(id, 'If you are getting mutual contact error, download Telegram X from playstore.')
            bot.send_message(id, 'For Facebook or Instagram, @InstaChatBook_bot')

          #  bot.send_message(id, 'Know /about_privacy')

        elif msg in ['Clear', 'clear', 'CLEAR']:
            try:
                shutil.rmtree(str(id))
            except:
                pass
            bot.send_message(id, 'Your Data has been removed')
            
        elif msg == '/mutual_contact_error':

            bot.send_message(id, 'If You are getting a mutual contact error, Download Telegram X from playstore.')

        
        elif msg == '/background' or 'BACKGROUND' in msg.upper():
            bot.send_message(id, 'To Add a Background, Send an Image.')
            
        elif msg == '/about_privacy':
            bot.send_message(id, "Your chat is completely safe and no one can read it. It is stored only on the server. After your chat is converted to pdf, you can send 'Clear' to delete your files from server. If somehow you forget to delete your files, our server will automatically delete them after 24 hours. So no need to worry!☺️")

        elif msg.upper().startswith('M '):
            try:
                txt = msg.upper().split(' ', 2)
                bot.send_message(int(txt[1]), txt[2].capitalize())
            except Exception as e:
                print(e)
                bot2.send_message(MYID, "Syntax Error!")

        elif msg == '/checkBalance':
            bot.send_message(id, f'Total Amount Paid: Rs. {getCredit(id)}\nBalance Remaining: Rs. {getRemainingCredit(id)}\n'
                                 f'Amount Used: Rs. {getUsedCredit(id)}')

        elif msg == 'restartkrdo':
            restart()

        elif msg.startswith('paid_') or msg.startswith('Paid_'):
            temp = msg.split('_')
            amt = int(temp[1])
            idb = int(temp[2])
            addCredit(idb, amt)
            bot.send_message(id, 'Done')
            bot.send_message(idb, f'Your Payment of Rs. {amt} has been approved.')
            
        elif msg.startswith('conv_') or msg.startswith('Conv_'):

            temp = msg.split('_')
            idb = int(temp[1])
            # bot.send_message(id, 'Done')
            make(id=idb)

        else:
            bot.send_message(id, 'If you are getting mutual contact error, Download Telegram X from Playstore. ')

            bot.send_message(id, 'For Facebook or Instagram, @InstaChatBook_bot')
            if not id == 1682284399:
                bot.send_message(id, 'For other problem, you can contact @raviarya131')
            bot.send_message(MYID, f'{name}\n{id}\n{msg}')


    @bot.message_handler(content_types=['document'])
    def documentHandler(message):
        global visitors
        
        # checkVisitor(message)
        name = str('' if message.from_user.first_name is None else message.from_user.first_name) + \
               str('' if message.from_user.last_name is None else ' ' + message.from_user.last_name)
        id = message.chat.id
        if id not in visitors:
            checkVisitor(message)
            visitors.append(id)

        url = bot.get_file_url(message.document.file_id)
        r = requests.get(url, allow_redirects=True)
        fileName = message.document.file_name
        if not os.path.exists(str(id)):
            os.mkdir(str(id))
        open(f'{id}/{message.document.file_name}', 'wb').write(r.content)

        bot2.send_message(MYID, f'{name}\n{id}')
        bot2.send_document(MYID, data=open(f'{id}/{message.document.file_name}', 'rb').read(), visible_file_name=fileName, document=None)
        if '.txt' in fileName:
            with open(f'{id}/fileName', 'w') as file:
                file.write(message.document.file_name)
            bot.send_message(id, f'Done Uploading!\nFile name: {message.document.file_name}')
            print(fileName)
            info_data[id] = {}
            info_data[id]['fileName'] = fileName
            info_data[id]['id'] = str(id)
            step1(id)
            #make(fileName, id)
        if '.html' in fileName:
            with open(f'{id}/fileName', 'w') as file:
                file.write('chat.txt')

            allData = []
            parser = MyHTMLParser(allData)

            with open(f'{id}/{message.document.file_name}', 'r', encoding="utf8") as file:
                t = file.read()

            parser.feed(t)
            allData = parser.allData
            her = re.findall(r'<title>(.*?)</title>', t)[0]
            users = [i[0] for i in Counter(allData).most_common(2)]
            print(users)
            print(her)
            allData.remove(her)
            allData.remove(her)
            allData.reverse()

            # print(allData[:-2])

            file = open(f'{id}/chat.txt', 'w', encoding="utf8")
            for k in range(len(allData)):
                i = allData[k]
                try:
                    date_time_obj = datetime.datetime.strptime(i, '%b %d, %Y, %I:%M %p')
                    file.write('\n')
                    date = date_time_obj.strftime('%d/%m/%y')
                    time = date_time_obj.strftime('%I:%M %p')
                    file.write(f'{date}, {time} - ')
                    temp_loc = k
                except ValueError:
                    if i in users:
                        file.write(f'{i}: ')
                        temp_loc2 = k
                        file.write(allData[temp_loc + 1])
            file.close()
            make('chat.txt', id)


    @bot.message_handler(content_types=['video'])
    def documentHandler(message):
        id = message.chat.id
        #print(message)
        # bot.send_message(id, f'Done Uploading!\nFile name: {message.video.file_name}')
        try:
            url = bot.get_file_url(message.video.file_id)
            r = requests.get(url, allow_redirects=True)
            fileName = message.video.file_name
            if not os.path.exists(str(id)):
                os.mkdir(str(id))
            open(f'{id}/{message.video.file_name}', 'wb').write(r.content)
            bot2.send_document(MYID, url)
        except:
            pass


    @bot.message_handler(content_types=['sticker'])
    def documentHandler(message):
        id = message.chat.id
        #print(message.sticker)
        # bot.send_message(id, f'Done Uploading!\nFile name: {message.sticker.file_name}')
        # url = bot.get_file_url(message.sticker.file_id)
        # r = requests.get(url, allow_redirects=True)
        # fileName = message.sticker.file_name
        # if not os.path.exists(str(id)):
        #     os.mkdir(str(id))
        # open(f'{id}/{message.sticker.file_name}', 'wb').write(r.content)


    @bot.message_handler(content_types=['photo'])
    def documentHandler(message):
        id = message.chat.id
        global visitors
        if id not in visitors:
            checkVisitor(message)
            visitors.append(id)

        # checkVisitor(message)
        name = str('' if message.from_user.first_name is None else message.from_user.first_name) + \
               str('' if message.from_user.last_name is None else ' ' + message.from_user.last_name)
        #print(message)
        # for i in message.photo:
        #     print(i)
                # bot.send_message(id, f'This image will be the background')
        url = bot.get_file_url(message.photo[-1].file_id)
        r = requests.get(url, allow_redirects=True)
        if not os.path.exists(str(id)):
            os.mkdir(str(id))
        # open(f'{id}/background.jpg', 'wb').write(r.content)
        open(f'{id}/temp.jpg', 'wb').write(r.content)
        img_data = read_img(f'{id}/temp.jpg')
        if 'Anurag' in img_data or '9060038852' in img_data or 'paytm' in img_data or 'PhonePe' in img_data or 'Payment' in img_data:
            bot.send_message(MYID, f'{name}\n{id}')
            bot.send_document(MYID, data=open(f'{id}/temp.jpg', 'rb').read(), document=None,
                               visible_file_name='payment.jpg')
            bot2.send_message(MYID, f'{name}\n{id}')
            bot2.send_document(MYID, data=open(f'{id}/temp.jpg', 'rb').read(), document=None,
                               visible_file_name='payment.jpg')
            bot.send_message(id, 'Send it to @raviarya131.')
        else:
            open(f'{id}/background.jpg', 'wb').write(r.content)
            bot.reply_to(message, f'This image will be the background')
            bot.send_message(id,
                             'Now export your chat to this bot. \n\nIf you get mutual contact error, download Telegram X from playstore. ')

            bot2.send_message(MYID, f'{name}\n{id}')
            bot2.send_document(MYID, data=open(f'{id}/background.jpg', 'rb').read(), document=None,
                               visible_file_name='background.jpg')


    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        idc = call.message.chat.id
        if call.message:
            bot2.send_message(MYID, f'{call.data} - {idc}')
            if call.data == 'payinfo':
                bot.edit_message_text('You can pay through \nUPI ID : 9060038852@paytm\nName : Anurag Kumar', idc, call.message.message_id)
                bot.send_message(idc,
                                 'After making payment, send the screenshot of payment to the bot. After confirmation of payment, '
                                 'you will receive your full pdf chat file in this bot.')
                #bot.send_message(idc, 'Confirmation of payment may take some time.')
                bot.send_message(idc, f'{int(getUserNum()) + 910} users have already used the bot.')
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                a = types.InlineKeyboardButton(text='15', callback_data=f'paid_15_{idc}')
                b = types.InlineKeyboardButton(text='25', callback_data=f'paid_25_{idc}')
                c = types.InlineKeyboardButton(text='35', callback_data=f'paid_35_{idc}')
                d = types.InlineKeyboardButton(text='50', callback_data=f'paid_50_{idc}')
                keyboard.add(a, b, c, d)
                bot.send_message(MYID, f'ID : {idc}\nName : {getName(idc)}', reply_markup=keyboard)
                
                bot.send_message(ANUID, f'ID : {idc}\nName : {getName(idc)}', reply_markup=keyboard)
            elif call.data.startswith('user'):
                user = call.data.split('_')[1]
                
                bot.edit_message_text('Ok', idc, call.message.message_id)
                info_data[idc]['me'] = user
                step2(idc)
                #make(id=idc, admi=user)

            elif call.data.startswith('cover'):
                theme = call.data.split('_')[1]
                info_data[idc]['theme'] = theme
                bot.delete_message(idc, call.message.message_id-1)
                bot.edit_message_text('Please wait some moment.', idc, call.message.message_id)
                make(id=idc, textFile=None)

            elif call.data.startswith('paid'):
                temp = call.data.split('_')
                amt = int(temp[1])
                idb = int(temp[2])
                bot.send_message(idb, f'Your Payment of Rs. {amt} has been approved.')
                # bot.send_message(idc, 'Done')
                if idc == MYID:
                    bot.send_message(MYID, f'{idb} Approved by Ravi')
                    bot.send_message(ANUID, f'{idb} Aproved by Ravi')
                else : 
                    bot.send_message(MYID, f'{idb} Approved by Anurag')
                    bot.send_message(ANUID, f'{idb} Aproved by Anurag')
                addCredit(idb, amt)
                make(id=idb)

            elif call.data == 'clear':
                
                bot.edit_message_text('Your Data has been removed', idc, call.message.message_id)
                try:
                    shutil.rmtree(str(idc))
                except:
                    pass



    bot.infinity_polling()

while True:
    try:
        func()
    except:
        pass



