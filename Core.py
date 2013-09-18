__author__ = 'Neo Yan'

from bottle import Bottle,redirect,route

import bottle

import qrcode

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A6

bottle.debug(True)

QrCodeApp=Bottle()

@QrCodeApp.route('/make/:c/:m/:p/:q/:d/:l')
def make(c,m,p,q,d,l):

    return makeQr(None,code=c,materials=m,position=p,quantity=q,makedate=d,line=l)

def makeQr(*keywords,**urlvars):

    code=urlvars.get('code')
    materials=urlvars.get('materials')
    position=urlvars.get('position')
    quantity=urlvars.get('quantity')
    makedate=urlvars.get('makedate')
    line=urlvars.get('line')

    parameter='/'.join([code,materials,position,quantity,makedate,line])

    qr=qrcode.QRCode(version=1,error_correction=qrcode.ERROR_CORRECT_L,box_size=2,border=4)

    qr.add_data('http://Neo-Notebook:8088/Logon/'+parameter+'\n')
    qr.add_data('code='+code+'\n')
    qr.add_data('materials='+materials+'\n')
    qr.add_data('position='+position+'\n')
    qr.add_data('quantity='+quantity+'\n')
    qr.add_data('makedate='+makedate+'\n')
    qr.add_data('line='+line+'\n')
    qr.make(fit=True)
    image=qr.make_image()

    s=canvas.Canvas('test.pdf')

    image.save('qr.jpg')

    s.drawImage('qr.jpg',0,680)
    s.drawString(180,800,'Code:'+code)
    s.drawString(180,780,'Quantity:'+quantity)
    s.showPage()
    s.save()

@QrCodeApp.route('/Logon/:c/:m/:p/:q/:d/:l')

def Logon(c,m,p,q,d,l):
    parameter='\n'+c+'\n'+m+'\n'+p+'\n'+q+'\n'+d+'\n'+l
    return """<a href='#'onClick="window.opener='anyone';window.close();">Close Window</a> """


bottle.run(QrCodeApp,host='0.0.0.0',port=8088,debug=True,reloader=True)