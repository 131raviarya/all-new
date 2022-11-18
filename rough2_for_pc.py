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
    blabla = []
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
        blabla.append((chunkDate - timedelta(days = chunkSize//2)).strftime("%d %b, %Y"))
    # d = [i[-1][0] for i in temper]
    # print(d, len(d))
    print(len(temper))
    print(len(blabla))
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
    return [['', '']+blabla+['', ''], [0, 0]+dayData+[0, 0], sDate, eDate]


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
    # print(temp)
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
    # driver.execute_script("document.body.style.zoom='200%'")
    path = os.path.abspath('lala.html')
    print(path)
    driver.get(r"file:///" + path)
    sleep(5)
    driver.get_screenshot_as_file('z2.png')
    driver.find_element_by_class_name('ravi').screenshot('z.png')
    driver.quit()

