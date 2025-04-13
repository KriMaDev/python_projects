from scapy.all import ARP, Ether, srp
import socket
# You will also have to download and install npcap to run this script

def scan_network(ip_range):
    print("Scanning the network...")
    
    # Create an ARP request packet
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    # Send the packet and receive responses
    result = srp(packet, timeout=2, verbose=False)[0]
    #result = srp(final_packet, timeout=2, iface="Your_Interface_Name", verbose=False)[0]
    
    devices = []
    for sent, received in result:
        # Resolve hostname (optional, can slow down the scan)
        try:
            hostname = socket.gethostbyaddr(received.psrc)[0]
        except socket.herror:
            hostname = "Unknown"
        
        devices.append({
            "ip": received.psrc,
            "mac": received.hwsrc,
            "hostname": hostname
        })

    return devices

# Replace this with your IP range, e.g., '192.168.1.0/24'
curr_ip = "192.168.1.1/24"

if __name__ == "__main__":
    
    devices = scan_network(curr_ip)
    
    print("\nConnected devices:")
    print("{:<20} {:<20} {:<30}".format("IP Address", "MAC Address", "Device Name"))
    print("="*70)
    for device in devices:
        print("{:<20} {:<20} {:<30}".format(device["ip"], device["mac"], device["hostname"]))
    
    if not devices:
        print("No devices found. Ensure you're connected to the network and try again.")
