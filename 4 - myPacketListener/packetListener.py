import scapy.all as scapy
from scapy.layers import http

def listenPackets(interface):
    # store > gelen paketleri hafızaya kaydetmek için verilen parametre.
    # prn > callback fonksiyonudur. Paket geldiğinde hangi fonksiyona yazılsın onu yazdık.
    scapy.sniff(iface = interface, store = False, prn = analyzePackets)

def analyzePackets(packet):
    # Katman ile istediğimiz verileri filtreleyebiliriz.
    if packet.haslayer(http.HTTPRequest):
        if packet.haslayer(scapy.Raw):
            print(packet[scapy.Raw].load)

listenPackets("eth0")

