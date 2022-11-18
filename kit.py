from PyPDF2 import PdfFileMerger, PdfFileWriter, PdfFileReader
import os
import re
from emoji import UNICODE_EMOJI

print('Ravi kit is running')
def extract_emojis(s):
    return [c for c in s if c in UNICODE_EMOJI.keys()]

def divideChat(fileName):
    # fileName = 'chat4.txt'
    with open(fileName, 'r', encoding='utf-8') as file:
        y = file.readlines()

    #print(y)
    z = len(y) // 1250
    zz = len(y) % 1250
    j = 0
    for i in range(0, len(y), 1250):
        j = j + 1
        with open(f'chats/filename_{j}', 'w', encoding='utf-8') as file:
            file.writelines(y[i:i+1250])
    # with open(f'chats/filename_{j+1}', 'w', encoding='utf-8') as file:
    #     file.writelines(y[len(y)+1250:])
    extraPage = 0 if len(y) %1250 == 0 else 1
    return [f'chats/filename_{j}' for j in range(1, (len(y)//1250)+1+extraPage)]


def mergePdf(length, id):

    pdfs = [f'{id}_{j + 1}.pdf' for j in range(length)]
    merger = PdfFileMerger()
    frontFile = PdfFileReader(f'{id}/cover.pdf', 'rb')
    merger.append(frontFile)
    for pdf in pdfs:

        infile = PdfFileReader(pdf, 'rb')
        #pages_to_delete = [0, infile.getNumPages()-1]
        pages_to_delete = [0,1]
        output = PdfFileWriter()
        for i in range(0, infile.getNumPages()-1):
            if i not in pages_to_delete:
                p = infile.getPage(i)
                output.addPage(p)
        with open(pdf, 'wb') as f:
            output.write(f)

        merger.append(pdf)
    merger.write(f"{id}/chat.pdf")
    merger.close()
    [os.remove(pdf) for pdf in pdfs]

def mergePdf2(file, id):
    merger = PdfFileMerger()
    frontFile = PdfFileReader(f'{id}/cover.pdf', 'rb')
    merger.append(frontFile)
    infile = PdfFileReader(file, 'rb')
    merger.append(infile)
    merger.write(f"{id}/chatx.pdf")
    # os.remove(file)
    return f"{id}/chatx.pdf"
# def convertPdf(name):
#     # driver = webdriver.Chrome(options=options)
#     driver = webdriver.Chrome(driverPath, options=options)
#     # options.binary_location = GOOGLE_CHROME_BIN
#     # driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)
#
#     path = os.path.abspath('index2.html')
#     driver.get(r'file://'+path)
#     #driver.save_screenshot('ss.png')
#     a = driver.execute_cdp_cmd(
#         "Page.printToPDF", {"path": 'html-page.pdf', "format": 'A4', 'printBackground':True,
#                             'marginTop':0,
#                             'marginBottom':0,
#                             'marginLeft':0,
#                             'marginRight':0,
#                             'paperWidth': 8.2677,
#                             'paperHeight': 11.7})
#
#     b64 = a['data']
#
#     bytes = b64decode(b64, validate=True)
#
#     if bytes[0:4] != b'%PDF':
#         raise ValueError('Missing the PDF file signature')
#
#     # Write the PDF contents to a local file
#     with open(f'chats/{name}.pdf', 'wb') as f:
#
#         f.write(bytes)
#     driver.quit()


def sieve(fil):
    file = open(fil, encoding='utf-8')
    file.readline()
    raw = []
    count = 0



    for index, line in enumerate(file.readlines()):
        if '‎<attached:' in line:
            line = line.replace('<attached: ', '')
            line = line.replace('>', ' (file attached)')

        y = r'(.+), (\d+:\d+) - (.*): (.*)'
        x = re.search(y, line)

        # x = re.search(r'(\d+/\d+/\d+), (\d+:\d+\d+ [A-Z]*) - (.*?): (.*)', line)
        if x == None :
            y = r'(\d+/\d+/\d+), (\d+:\d+\d+ [A-Z]*) - (.*?): (.*)'
            x = re.search(y, line)
        if x == None :
            y = r'(\d+/\d+/\d+), (\d+:\d+\d+ [a-z]*) - (.*?): (.*)'
            x = re.search(y, line)
        if x == None :
            y = r'(\d+/\d+/\d+), (\d+:\d+\d+ [A-Z]*) - (.*?)'
            x = re.search(y, line)
        if x == None :
            y = r'(\d+/\d+/\d+), (\d+:\d+\d+ [a-z]*) - (.*?)'
            x = re.search(y, line)
        if x == None :
            y = r'(.+), (\d+:\d+) - (.*)()'
            x = re.search(y, line)
        if x == None :
            y = '\[(.*?), (.*?)\] (.*): (.*)'
            x = re.search(y, line)
        if x == None:
            # print(line)
            # print(count, index, line)
            # input()he
            count += 1
            if not (line.endswith('.jpg\n') or line.endswith('.mp4\n') or line.endswith('.webp\n')):
                try:
                    raw[index-count][-1] += line.strip()+'<br>'
                except Exception as e:
                    pass
        else:
            # print(x.groups())
            if len(x.groups()) == 4:
                raw.append([*x.groups()])


    file.close()
    users = set([i for _,_,i,_ in raw])
    default_user = None
    for name, msg in [[j,i]for _,_,j,i in raw]:

        if 'You deleted this message' in msg:
            default_user = name

    l = raw
    n = 1250
    divided_chat = [l[i:i + n] for i in range(0, len(l), n)]
    with open(fil, 'r', encoding='utf-8') as f:
        xyz = str(f.read())
        em = extract_emojis(xyz)
        emojiList = []
        for j in em:
            emojiList.append('emojies\\'+'U+{:X}'.format(ord(j)))

    for i in range(len(raw)):
        test = '(\d+:\d+:\d+)'
        x = re.search(test, raw[i][1])
        if x is not None:
            if len(raw[i][1]) == 11:
                raw[i][1] = raw[i][1][:5]+raw[i][1][-3:]
            elif len(raw[i][1]) == 8:
                raw[i][1] = raw[i][1][:5]
    print(list(users))
    return raw, list(users), default_user, divided_chat, emojiList

