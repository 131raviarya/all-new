import re

with open('iphone/_chat (3).txt', encoding='utf-8') as file:
    a = file.readlines()
    test = '\[(.*?), (.*?)\] (.*): (.*)'

    raw = []
    for i in a:
        if '‎<attached:' in i:
            print(i)
            i = i.replace('<attached: ', '')
            i = i.replace('>', '')
            print(i)
        x = re.search(test, i)
        if x == None:
            pass
        elif len(x.groups()) == 4:
            raw.append([*x.groups()])
        else: print('Length:', x)
    for i in range(len(raw)):
        test = '(\d+:\d+:\d+)'
        x = re.search(test, raw[i][1])
        if x is not None:
            if len(raw[i][1]) == 11:
                raw[i][1] = raw[i][1][:5]+raw[i][1][-3:]
            elif len(raw[i][1]) == 8:
                raw[i][1] = raw[i][1][:5]



print(len(a), len(raw))


test = '(\d+:\d+:\d+)'

a = '15:46:22'

print(re.search(test, a))

a = '15:46:33'
x = re.search(test, a)
if x is not None and len(a) == 11:
    print(a[:5]+a[-3:])
