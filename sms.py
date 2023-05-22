import datetime, time, socket, datetime, serial

VKSterm = {'18094':['10.10.243.4', 23, True],
           '18095':['10.10.243.5', 23, True],
           '18097':['10.10.243.7', 23, True],
           '18098':['10.10.243.8', 23, True],
           '180911':['10.10.243.11', 23, True],
           '180914':['10.10.243.14', 23, True],
           'gatekeeper_240':['10.10.249.240', 80, True],
           'gatekeeper_241':['10.10.249.241', 80, True],
          }
phones = ('+79061545607',)
port = 'COM4'

def sendLOG(text):
    with open('log.txt', 'a') as log:
        log.write(text+'\r\n')

def sendSMS(tel, text):
    try:
        sim900 = serial.Serial(port, 19200, timeout=3)
        sendTEXT = 'AT\r\n'
        sim900.write(sendTEXT.encode('utf-8'))
        otvet = sim900.read(64)
        if 'OK' in otvet.decode('utf-8'):
            print(otvet.decode('utf-8'))
            time.sleep(1)
            sendTEXT = 'AT+CMGS="'+tel+'"'+'\r\n'
            sim900.write(sendTEXT.encode('utf-8'))
            time.sleep(1)
            sendTEXT = text
            sim900.write(sendTEXT.encode('utf-8'))
            time.sleep(1)
            sim900.write(b'\x1a')
            otvet = sim900.read(64)
            print(otvet.decode('utf-8'))
            print('Send SMS on '+tel)
        else:
            sendLOG('GSM modem ERROR')
            print('GSM modem ERROR')
        sim900.close()
    except serial.SerialException:
        print(port, ' port ERROR')
        sendLOG(port + ' port ERROR')

while 1:
    for VKSnum in VKSterm:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        VKSaddr = (VKSterm[VKSnum][0], VKSterm[VKSnum][1])
        dt_now = datetime.datetime.now()
        log = dt_now.strftime('%d/%m/%Y - %H:%M') + ' test ' + VKSnum
        sendLOG(log)
        print(log)
        if sock.connect_ex(VKSaddr) == 0:
            if VKSterm[VKSnum][2] == False:
                log = dt_now.strftime('%d/%m/%Y - %H:%M') + ' ' + VKSnum + ' change status ON'
                for phone in phones:        
                    sendLOG(log)
                    sendSMS(phone, log)
                    time.sleep(3)
                VKSterm[VKSnum][2] = True
        else:
            if VKSterm[VKSnum][2] == True:
                log = dt_now.strftime('%d/%m/%Y - %H:%M') + ' ' + VKSnum + ' change status OFF'
                for phone in phones:        
                    sendLOG(log)
                    sendSMS(phone, log)
                    time.sleep(3)
                VKSterm[VKSnum][2] = False
        sock.close()
    time.sleep(60)

