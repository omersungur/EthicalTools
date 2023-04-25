import subprocess # komut kümeleri çalıştırabilmemiz için kütüphane
import optparse  # Terminal içinde kullanıcıdan input almaya yarayan kütüphane.
import re # Regex kütüphanesi

def getUserInput():
    parseObj = optparse.OptionParser()
    parseObj.add_option("-i", "--interface", dest="interface", help="interface to change")
    parseObj.add_option("-m", "--mac", dest="mac_addr", help="new mac address")

    return parseObj.parse_args()  # ilk parametreyle kullanıcının girdiği inputları alabiliyoruz. (user_inputs,arguments) dönderir.

def macChanger(user_interface, user_mac_addr):
    subprocess.call(["ifconfig", user_interface, "down"])
    subprocess.call(["ifconfig", user_interface, "hw", "ether", user_mac_addr])
    subprocess.call(["ifconfig", user_interface, "up"])

def showInterface(interface):
    ifconfig = subprocess.check_output(["ifconfig",interface])
    # w regex komutuyla bütün harfleri alabiliyoruz ve aşağıda belirttiğimiz patern bizim mac paternimiz.
    newMacAddr = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig)) # regex patterni, regex uygulanacak metin

    if newMacAddr: # newMacAddr boş değilse bura çalışıyor.
        return newMacAddr.group(0) # belirttiğimiz paterne sahip bir sürü sonuç çıkabilir. Biz ilk bulduğumuz sonucu alıyoruz.
    else:
        return None

(user_inputs, arguments) = getUserInput()

macChanger(user_inputs.interface, user_inputs.mac_addr)

final_mac = showInterface(str(user_inputs.interface))

if final_mac == user_inputs.mac_addr:
    print("Successful!")
else:
    print("Error!")
