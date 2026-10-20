# Network Scanner

Three small networking tools: find devices on your local network, look up who owns an IP address,
and find the manufacturer of a MAC address.

| Script | What it does | Needs admin/root |
|---|---|---|
| `scan_network.py` | Finds devices on your local network with ARP requests | **Yes** |
| `check_ip.py` | Shows RDAP/WHOIS data for an IPv4 address and whether it is a VPN, proxy or Tor node | No |
| `check_mac.py` | Shows the vendor (manufacturer) of a MAC address | No |

> **Ethical use:** only scan networks you own or have explicit permission to scan. Scanning other
> people's networks can break the law and your network's terms of use (for example at work, school or
> in public Wi-Fi).

## Setup

From the repository root, with your virtual environment active (see the [main README](../README.md#setup)):

```bash
pip install -r Network_Scanner/requirements.txt
```

`scan_network.py` additionally needs:

- **Windows:** [Npcap](https://npcap.com/#download) installed (Scapy uses it to send raw packets), and a
  terminal opened with **Run as administrator**.
- **Linux / macOS:** root rights. Use the Python from your virtual environment, because plain `sudo python`
  would use the system Python without Scapy installed: `sudo .venv/bin/python Network_Scanner/scan_network.py`

`check_ip.py` and `check_mac.py` need no special rights. They only need an internet connection.

## scan_network.py: find devices on your network

```bash
python Network_Scanner/scan_network.py                         # scans this machine's /24 network
python Network_Scanner/scan_network.py --range 192.168.1.0/24  # scan a specific range
python Network_Scanner/scan_network.py --help
```

It sends an ARP "who has this IP?" request to every address in the range and lists the devices that answer.
By default it scans the /24 network of the adapter that has your default route. If you use a VPN or
virtual machines, pass `--range` to be sure the right network is scanned.

Example output (addresses changed):

```text
Scanning the network (192.168.1.23/24)...

Network scan completed.

Connected devices:
IP Address           MAC Address          Host Name                      ARP Operation                            Ether Type
============================================================================================================================================
192.168.1.1          aa:bb:cc:00:00:01    router.lan                     2                                        2054
192.168.1.42         aa:bb:cc:00:00:2a    Unknown                        2                                        2054
```

ARP operation `2` means "reply", and Ether type `2054` (0x0806) is ARP. The first run can take up to a minute
on Windows while Scapy loads.

## check_ip.py: who owns an IP address

```bash
python Network_Scanner/check_ip.py 8.8.8.8   # check an address directly
python Network_Scanner/check_ip.py           # asks for the address
```

It uses [RDAP](https://about.rdap.org/) (the modern WHOIS) through `ipwhois`, and the free
[proxycheck.io](https://proxycheck.io/) API for VPN/proxy/Tor detection. Only IPv4 is supported.

Example output (shortened):

```text
Fetching IP information...
IP Information:
asn_registry: arin
asn: 15169
asn_cidr: 8.8.8.0/24
asn_country_code: US
asn_description: GOOGLE - Google LLC, US
...

Checking if the IP is a VPN...
No VPN Detected (type: Business)
```

For a Tor exit node the last line reads `VPN/Proxy Detected (type: TOR)`.

## check_mac.py: who made a network device

```bash
python Network_Scanner/check_mac.py 00:1A:2B:3C:4D:5E   # look up directly
python Network_Scanner/check_mac.py                     # menu: type a MAC or use the example one
```

Accepts `AA:BB:CC:DD:EE:FF`, `aa-bb-cc-dd-ee-ff` and `AABBCCDDEEFF`. It uses the free
[maclookup.app](https://maclookup.app/) API, which allows about 1000 requests per month without a key.

Example output:

```text
For MAC Address 00:1A:2B:3C:4D:5E
Exists & Found: True & True
Random & Private: False & False
Company: Ayecom Technology Co., Ltd.
Address: No. 25, R&D Road 2, Science-Based Industrial Park, Hsinchu  300, TW
Country: TW
Updated: 2015-11-17
MAC Prefix: 001A2B
Block Start: 001A2B000000
Block End: 001A2BFFFFFF
Block Size: 16777215
Block Type: MA-L
```

`Random & Private: True` means the device uses a randomised MAC address (common on phones), so no vendor can be found.

## Libraries

| Package | Used for | Licence |
|---|---|---|
| [scapy](https://pypi.org/project/scapy/) | Building and sending ARP packets | GPL-2.0 |
| [ipwhois](https://pypi.org/project/ipwhois/) | RDAP lookups | BSD-2-Clause |
| [requests](https://pypi.org/project/requests/) | HTTP calls to proxycheck.io and maclookup.app | Apache-2.0 |

Scapy is GPL-2.0 licensed. These scripts import it but do not include or modify it. The repository's
MIT licence covers only the code in this repository.
