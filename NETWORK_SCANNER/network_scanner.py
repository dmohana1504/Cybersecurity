from scapy.all import ARP, Ether, srp

t_ip = input("Enter a target IP :")
arp = ARP(pdst=t_ip)
ether = Ether(dst = "ff:ff:ff:ff:ff:ff")
packet = ether/arp
result = srp(packet, timeout=3, verbose=0) [0]

clients = []

for sent, recieved in result:
    clients.append({'IP': recieved.psrc, 'MAC': recieved.hwsrc})

print("Devices on the network: ")
print("IP"+" "*18+"MAC")

for client in clients:
    print("{:16} {}".format(client['IP'], client['MAC']))