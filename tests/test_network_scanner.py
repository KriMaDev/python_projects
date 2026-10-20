import pytest

from check_ip import is_valid_ip, parse_proxycheck
from check_mac import is_valid_mac


@pytest.mark.parametrize("ip", ["192.168.1.10", "8.8.8.8", "0.0.0.0", "255.255.255.255"])
def test_is_valid_ip_accepts_ipv4(ip):
    assert is_valid_ip(ip)


@pytest.mark.parametrize("ip", ["256.1.1.1", "1.2.3", "1.2.3.4.5", "a.b.c.d", "", "1.2.3.4 ", "::1"])
def test_is_valid_ip_rejects_invalid(ip):
    assert not is_valid_ip(ip)


@pytest.mark.parametrize("mac", ["AA:BB:CC:DD:EE:FF", "aa-bb-cc-dd-ee-ff", "00:1A:2B:3C:4D:5E", "001A2B3C4D5E"])
def test_is_valid_mac_accepts_common_formats(mac):
    assert is_valid_mac(mac)


@pytest.mark.parametrize("mac", ["AA:BB:CC:DD:EE", "AA:BB:CC:DD:EE:GG", "AA:BB-CC:DD:EE:FF", "", "nope"])
def test_is_valid_mac_rejects_invalid(mac):
    assert not is_valid_mac(mac)


def test_parse_proxycheck_detects_proxy():
    data = {"status": "ok", "185.220.101.1": {"proxy": "yes", "type": "TOR"}}
    assert parse_proxycheck(data, "185.220.101.1") == {"proxy": True, "type": "TOR"}


def test_parse_proxycheck_clean_ip():
    data = {"status": "ok", "8.8.8.8": {"proxy": "no", "type": "Business"}}
    assert parse_proxycheck(data, "8.8.8.8") == {"proxy": False, "type": "Business"}


def test_parse_proxycheck_api_error():
    data = {"status": "denied", "message": "Daily limit reached"}
    assert parse_proxycheck(data, "8.8.8.8") == {"error": "Daily limit reached"}
