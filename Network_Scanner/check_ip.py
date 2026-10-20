"""Look up who owns an IPv4 address (RDAP/WHOIS) and whether it is a known VPN, proxy or Tor node."""
import argparse
import re
from typing import Any

import requests
from ipwhois import IPWhois

REQUEST_TIMEOUT = 10


def is_valid_ip(ip: str) -> bool:
    """Return True if ip is a valid dotted IPv4 address like 192.168.1.10."""
    # Validate IP address format
    pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    if pattern.match(ip):
        parts = ip.split(".")
        return all(0 <= int(part) <= 255 for part in parts)
    return False


def get_ip_info(ip: str) -> dict[str, Any]:
    """Return the RDAP registration data for an IP, or {"error": ...} if the lookup fails."""
    try:
        obj = IPWhois(ip, timeout=REQUEST_TIMEOUT)
        results = obj.lookup_rdap()
        return results
    except Exception as e:
        return {"error": str(e)}


def parse_proxycheck(data: dict[str, Any], ip: str) -> dict[str, Any]:
    """Turn a proxycheck.io response into {"proxy": bool, "type": str}, or {"error": ...}."""
    if data.get("status") not in ("ok", "warning") or ip not in data:
        return {"error": data.get("message", "unexpected response from proxycheck.io")}
    result = data[ip]
    return {"proxy": result.get("proxy") == "yes", "type": result.get("type", "Unknown")}


def check_vpn(ip: str) -> dict[str, Any]:
    """Ask proxycheck.io whether an IP is a VPN/proxy. Returns {"proxy": bool, "type": str} or {"error": ...}."""
    try:
        api_url = f"https://proxycheck.io/v2/{ip}?vpn=1&asn=1"
        response = requests.get(api_url, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            return parse_proxycheck(response.json(), ip)
        else:
            return {"error": f"API error: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ip", nargs="?", help="IPv4 address to check (asked interactively if omitted)")
    args = parser.parse_args()

    ip = (args.ip or input("Enter an IP address to check: ")).strip()
    if not is_valid_ip(ip):
        print("Invalid IP address format.")
        return

    print("\nFetching IP information...")
    ip_info = get_ip_info(ip)
    if "error" in ip_info:
        print(f"Error fetching IP information: {ip_info['error']}")
    else:
        print("IP Information:")
        for key, value in ip_info.items():
            print(f"{key}: {value}")

    print("\nChecking if the IP is a VPN...")
    vpn_status = check_vpn(ip)
    if "error" in vpn_status:
        print(f"Error checking VPN status: {vpn_status['error']}")
    elif vpn_status["proxy"]:
        print(f"VPN/Proxy Detected (type: {vpn_status['type']})")
    else:
        print(f"No VPN Detected (type: {vpn_status['type']})")


if __name__ == "__main__":
    main()
