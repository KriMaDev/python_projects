import re
import requests
from ipwhois import IPWhois

def is_valid_ip(ip):
    # Validate IP address format
    pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    if pattern.match(ip):
        parts = ip.split(".")
        return all(0 <= int(part) <= 255 for part in parts)
    return False

def get_ip_info(ip):
    try:
        obj = IPWhois(ip)
        results = obj.lookup_rdap()
        return results
    except Exception as e:
        return {"error": str(e)}

def check_vpn(ip):
    try:
        # Replace with a reliable VPN detection API
        api_url = f"https://proxycheck.io/v2/{ip}?vpn=1&asn=1"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return data.get("security", {}).get("vpn", False)
        else:
            return {"error": f"API error: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def main():
    ip = input("Enter an IP address to check: ").strip()
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
    if isinstance(vpn_status, dict) and "error" in vpn_status:
        print(f"Error checking VPN status: {vpn_status['error']}")
    else:
        print("VPN Detected" if vpn_status else "No VPN Detected")

if __name__ == "__main__":
    main()