import os
from cryptography.fernet import Fernet

fileList = []

for file in os.listdir():
    if file == "ransomm.py" or file == "key.key" or file == "ransomdecrypter.py": # Python dosyalarını ve şifrenin olduğu dosyayı şifrelemememiz gerekiyor.
        continue
    if os.path.isfile(file): # Klasörler veya başka tipteki yapılar için bir kontrol yapıyoruz. Eğer dosya bulursak liste içine ekliyoruz.
        fileList.append(file)

with open("key.key","rb") as generatedKey:
    secretKey = generatedKey.read() # keyimizi okuduk.

for file in fileList:
    with open(file,"rb") as theFile:
        contents = theFile.read() # dosya içeriklerimizi okuduk
    contentsDecrypted = Fernet(secretKey).decrypt(contents) # okuduğumuz dosya içeriklerinin keyini secretKey ile açtık.
    with open(file,"wb") as theFile:
        theFile.write(contentsDecrypted) # şifresini çözdüğümüz klasörlerdeki verileri yazdık.