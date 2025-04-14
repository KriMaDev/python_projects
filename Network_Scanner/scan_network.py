# This script scans the local network for connected devices using ARP requests.
# It uses the Scapy library to send ARP requests and receive responses.
# The script automatically determines the local IP address.
# It then scans the network for devices and prints their IP address, MAC address, device name, ARP operation, and Ethernet type.
# Besides the modules already imported, you will need to download and install npcap to run this script.
from scapy.all import ARP, Ether, srp
import socket

# Scan current network for devices and return their details
def scan_network(ip_range):
    print("Scanning the network...")
    
    # Create an ARP request packet
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    # Send the packet and receive responses
    result = srp(packet, timeout=2, verbose=False)[0]
    
    # Parse the responses
    devices = []
    for sent, received in result:
        # Append resolved data from the received packet
        try:
            hostname = socket.gethostbyaddr(received.psrc)[0]
        except socket.herror:
            hostname = "Unknown"
        try:
            devices.append({
                "ip": received.psrc if received.psrc else "Unknown",
                "mac": received.hwsrc if received.hwsrc else "Unknown",
                "hostname": hostname,
                "arp_op": received.op if received.op else "Unknown",
                "ether_type": received.type if received.type else "Unknown",
            })
        except socket.herror:
            hostname = "Unknown"
    return devices

# Automatically get the machine's IP address and derive the subnet
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
curr_ip = f"{local_ip}/24"
devices = scan_network(curr_ip)

if __name__ == "__main__":
    # print(devices)
    print("\nNetwork scan completed.")
    print("\nConnected devices:")
    print("{:<20} {:<20} {:<30} {:<40} {:20}".format("IP Address", "MAC Address", "Host Name", "ARP Operation", "Ether Type"))
    print("="*140)
    for device in devices:
        print("{:<20} {:<20} {:<30} {:<40} {:20}".format(device["ip"], device["mac"], device["hostname"], device["arp_op"], device["ether_type"]))
    
    if not devices:
        print("No devices found. Ensure you're connected to the network and try again.")
