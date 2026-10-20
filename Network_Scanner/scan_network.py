# This script scans the local network for connected devices using ARP requests.
# It uses the Scapy library to send ARP requests and receive responses.
# The script automatically determines the local IP address.
# It then scans the network for devices and prints their IP address, MAC address, device name, ARP operation, and Ethernet type.
# Besides the modules already imported, you will need to download and install npcap to run this script.
# Only scan networks you own or have permission to scan.
"""Find devices on your local network with ARP requests (needs admin/root rights and Npcap on Windows)."""
import argparse
import socket
from typing import Any

from scapy.all import ARP, Ether, srp


def get_default_range() -> str:
    """Return the /24 subnet of this machine's IP address, e.g. 192.168.1.23/24."""
    # Use the IP of the adapter that has the default route. Connecting a UDP socket sends
    # no packets, it only picks the route (gethostbyname often returns a VirtualBox/VPN adapter)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
    except OSError:
        local_ip = socket.gethostbyname(socket.gethostname())
    return f"{local_ip}/24"


def scan_network(ip_range: str) -> list[dict[str, Any]]:
    """Send ARP requests to every address in ip_range and return the devices that answer."""
    print(f"Scanning the network ({ip_range})...")

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
        except (socket.herror, socket.gaierror):
            hostname = "Unknown"
        devices.append({
            "ip": received.psrc if received.psrc else "Unknown",
            "mac": received.hwsrc if received.hwsrc else "Unknown",
            "hostname": hostname,
            "arp_op": received.op if received.op else "Unknown",
            "ether_type": received.type if received.type else "Unknown",
        })
    return devices


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--range", dest="ip_range", help="network to scan, e.g. 192.168.1.0/24 (default: this machine's /24)")
    args = parser.parse_args()

    devices = scan_network(args.ip_range or get_default_range())

    print("\nNetwork scan completed.")
    print("\nConnected devices:")
    print("{:<20} {:<20} {:<30} {:<40} {:20}".format("IP Address", "MAC Address", "Host Name", "ARP Operation", "Ether Type"))
    print("="*140)
    for device in devices:
        print("{:<20} {:<20} {:<30} {:<40} {:20}".format(device["ip"], device["mac"], device["hostname"], device["arp_op"], device["ether_type"]))

    if not devices:
        print("No devices found. Ensure you're connected to the network and try again.")


if __name__ == "__main__":
    main()
