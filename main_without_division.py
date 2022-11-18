from emoji import UNICODE_EMOJI
from kit import divideChat, mergePdf, sieve
import os
from tqdm import tqdm


def extract_emojis(s):
    return [c for c in s if c in UNICODE_EMOJI.keys()]


def make(textFile):
    fileNames = divideChat(textFile)
    # (fileNames)
    _, users, me = sieve(textFile)
    if me == None:
        print('Which one is you?')
        index = 0
        for i in users:
            index = index + 1
            print(f'{index, i}')
        me = users[int(input('Answer in number')) - 1]

    count = 0
    # for banIndex in tqdm(range(len(fileNames))):
    bandar = textFile
    # for bandar in fileNames:
    count = count + 1
    # print(count)
    data, users, _ = sieve(bandar)
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

    with open('index2.html', 'w', encoding='utf-8') as html:
        html.write(r'''<!DOCTYPE html>
    <html>
    <head>
    <title>''' + str(count) + '''</title>
    <link rel="stylesheet" href="style.css">

    </head>
    <body>
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

                    if msg.endswith('jpg (file attached)') or msg.endswith('png (file attached)') or msg.endswith(
                        'gif (file attached)') or msg.endswith('webp (file attached)'):
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

                    elif msg.endswith('mp4 (file attached)\n'):
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
                    if msg.endswith('jpg (file attached)\n') or msg.endswith('webp (file attached)\n'):
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
                    elif msg.endswith('mp4 (file attached)\n'):
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

        html.write(r'</ul></div></body></html>')
        #convertPdf(count)
        #os.remove(bandar)
    # print('Creating Pdf')
    #mergePdf(len(fileNames))
    print('done')


file = input('Enter the chat.txt address ')
make(file)


