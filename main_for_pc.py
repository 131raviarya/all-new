from emoji import UNICODE_EMOJI
from time import sleep
import shutil
from kit import divideChat, mergePdf, sieve
import os
import requests
from pdf_crop import downloadPdf, cropPdf, dividePdf
import telebot
from threading import Thread
import datetime
from rough2 import analyse


auth = 'bbb3ac5b-3568-4143-a9e0-01dede6e34ca'
app_name = 'chand-tara1'

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
TOKEN2 = '2025314077:AAHaS5N98O5mWiKztJena2j62f7R2p8YLAk'
# bot = telebot.TeleBot(TOKEN)
bot = telebot.TeleBot(TOKEN2)
MYID = 2040144251

print('sent')
bot.send_message(MYID, 'Bot Started')
print('Started')

def extract_emojis(s):
    if s == None:
        return []
    return [c for c in s if c in UNICODE_EMOJI.keys()]


def make(textFile,id):

    _, users, me, divided_chats, emojiList = sieve(f'{id}/{textFile}')
    print(users, me)
    dirToCopy = ['icons', 'emojies']
    fileToCopy = ['block.png', 'style.css', 'bc.jpg']
    for di in dirToCopy:
        if not os.path.exists(f'{id}/{di}'):
            shutil.copytree(di, f'{id}/{di}')

    for f in fileToCopy:
        shutil.copyfile(f, f'{id}/{f}')
    print('files copied')
    # fileNames = divideChat(textFile)
    message = bot.send_message(id, 'Please wait sometimes')
    sleep(15)
    if me == None:
        me = users[0]

    count = 0

    message = bot.send_message(id, 'Progress: ░░░░░░░░░░ 0%')
    try:
        analyse(f'{id}/{textFile}')

        bot.send_document(id, data=open(f'z.png', 'rb').read(),
                           visible_file_name='Whatsapp Chat Analysis.png')
        bot.send_document(MYID, data=open(f'z.png', 'rb').read(),
                          visible_file_name='Whatsapp Chat Analysis.png')
        os.remove('z.png')
    except Exception as e:
        print("Couldn't analyse")
        print(e)

    print(message.message_id)
    for divided_chat in divided_chats:
        #print(message.message_id)
        count = count + 1
        print(f'{count}/{len(divided_chats)}')
        progress = int(((count/len(divided_chats))*100)//10)
        toSend = 'Progress: ' + '█' * progress + '░' * (10 - progress) + f'  {count}/{len(divided_chats)}'
        #bot.send_message(id, f'{count}/{len(divided_chats)}')

        message = bot.edit_message_text(toSend, id, message.message_id)
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

                    if msg.startswith('https://') or msg.startswith('http://') or msg.startswith('www.'):
                        msg = f"<a href='{msg}'>{msg}</a>"

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
                                        <li><img src= '""" + msg + r"""' alt=""" + msg + """></li>
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
                                                        <li><img src= '""" + msg + r"""' alt=""" + msg + """></li>
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
            cropPdf(f'{id}/temp2.pdf', count, id)
    print('Creating Pdf')
    bot.send_message(id, 'Creating Pdf')
    mergePdf(count, id)
    print(f'{count} files merged')
    bot.send_message(id, 'Sending File')
    bot.send_message(MYID, 'Sending File')
    print('done')
    sleep(2)
    size = os.path.getsize(f'{id}/chat.pdf')/1024/1024
    print(size)
    if size > 45:
        bot.send_message(id, 'Created File is too long to send.')
        bot.send_message(MYID, 'Created File is too long to send.')
        bot.send_message(id, 'Dividing Pdf')
        names = dividePdf(id)
        for n in names:
            size = os.path.getsize(n)/1024/1024
            bot.send_message(MYID, str(size)+' mb')
            bot.send_document(id, data=open(n, 'rb').read(), visible_file_name='Chat.pdf')
            bot.send_document(MYID, data=open(n, 'rb').read(), visible_file_name='Chat.pdf')
            os.remove(n)

    else:
        bot.send_document(id, data=open(f'{id}/chat.pdf', 'rb').read(), visible_file_name='Chat.pdf')
        bot.send_document(MYID, data=open(f'{id}/chat.pdf', 'rb').read(), visible_file_name='Chat.pdf')
        os.remove(f'{id}/chat.pdf')
    bot.send_message(id, "Send 'Clear' to delete your data")
    print('Sent')
# make('WhatsApp Chat with DDya🌸.txt', 2040144251)


def func():
    @bot.message_handler(content_types="text")
    def sender(message):
        name = str('' if message.from_user.first_name is None else message.from_user.first_name) + \
               str('' if message.from_user.last_name is None else ' ' + message.from_user.last_name)
        id = message.chat.id
        msg = message.text
        print(msg)
        if msg in ['start', 'Start', 'START', '/start', '/START', 'hi', 'Hello', 'Hi', 'Hey', 'hey']:
            bot.send_message(id, 'Send Your chat File')
            bot.send_message(id,
                             'To do this\n\n1. go to whatsapp chat.\n2. Tap on the three dots on the top right corner.\n3.Tap More and then Export Chat.\n4. Tap on any of the two options\n5. Send it through Telegram to this bot.')
            bot.send_message(id, 'You can also watch youtube video : https://youtu.be/ASbgkpGa04w')
        if msg in ['Clear', 'clear', 'CLEAR']:
            shutil.rmtree(str(id))
            bot.send_message(id, 'Your Data has been removed')
        bot.send_message(MYID, f'{name}\n{id}\n{msg}')


    @bot.message_handler(content_types=['document'])
    def documentHandler(message):
        name = str('' if message.from_user.first_name is None else message.from_user.first_name) + \
               str('' if message.from_user.last_name is None else ' ' + message.from_user.last_name)
        id = message.chat.id
        bot.send_message(id, f'Done Uploading!\nFile name: {message.document.file_name}')
        url = bot.get_file_url(message.document.file_id)
        r = requests.get(url, allow_redirects=True)
        fileName = message.document.file_name
        if not os.path.exists(str(id)):
            os.mkdir(str(id))
        open(f'{id}/{message.document.file_name}', 'wb').write(r.content)
        bot.send_message(MYID, f'{name}\n{id}')
        bot.send_document(MYID, data=open(f'{id}/{message.document.file_name}', 'rb').read(), visible_file_name=fileName)
        if 'WhatsApp Chat with ' in fileName:
            print(fileName)
            make(fileName, id)


    @bot.message_handler(content_types=['video'])
    def documentHandler(message):
        id = message.chat.id
        #print(message)
        bot.send_message(id, f'Done Uploading!\nFile name: {message.video.file_name}')
        url = bot.get_file_url(message.video.file_id)
        r = requests.get(url, allow_redirects=True)
        fileName = message.video.file_name
        if not os.path.exists(str(id)):
            os.mkdir(str(id))
        open(f'{id}/{message.video.file_name}', 'wb').write(r.content)


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
        name = str('' if message.from_user.first_name is None else message.from_user.first_name) + \
               str('' if message.from_user.last_name is None else ' ' + message.from_user.last_name)
        #print(message)
        # for i in message.photo:
        #     print(i)
        bot.send_message(id, f'This image will be the background')
        url = bot.get_file_url(message.photo[-1].file_id)
        r = requests.get(url, allow_redirects=True)
        if not os.path.exists(str(id)):
            os.mkdir(str(id))
        open(f'{id}/background.jpg', 'wb').write(r.content)
        bot.send_message(MYID, f'{name}\n{id}')
        bot.send_document(MYID, data=open(f'{id}/background.jpg', 'rb').read(),
                           visible_file_name='background.jpg')

    bot.infinity_polling()

while True:
    try:
        func()
    except:
        pass


from kit import sieve
import re
from selenium import webdriver
from time import sleep
import os
from selenium.webdriver.chrome.options import Options
from emoji import UNICODE_EMOJI
from datetime import datetime, timedelta

CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
GOOGLE_CHROME_BIN = '/app/.apt/usr/bin/google-chrome'


def extract_emojis(s):
    if s == None:
        return []
    return [c for c in s if c in UNICODE_EMOJI.keys()]


def to24hr(s):
    in_time = datetime.strptime(s, "%I:%M %p")
    out_time = datetime.strftime(in_time, "%H:%M")
    return out_time

def msgOverTimeData(raw, user=None):
    def getMsgPerDate(rawdata):
        def convertOneDigitToTwoDigit(i):
            return f"{int(i.split('/')[0]):02}/{int(i.split('/')[1]):02}/{i.split('/')[2] if len(i.split('/')[2])==4 else '20' + i.split('/')[2]}"

        temp = [i[0] for i in rawdata]
        dates = []
        separatedDate = []
        for i in temp:
            if i not in dates:
                dates.append(i)
                separatedDate.append(i.split('/'))
        temp = [max([int(i) for i, j, _ in separatedDate]), max([int(j) for i, j, _ in separatedDate])]
        if temp[0] > 12:
            frmt = '%d/%m/%Y'
        elif temp[1] > 12:
            frmt = '%m/%d/%Y'
        else:
            frmt = '%d/%m/%Y'
        if user == None:
            dateMsg = [(convertOneDigitToTwoDigit(i), len([j[2] for j in rawdata if j[0] == i])) for i in dates]
        else :
            dateMsg = [(convertOneDigitToTwoDigit(i), len([j[2] for j in rawdata if j[0] == i and j[2] == user])) for i
                       in dates]
        return [dateMsg, frmt]

    def deltaToDeltaNum(x):
        return int(str(x).split(',')[0].split()[0])

    dateMsg = getMsgPerDate(raw)
    # print(dateMsg[0])

    frmt = dateMsg[1]
    startDate = datetime.strptime(dateMsg[0][0][0], frmt)
    endDate = datetime.strptime(dateMsg[0][-1][0], frmt)
    delta = datetime.strptime(dateMsg[0][-1][0], frmt) - startDate
    delta = deltaToDeltaNum(delta)

    split = 59
    chunkSize = delta//59
    remainder = delta % 59
    chunkDate = startDate
    temper = []
    for k in range((delta//chunkSize)+1):
        chunkDate = chunkDate + timedelta(days=chunkSize)
        temp = []
        for i, j in dateMsg[0]:
            date = datetime.strptime(i, frmt)
            # print(chunkDate - timedelta(days=chunkSize), date, chunkDate)
            # input()
            if chunkDate - timedelta(days=chunkSize) <= date < chunkDate:
                temp.append([i, j])
        temper.append(temp)

    # d = [i[-1][0] for i in temper]
    # print(d, len(d))
    dayData = [sum(i[1] for i in j) for j in temper]
    dateSplit = 6
    dayChunk = (delta//(dateSplit+1))-1
    nameData = []
    date = startDate
    for i in range(dateSplit):
        date = date + timedelta(dayChunk)
        nameData = nameData + ['']*((len(dayData)-dateSplit)//dateSplit)
        nameData.append(date.strftime('%b %d, %y'))
    nameData = nameData + ['']*(len(dayData)-len(nameData))
    # print(dayData)
    # print(nameData)
    # print(len(nameData))
    sDate = startDate.strftime('%b %d, %Y')
    eDate = endDate.strftime('%b %d, %Y')
    return [['', '']+nameData+['', ''], [0, 0]+dayData+[0, 0], sDate, eDate]


# [print(i) for i in msgOverTimeData(rawData)]
# [print(i) for i in msgOverTimeData(rawData, me)]
# [print(i) for i in msgOverTimeData(rawData, 'Ridmi 💕')]

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)



def getDailyTimeData(raw, user):
    times = [i[1] for i in raw if i[2]==user]
    # print(times)
    temp = []
    # print(times)
    # input()
    if times[3][-1].isalpha():
        for i in times:
            temp.append(to24hr(i))
    times = temp
    hourList = [int(i.split(':')[0]) for i in times]
    # print(hourList)
    # print(hourList)
    # print(len(hourList))
    data = '[,,'+ str([hourList.count(i) for i in range(24)])[1:-1]+',,]'
    # print([(i, hourList.count(i)) for i in range(24)])
    hours = ['', '']+['12 AM', '', '', '', '4 AM', '', '', '', '', '', '10 AM', '', '', '', '', '', '4 PM', '', '', '', '', '', '10 PM', '']+['', '']
    return data


def textDistribution(raw, user=None):
    if not user==None:
        texts = [i[3] for i in raw if i[2] == user and '<Media omitted>' not in i[3]]

    else:
        texts = [i[3] for i in raw if '<Media omitted>' not in i[3]]

    noOfText = len(texts)
    allText = ' '.join(texts)
    emojiList = extract_emojis(allText)
    noOfEmoji = len(emojiList)
    allTextEmojiFree = deEmojify(allText)
    allWordList = re.split(' |, |,|-', allTextEmojiFree)
    temp = []
    for i in set(allWordList):
        temp.append((i, allWordList.count(i)))

    temp.sort(key=lambda a: a[1], reverse=True)
    wordData = temp
    temp = []
    for i in set(emojiList):
        temp.append((i, emojiList.count(i)))

    temp.sort(key=lambda a: a[1], reverse=True)
    emojiData = temp

    # print(f'emoji = {len(emojiList)}')
    # print(f'words = {len(allWordList)}')
    # print(wordData)
    # print(emojiData)
    noOfWords = len(allWordList)
    # print(noOfWords)
    return [noOfText, noOfWords, noOfEmoji, wordData, emojiData]


# textDistribution(rawData, other)
# textDistribution(rawData, me)
# textDistribution(rawData)

# getDailyTimeData(rawData, me)
# getDailyTimeData(rawData, other)

def analyse(fileName):

    textFile = fileName

    rawData, users, me, divided_chats, emojiList = sieve(f'{textFile}')

    users.sort(key=len)
    if me == None: me = users[0]
    users.remove(me)
    other = users[0]
    with open(r'lalwa.html', 'r', encoding='utf-8') as file:
        x = file.read()
        dayName1, barHeight1, sDate, eDate = msgOverTimeData(rawData)
        x = x.replace('#dayName1', str(dayName1))
        x = x.replace('#barHeight1', str(barHeight1))
        x = x.replace('#strEndDate', f'{sDate} - {eDate}')
        myData = msgOverTimeData(rawData, me)[1]
        otherData = msgOverTimeData(rawData, other)[1]

        if sum(myData)/len(myData) > sum(otherData)/len(otherData):
            x = x.replace('#lineHeight1', str(otherData))
            x = x.replace('#lineHeight2', str(myData))
            x = x.replace('#color1', 'otherColor')
            x = x.replace('#color2', 'myColor')
        else :
            x = x.replace('#lineHeight1', str(myData))
            x = x.replace('#lineHeight2', str(otherData))
            x = x.replace('#color2', 'otherColor')
            x = x.replace('#color1', 'myColor')
        x = x.replace('#myDailyTime', getDailyTimeData(rawData, me))
        x = x.replace('#otherDailyTime', getDailyTimeData(rawData, other))
        x = x.replace('#meName', deEmojify(me).upper())
        x = x.replace('#otherName', deEmojify(other).upper())
        a1, a2, a3, a4, a5 = textDistribution(rawData, me)
        b1, b2, b3, b4, b5 = textDistribution(rawData, other)
        c1, c2, c3, c4, c5 = textDistribution(rawData)
        x = x.replace('#aa1', str(a1))
        x = x.replace('#aa2', str(a2))
        x = x.replace('#aa3', str(a3))
        ucode = 'U+{:X}'.format(ord(a5[0][0]))
        aa5 = fr'<img class="emoji" src="emojies\\{ucode}.png">'
        x = x.replace('#aa4', f'{a4[0][0]} ({a4[0][1]})')
        x = x.replace('#aa5', f'{aa5} ({a5[0][1]})')
        x = x.replace('#bb1', str(b1))
        x = x.replace('#bb2', str(b2))
        x = x.replace('#bb3', str(b3))
        ucode = 'U+{:X}'.format(ord(b5[0][0]))
        bb5 = fr'<img class="emoji" src="emojies\\{ucode}.png">'
        x = x.replace('#bb4', f'{b4[0][0]} ({b4[0][1]})')
        x = x.replace('#bb5', f'{bb5} ({b5[0][1]})')
        x = x.replace('#cc1', str(a1+b1))
        x = x.replace('#cc2', str(a2+b2))
        x = x.replace('#cc3', str(a3+b3))
        ucode = 'U+{:X}'.format(ord(c5[0][0]))
        cc5 = fr'<img class="emoji" src="emojies\\{ucode}.png">'
        x = x.replace('#cc4', f'{c4[0][0]} ({c4[0][1]})')
        x = x.replace('#cc5', f'{cc5} ({c5[0][1]})')
        topWords = [i[0] for i in c4 if i[0] != ''][:10]
        # print(topWords)
        myTopWords = []
        otherTopWords = []
        for i in topWords:
            if i in dict(a4).keys():
                myTopWords.append(dict(a4)[i])
            else:
                myTopWords.append(0)
            if i in dict(b4).keys():
                otherTopWords.append(dict(b4)[i])
            else:
                otherTopWords.append(0)



        x = x.replace('#topWords', str(topWords))
        x = x.replace('#myTopWords', str(myTopWords))
        x = x.replace('#otherTopWords', str(otherTopWords))

        topEmojis = [i[0] for i in c5 if i[0] != ''][:5]
        myTopEmojis = []
        otherTopEmojis = []
        for i in topEmojis:
            if i in dict(a5).keys():
                myTopEmojis.append(dict(a5)[i])
            else:
                myTopEmojis.append(0)
            if i in dict(b5).keys():
                otherTopEmojis.append(dict(b5)[i])
            else:
                otherTopEmojis.append(0)
        x = x.replace('#topEmojis', str(topEmojis))
        x = x.replace('#myTopEmojis', str(myTopEmojis))
        x = x.replace('#otherTopEmojis', str(otherTopEmojis))
        x = x.replace('#meTextAvg', str(a2/a1))
        x = x.replace('#otherTextAvg', str(b2 / b1))
        topEmojiCode = list(map(lambda a: 'U+{:X}'.format(ord(a)), topEmojis))
        for i in range(len(topEmojiCode)):
            x = x.replace(f'#em{i+1}', fr'emojies\\{topEmojiCode[i]}.png')
        # print(topEmojiCode)
        # print(topEmojis, c4)
        # print(myTopEmojis, a4)
        # print(otherTopEmojis, b4)
        print('Done')



    with open('lala.html', 'w', encoding='utf-8') as file:
        file.write(x)

    chrome_options = Options()
    WINDOW_SIZE = "1234,1240"
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.binary_location = GOOGLE_CHROME_BIN
    CHROMEDRIVER_PATH = 'chromedriver.exe'
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)

    path = os.path.abspath('lala.html')
    print(path)
    driver.get(r"file:///" + path)
    sleep(5)
    driver.get_screenshot_as_file('z2.png')
    driver.find_element_by_class_name('ravi').screenshot('z.png')
    driver.quit()


