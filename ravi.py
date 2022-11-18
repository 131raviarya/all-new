import requests
import datetime
day = datetime.datetime.now().strftime('%d')
hour = datetime.datetime.now().strftime('%H')
if int(day) < 17 :
    app = 'baghin'
else:
    app = 'baghin2'

print(app)

url = 'https://www.dropbox.com/s/bxn03mkjtkpmdrw/mainpay.py?dl=1' #whatsapp
# url = 'https://www.dropbox.com/s/5f8enws2wipbrjb/pricing.png?dl=1' #insta
r = requests.get(url, allow_redirects=True)
open('mainpay_30july.py', 'wb').write(r.content)



# html_url = '1YOL46JUVbgfYPhSoQc1kxsLzxSh9RTi8'
# main_url = '1xWkkN6SpS651D3-25kLAH1LjzPiC9Kpy'
# image_url = '1QP1oJ0s5dtms-jQOfb00wGDIUQP_Uk6_'
# help_url = '1dndfM7d_VeN9PG95RpDGyQJLTxRJnDcq'



print('downloaded')
try:
    url = 'https://www.dropbox.com/s/e5bc0wycmme0px9/pdf_crop.py?dl=1'
    r = requests.get(url, allow_redirects=True)
    open('pdf_crop.py', 'wb').write(r.content)
except:
    pass

try:
    url = 'https://www.dropbox.com/s/eytjihmfnui5kml/kit.py?dl=1'
    r = requests.get(url, allow_redirects=True)
    open('kit.py', 'wb').write(r.content)
except:
    pass
import mainpay_30july