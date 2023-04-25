import scapy.all as scapy
import optparse

def getUserInput():
    parseObj = optparse.OptionParser()
    parseObj.add_option("-i", "--ip address", dest="ip_addr", help="scanning for ip address")

    (user_inputs, arguments) = parseObj.parse_args()
    return user_inputs

def scanNetwork(user_input):

    #ARP isteği oluşturmak
    #Broadcast
    #Cevap Almak

    arpRequest = scapy.ARP(pdst = user_input)  # Belirttiğimiz IP adresi için bir ARP paketi oluşturduk.
    # print(scapy.ls(scapy.ARP())) scapy metodlarının nasıl kullanılacağının rehberini alabiliriz.

    broadcastPacket = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff") # bu gösterimle genel bir yayın yaptık.
    combinedPacket = broadcastPacket / arpRequest # iki paketi birleştirdik ve kullanımını böyle yapacağız.

    (answered_list,unanswered_list) = scapy.srp(combinedPacket,timeout = 1) # göndermek istediğimiz paketi ve timeout verdik. Timeout ile cevap verilmeyen request için bekleme yapmayız.
    answered_list.summary()

userIpInput= getUserInput() # kullanıcıdan aldığım ip adresine erişiyorum.

scanNetwork(userIpInput.ip_addr)
