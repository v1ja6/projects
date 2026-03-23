from project import ip_addr_check
from project import subnet_checker
from project import reverse_dns_lookup
import pytest

def test_ip():
    assert ip_addr_check("8.8.8.8") == True
    assert ip_addr_check("1.1.1") == False
    assert ip_addr_check("123213.1.1.1") == False
    assert ip_addr_check("1.1.1..1") == False
    assert ip_addr_check("1.1.wdq1") == False
    assert ip_addr_check("192.168.1.16") == True

def test_subnet():
    assert subnet_checker("/24") == True
    assert subnet_checker("24") == False
    assert subnet_checker("/35") == False
    assert subnet_checker("fewafwefwefwe") == False

def test_dns():
    assert reverse_dns_lookup("8.8.8.8") == "dns.google"
